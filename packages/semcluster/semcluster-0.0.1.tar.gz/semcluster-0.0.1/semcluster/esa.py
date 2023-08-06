from abc import ABC, abstractmethod
import os


class ESA(ABC):
    @abstractmethod
    def measure_similarity(self, phrase1, phrase2):
        pass


class WikiESA(ESA):
    def __init__(self):
        # Only import from esa_wiki if necessary
        from esa_wiki import SemanticAnalyser
        self.analyzer = SemanticAnalyser(os.path.join(os.path.dirname(__file__), 'matrix/'))
        pass

    def measure_similarity(self, phrase1, phrase2):
        return self.analyzer.cosine_similarity(phrase1, phrase2)
