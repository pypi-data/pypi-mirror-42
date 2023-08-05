import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter('ignore')

from itertools import product
from collections import defaultdict, Counter
from fuzzywuzzy import fuzz
import numpy as np
import pulp
from scipy.spatial.distance import euclidean
from .texts._text_functions import normalizer_textcleaning
from .texts._tatabahasa import (
    rules_normalizer,
    consonants,
    vowels,
    sounds,
    GO,
    PAD,
    EOS,
    UNK,
)
from .spell import _return_possible, _edit_normalizer, _return_known
from .similarity import is_location


def _tokens_to_fracdict(tokens):
    cntdict = defaultdict(lambda: 0)
    for token in tokens:
        cntdict[token] += 1
    totalcnt = sum(cntdict.values())
    return {token: float(cnt) / totalcnt for token, cnt in cntdict.items()}


def _word_mover(left_token, right_token, vectorizer):
    all_tokens = list(set(left_token + right_token))
    wordvecs = {
        token: vectorizer.get_vector_by_name(token) for token in all_tokens
    }
    left_bucket = _tokens_to_fracdict(left_token)
    right_bucket = _tokens_to_fracdict(right_token)

    T = pulp.LpVariable.dicts(
        'T_matrix', list(product(all_tokens, all_tokens)), lowBound = 0
    )
    prob = pulp.LpProblem('WMD', sense = pulp.LpMinimize)
    prob += pulp.lpSum(
        [
            T[token1, token2] * euclidean(wordvecs[token1], wordvecs[token2])
            for token1, token2 in product(all_tokens, all_tokens)
        ]
    )
    for token2 in right_bucket:
        prob += (
            pulp.lpSum([T[token1, token2] for token1 in left_bucket])
            == right_bucket[token2]
        )
    for token1 in left_bucket:
        prob += (
            pulp.lpSum([T[token1, token2] for token2 in right_bucket])
            == left_bucket[token1]
        )
    prob.solve()
    return prob


def distance(left_token, right_token, vectorizer):
    """
    calculate word mover distance between left hand-side sentence and right hand-side sentence

    Parameters
    ----------
    left_token : list
        Eg, ['saya','suka','makan','ayam']
    right_token : list
        Eg, ['saya','suka','makan','ikan']
    vectorizer : object
        fast-text or word2vec interface object

    Returns
    -------
    distance: float
    """
    assert isinstance(left_token, list), 'left_token must be a list'
    assert isinstance(right_token, list), 'right_token must be a list'
    assert hasattr(
        vectorizer, 'get_vector_by_name'
    ), 'vectorizer must has `get_vector_by_name` method'
    prob = _word_mover(left_token, right_token, vectorizer)
    return pulp.value(prob.objective)


class _DEEP_CONTRACTION:
    def __init__(self, corpus, vectorizer):
        self.corpus = Counter(corpus)
        self.vectorizer = vectorizer

    def _suggest(self, string):
        """
        Normalize a string

        Parameters
        ----------
        string : str

        debug : bool, optional (default=True)
            If true, it will print character similarity distances.

        Returns
        -------
        string: normalized string
        """
        assert isinstance(string, str), 'input must be a string'
        result, outer_candidates = [], []
        for word in normalizer_textcleaning(string).split():
            if word.istitle():
                result.append(word)
                continue
            if len(string) > 2:
                if string[-2] in consonants and string[-1] == 'e':
                    string[-1] = 'a'
            if word[0] == 'x' and len(word) > 1:
                result_string = 'tak '
                word = word[1:]
            else:
                result_string = ''
            if word[-2:] == 'la':
                end_result_string = ' lah'
                word = word[:-2]
            elif word[-3:] == 'lah':
                end_result_string = ' lah'
                word = word[:-3]
            else:
                end_result_string = ''
            if word in sounds:
                result.append(result_string + sounds[word] + end_result_string)
                continue
            if word in rules_normalizer:
                result.append(
                    result_string + rules_normalizer[word] + end_result_string
                )
                continue
            if word in self.corpus:
                result.append(result_string + word + end_result_string)
                continue
            candidates = (
                _return_known([word], self.corpus)
                or _return_known(_edit_normalizer(word), self.corpus)
                or _return_possible(word, self.corpus, _edit_normalizer)
                or [word]
            )
            candidates = list(candidates)
            candidates = [
                (candidate, is_location(candidate))
                for candidate in list(candidates)
            ]
            strings = [fuzz.ratio(string, k[0]) for k in candidates]
            descending_sort = np.argsort(strings)[::-1]
            selected = None
            for index in descending_sort:
                if not candidates[index][1]:
                    selected = candidates[index][0]
                    break
            selected = (
                candidates[descending_sort[0]][0] if not selected else selected
            )
            result.append(result_string + word + end_result_string)
            outer_candidates.append([(word, k[0]) for k in candidates])
        return ' '.join(result), outer_candidates

    def expand(self, string):
        result, candidates = self._suggest(string)
        intermediates = []
        for candidate in candidates:
            inner = []
            for c in candidate:
                text = [c[1] if w in c[0] else w for w in result.split()]
                inner.append(
                    (
                        c[0],
                        ' '.join(text),
                        distance(text, result.split(), self.vectorizer),
                    )
                )
            inner.sort(key = lambda x: x[2])
            intermediates.append(inner)
        return intermediates


def expander(corpus, vectorizer):
    assert isinstance(corpus, list) and isinstance(
        corpus[0], str
    ), 'input must be list of strings'
    assert hasattr(
        vectorizer, 'get_vector_by_name'
    ), 'vectorizer must has `get_vector_by_name` method'
    return _DEEP_CONTRACTION(corpus, vectorizer)
