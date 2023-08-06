from enum import Enum
from typing import Iterable, Tuple, Dict

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class Operator(Enum):
    mean = 'mean'
    sum = 'sum'
    max = 'max'


class BaseEmbeddingVectorizerMixin:
    """
    Base class for Embedding vectorizer
    Note that we implement this as vectorizer rather than transformer because we need to access the vocabulary.
    """

    def __init__(self, word2vec: dict, operator: Operator = Operator.mean, **kargs):
        # WvA: apparently we should enumerate all arguments rather than use **kargs,
        # e.g. https://github.com/scikit-learn/scikit-learn/blob/7389dba/sklearn/feature_extraction/text.py#L1493-L1509
        super().__init__(**kargs)
        self.word2vec = word2vec
        self.operator = operator if isinstance(operator, Operator) else Operator(operator)

    def fit_transform(self, X: Iterable[str], y=None):
        x = super().fit_transform(X, y).tocsr()
        return np.array(list(self._transform(x)))

    def transform(self, X: Iterable[str], y=None):
        x = super().transform(X, y).tocsr()
        return np.array(list(self._transform(x)))

    def _transform(self, x):
        dim = len(next(iter(self.word2vec.values())))
        voca = dict(_get_words(self.word2vec, self.vocabulary_))
        for doc in range(len(x.indptr) - 1):
            words = x.indices[x.indptr[doc]:x.indptr[doc + 1]]
            weights = x.data[x.indptr[doc]:x.indptr[doc + 1]]
            # select weights and vectors for known words
            vectors = [voca[w] for w in words if w in voca]
            if not vectors:
                yield np.zeros(dim)
            else:
                if self.operator == Operator.max:
                    yield np.amax(vectors, axis=0)
                else:
                    word_weights = np.array([wt for (wt, w) in zip(weights, words) if w in voca])
                    if self.operator == Operator.mean:
                        yield np.average(vectors, axis=0, weights=word_weights)
                    elif self.operator == Operator.sum:
                        yield np.sum(vectors * word_weights[:, np.newaxis], axis=0)


def _get_words(model: Dict[str, object], vocabulary: Dict[str, int]) -> Iterable[Tuple[int, object]]:
    """
    Create a mapping of word index -> word vector for the given vocabulary and model
    """
    for w, i in vocabulary.items():
        if w in model:
            yield i, model[w]


class EmbeddingCountVectorizer(BaseEmbeddingVectorizerMixin, CountVectorizer):
    """
    Vectorizer based on CountVectorizer that yields average, sum, or max word embedding per document
    """


class EmbeddingTfidfVectorizer(BaseEmbeddingVectorizerMixin, TfidfVectorizer):
    """
    Vectorizer based on CountVectorizer that yields average, sum, or max word embedding per document
    """
