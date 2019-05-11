import numpy
from   ..codecs.LemmaTCorpFileCodec import LemmaTCorpFileCodec
from   ..slexicon.SKey import *


class ModelLemmaInData(object):
    WVEC_LEN       = 9      # keep 8 letters from the lemma + 1 for the category
    MAX_LETTER_IDX = 28     # a-z plus <oov> and <>
    def __init__(self, fn):
        self.entries = LemmaTCorpFileCodec.load(fn)

    # Lower-case the word and turn it arround (so the last char is always in position 0)
    # Empty characters are labeled 0, characters not a-z are labeled 1
    @classmethod
    def wordToVec(cls, word, category):
        vec = numpy.zeros(shape=(cls.WVEC_LEN, cls.MAX_LETTER_IDX), dtype='float32')
        word = list(word.lower())[::-1]     # lower-case, list, inverted-order
        for i, letter in enumerate(word):
            if i >= cls.WVEC_LEN-1:
                break
            val = ord(letter)
            one_hot = val-95 if val>=97 and val<=122 else 1
            vec[i+1, one_hot] = 1
        # Now prepend the category one-hot
        if category == SKey.NOUN:
            vec[0, 0] = 1
        elif category == SKey.VERB:
            vec[0, 1] = 1
        elif category == SKey.ADJ:
            vec[0, 2] = 1
        elif category == SKey.ADV:
            vec[0, 3] = 1
        else:
            raise ValueError('Unhandled category: %s' % category)
        return vec

    # Input letters classes
    @staticmethod
    def getLetterClasses():
        classes = ['<>', '<oov>'] + [chr(i) for i in range(97,123)]
        return classes
