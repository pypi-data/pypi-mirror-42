from typing import Any, List, Callable, TypeVar, Iterable, Dict, Optional, Tuple
from functools import reduce
from operator import iconcat
import numpy as np

T = TypeVar("T")
U = TypeVar("U")


def split_list(list: List[T], is_delimiter: Callable[[T], bool], keep_empty = False) -> List[List[T]]:
    sublists = []
    current_sublist = None
    for element in list:
        if is_delimiter(element):
            if current_sublist is not None:
                if keep_empty or len(current_sublist) > 0:
                    sublists.append(current_sublist)
                current_sublist = None
        else:
            if current_sublist is None:
                current_sublist = []
            current_sublist.append(element)

    if current_sublist is not None:
        sublists.append(current_sublist)

    return sublists


def flatten(l: Iterable[List[T]]) -> List[T]:
    return reduce(iconcat, l, [])


def pairwise_similarity(x: List[T], metric: Callable[[T, T], float]) -> np.ndarray:
    """
    Computes the pairwise similarity for all elements in the given list with the given similarity measure.
    metric(x, x) is required to be 1.

    :param x: Elements
    :param metric: Similarity measure with metric(x, x) == 1
    :return: Pairwise similarity matrix
    """
    # Halve the diagonal, as it is added to itself at the end
    dist_matrix = np.zeros((len(x), len(x)))
    for i in range(1, len(x)):
        # Only fill lower triangle
        for j in range(i):
            dist_matrix[i, j] = metric(x[i], x[j])
    # Copy lower triangle to upper triangle
    return dist_matrix + dist_matrix.T


def groupby(x: Iterable[T], key: Callable[[T], U]) -> Dict[U, List[T]]:
    result = {}
    for v in x:
        k = key(v)
        if k not in result:
            result[k] = []
        result[k].append(v)

    return result


def subsequence_index(source: List[T], subsequence: List[T]) -> Optional[int]:
    for i in range(0, len(source) - len(subsequence)):
        for j in range(0, len(subsequence)):
            if source[i + j] != subsequence[j]:
                break
        else:
            return i
    return None
