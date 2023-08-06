import nltk
import nltk.corpus
from typing import List, Optional, Tuple, Union
import re
from nltk.corpus import wordnet
from nltk.corpus.reader import Synset
from nltk.wsd import lesk
from semcluster.util import split_list, flatten
import math
from .util import pairwise_similarity
from sklearn.cluster import AffinityPropagation
import numpy as np
from .util import groupby, subsequence_index
import sys
from .esa import ESA, WikiESA


class _CandidatePhrase:
    def __init__(
            self,
            parts_of_speech: List[Tuple[str, str]],
            pattern_type: str,
            window: Optional[List[str]] = None,
            synset: Optional[Synset] = None,
    ):
        self.parts_of_speech = parts_of_speech
        self.window = window
        self.synset = synset
        self.pattern_type = pattern_type

    @property
    def phrase(self):
        if len(self.parts_of_speech) == 0:
            return []
        phrase, *_ = zip(*self.parts_of_speech)
        return list(phrase)


    def split(self) -> '_CandidatePhrase':
        # TODO: Better splitting
        if any(tag in {'STOPWORD'} for _, tag, *_ in self.parts_of_speech):
            split = split_list(self.parts_of_speech, lambda x: x[1] in {'STOPWORD'})
            if len(split) == 2:
                return _CandidatePhrase(split[1], self.pattern_type, self.window, self.synset)
            elif len(split) == 1:
                return _CandidatePhrase(split[0], self.pattern_type, self.window, self.synset)

        return _CandidatePhrase(self.parts_of_speech[1:], self.pattern_type, self.window, self.synset)


    def contains(self, pattern: str):
        return pattern in self.formatted_phrase

    @property
    def formatted_phrase(self) -> str:
        return " ".join(self.phrase)


    @property
    def tags(self) -> List[str]:
        return [tag for _, tag, *_ in self.parts_of_speech]


    def __hash__(self):
        return self.synset.__hash__()


    def __eq__(self, other):
        return (
            self.parts_of_speech == other.parts_of_speech and
            self.synset == other.synset
        )


class _CandidatePhraseSet:
    def __init__(
        self,
        synset: Optional[Synset],
        phrase: List[str],
        sources: List[_CandidatePhrase]
    ):
        self.synset = synset
        self.phrase = phrase
        self.sources = sources


    @property
    def formatted_phrase(self) -> str:
        return " ".join(self.phrase)


    @property
    def pattern_type(self) -> str:
        return self.sources[0].pattern_type


    @property
    def parts_of_speech(self) -> List[Tuple[str, str]]:
        return self.sources[0].parts_of_speech


    def __hash__(self):
        return self.synset.__hash__()


    def __eq__(self, other):
        return (
            self.synset == other.synset and
            self.phrase == other.phrase and
            self.sources == other.sources
        )


class SemClusterKeywordExtractor:
    def __init__(self, esa: Optional[ESA] = None):
        """
        Initializes a keyword extractor based on the SemCluster algorithm.
        The ESA parameter can be used to specify, what system should be used for explicit semantic analysis.
        Defaults to esa_wiki if no other value is set. This requires the esa_wiki package to be installed.

        :param esa: Explicit Semantic Analysis interface
        """
        self._wiki_esa = esa if esa is not None else WikiESA()
        self._stopwords = set(nltk.corpus.stopwords.words('english'))


    def __extract_candidate_phrases(self, parts_of_speech):
        # TODO: Improve selection of stopwords
        pos_stopword_mapped = [
            (word, "STOPWORD" if word in self._stopwords or tag in {"DT", "IN"} else tag) for word, tag in parts_of_speech
        ]

        grammar = """
        E: {<NNP|NNPS>*<STOPWORD>*<NNP|NNPS>+}
        C: {<JJ>*<NN|NNS>+}
        N: {<NN|NNS>}
        """

        parser = nltk.RegexpParser(grammar)
        # noinspection PyTypeChecker
        tree = parser.parse(pos_stopword_mapped)
        candidate_roots = [root for root in tree.subtrees() if root.label() in {'E', 'C', 'N'}]
        candidate_phrases = [(root.label(), root.leaves()) for root in candidate_roots]

        # SemCluster paper filters phrases to a max length of 5
        # candidate_phrases = [phrase for phrase in candidate_phrases if len(phrase) <= 5]
        window = [w for w, *_ in parts_of_speech]
        candidate_phrases = [_CandidatePhrase(pos, root, window) for root, pos in candidate_phrases]
        return candidate_phrases


    def __lookup_phrases(self, candidates: List[_CandidatePhrase]):
        def __recursive_lookup(phrase: _CandidatePhrase) -> Optional[_CandidatePhrase]:
            if len(phrase.phrase) == 0:
                return None

            phrase_name = "_".join(phrase.phrase)
            # Noun phrases are all listed as NOUN in WordNet
            synsets = wordnet.synsets(phrase_name, pos=wordnet.NOUN)

            if len(synsets) > 0:
                synset = lesk(phrase.window, phrase_name, synsets=synsets)
                return _CandidatePhrase(phrase.parts_of_speech, phrase.pattern_type, phrase.window, synset)

            # Remove first word and check, whether that gives a definition
            __recursive_lookup(phrase.split())

        # discard phrases that have no definition in core ontology (WordNet)
        phrases = [__recursive_lookup(p) for p in candidates]

        return [
            phrase for phrase in phrases
            if phrase is not None
            and phrase.formatted_phrase not in self._stopwords  # TODO: Better noise word filtering
        ]


    @classmethod
    def __synset_wordset(cls, synset: Synset, follow_related: bool = True) -> set:
        synonyms = set(w for s in synset.lemma_names() for w in s.split("_"))
        gloss = set(re.split(r'[^a-zA-Z0-9]+', synset.definition()))
        related = set()
        if follow_related:
            queries = [
                *synset.hypernyms(),
                *synset.hyponyms(),
                *synset.instance_hypernyms(),
                *synset.instance_hyponyms(),
                *synset.member_meronyms(),
                *synset.member_holonyms(),
                *synset.part_meronyms(),
                *synset.part_holonyms(),
                *synset.substance_meronyms(),
                *synset.substance_holonyms()
            ]
            related = set(flatten(
                cls.__synset_wordset(query, follow_related=False) for query in queries
            ))

        return synonyms.union(gloss).union(related)


    @classmethod
    def __score_phrase_similarity(cls, a: Synset, b: Synset) -> Optional[float]:
        """
        Extended WuPalmer WordNet similarity

        :param a: First synset
        :param b: Second synset
        :return: WuPalmer similarity between a and b
        """

        # Lowest common subsumer
        lcss = a.lowest_common_hypernyms(b)
        if len(lcss) == 0:
            print(f"LCS between {a} and {b} does not exist")
            return 0

        lcs = lcss[0]

        ls_a = a.shortest_path_distance(lcs)
        ls_b = b.shortest_path_distance(lcs)
        d = lcs.max_depth() + 1

        a_wordset = cls.__synset_wordset(a)
        b_wordset = cls.__synset_wordset(b)

        overlap = math.log(len(a_wordset.intersection(b_wordset)) + 1)
        sim = (2 * d + overlap) / (ls_a + ls_b + 2 * d + overlap)

        return sim


    def __score_cluster_similarity(self, medoid1: Union[_CandidatePhraseSet, _CandidatePhrase], medoid2: Union[_CandidatePhraseSet, _CandidatePhrase]) -> float:
        return self._wiki_esa.measure_similarity(medoid1.formatted_phrase, medoid2.formatted_phrase)


    @classmethod
    def __group_candidates(cls, candidates: List[Union[_CandidatePhraseSet, _CandidatePhrase]]):
        candidates = groupby(candidates, key=lambda c: c.synset)
        candidates = [_CandidatePhraseSet(group[0].synset, group[0].phrase, group) for pos, group in candidates.items()]
        return candidates


    @classmethod
    def __compute_clusters(cls, candidates: List[Union[_CandidatePhraseSet, _CandidatePhrase]]) -> List[Tuple[Union[_CandidatePhraseSet, _CandidatePhrase], List[Union[_CandidatePhraseSet, _CandidatePhrase]]]]:
        similarity = pairwise_similarity([x.synset for x in candidates], metric=cls.__score_phrase_similarity)

        # set similarity(x,x) to median
        similarity += np.eye(similarity.shape[0]) * np.median(similarity)

        # Perform relational clustering using AP on similarity semcluster.matrix
        ap = AffinityPropagation(affinity='precomputed').fit(similarity)

        # medoids = list(np.array(candidates)[ap.cluster_centers_indices_])

        # Select medoids of clusters (like centroids but for relational clustering)
        clusters = [(candidates[medoid_idx], []) for medoid_idx in ap.cluster_centers_indices_]

        # Add candidates to their corresponding clusters
        for (i, label) in enumerate(ap.labels_):
            if i != ap.cluster_centers_indices_[label]:
                clusters[label][1].append(candidates[i])

        return clusters

    @classmethod
    def __select_seeds(cls, clusters: List[Tuple[_CandidatePhraseSet, List[_CandidatePhraseSet]]], threshold: float) -> List[Union[_CandidatePhraseSet, _CandidatePhrase]]:
        return [
            medoid for medoid, _ in clusters
        ] + [
            candidate
            for medoid, candidates in clusters
            for candidate in candidates
            if cls.__score_phrase_similarity(medoid.synset, candidate.synset) >= threshold
        ]


    def __filter_seeds(self, medoids: List[Union[_CandidatePhraseSet, _CandidatePhrase]]) -> List[Union[_CandidatePhraseSet, _CandidatePhrase]]:
        medoid_similarity = pairwise_similarity(medoids, self.__score_cluster_similarity)
        medoid_score = np.sum(medoid_similarity, axis=1) / (medoid_similarity.shape[1] - 1)
        avg_score = np.mean(medoid_score)

        # Select only the medoids whose score is greater than the avg score
        return list(np.array(medoids)[medoid_score >= avg_score])


    @classmethod
    def __select_phrases(cls, seeds: List[Union[_CandidatePhraseSet, _CandidatePhrase]], phrases: List[_CandidatePhrase]) -> List[str]:
        results = []
        seeds = set(seeds)  # Create copy so that seeds does not get mutated

        # Implicitly following paper extraction rules:
        for phrase in phrases:
            active_seeds = [seed for seed in seeds if phrase.contains(seed.formatted_phrase)]
            if len(active_seeds) == 0:
                continue
            # If E pattern: Only take seed
            if active_seeds[0].pattern_type == "E":
                results.append(active_seeds[0].formatted_phrase)
            else:
                # If C pattern or N pattern: take <JJ>*<NN|NNS>+ chunk surrounding phrase
                # Every N pattern will be extracted as a C pattern, so its surrounding <JJ>*<NN|NNS>+ phrase is extracted as well.
                results.append(phrase.formatted_phrase)
            for s in active_seeds:
                # Only use first match for seed, remove seed after match has been found
                seeds.remove(s)

        return results


    def extract_keyphrases(self, document: str, seed_threshold: float = 0.7, verbose: bool = False) -> List[str]:
        """
        Extracts the most important keyphrases of the given document using the SemCluster algorithm.
        Keyphrases are noun phrases and can span multiple words.

        Candidate phrases are clustered based on their similarity and the medoids are selected as seeds for keyphrases.
        The seed set will be extended with other samples from the clusters with an extended Wu-Palmer similarity greater than
        seed_threshold. A seed_threshold of 1 inhibits the selection of additional seeds.
        A threshold of 0 selects all candidates as seeds.

        :param document: Large text to extract keyphrases from
        :param seed_threshold: Threshold for additional keyphrases
        :param verbose: If set to True, progress is reported to stdout
        :return:
        """
        if verbose:
            print("Tokenizing document... ", end='', flush=True)
        document = document.lower()
        sentences = nltk.sent_tokenize(document)
        tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
        if verbose:
            print("Done.")

        if verbose:
            print("Tagging POS... ", end='', flush=True)
        parts_of_speech = [nltk.pos_tag(s_tokens) for s_tokens in tokens]
        if verbose:
            print("Done.")

        if verbose:
            print("Extracting candidates... ", end='', flush=True)
        full_candidate_phrases = [
            candidate for pos in parts_of_speech for candidate in self.__extract_candidate_phrases(pos)
        ]
        if verbose:
            print("Done.")

        if verbose:
            print("Looking up Synsets... ", end='', flush=True)
            sys.stdout.flush()
        candidates = self.__lookup_phrases(full_candidate_phrases)
        if verbose:
            print("Done.")

        if verbose:
            print("Clustering candidates... ", end='', flush=True)
        # candidates = self.__group_candidates(candidates)
        clusters = self.__compute_clusters(candidates)
        if verbose:
            print("Done.")

        if verbose:
            print("Selecting seeds... ", end='', flush=True)
        seeds = self.__select_seeds(clusters, seed_threshold)
        if verbose:
            print(f"Done. [{len(seeds)} seeds]")
        if verbose:
            print("Filtering seeds... ", end='', flush=True)
        seeds = self.__filter_seeds(seeds)
        if verbose:
            print(f"Done. [{len(seeds)} seeds]")

        if verbose:
            print("Selecting phrases... ", end='', flush=True)
        phrases = self.__select_phrases(seeds, full_candidate_phrases)
        if verbose:
            print("Done.")

        # Remove duplicates
        phrases = set(phrases)

        # TODO: Proper Redundant Tag Removal (Paper sadly doesn't go into detail)
        to_be_removed = set()
        for phrase in phrases:
            for other in phrases:
                # Remove all phrases, for which a phrase exists, that is a strict superset
                if phrase != other and set(phrase.split(" ")).issuperset(set(other.split(" "))):
                    to_be_removed.add(other)

        for p in to_be_removed:
            phrases.remove(p)

        return sorted(phrases)
