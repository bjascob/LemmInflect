#import logging
from   ..kmodels.ModelLemmaInData import ModelLemmaInData
from   ..kmodels.KInfer           import getKInferInstance
from   .LexicalUtils              import uposToCategory
from   .. import config


class LemmatizerRules(object):
    def __init__(self, kitype=config.kinfer_type, model_fn=config.model_lemma_fn):
        self.kinfer = getKInferInstance(kitype, model_fn)
        self.rules = self.kinfer.getOutputEnum()

    def lemmatize(self, word, upos):
        category = uposToCategory(upos)
        try:
            vec = ModelLemmaInData.wordToVec(word, category)
        except ValueError:
            return None
        rnum, _ = self.kinfer.run(vec)
        lemma = self._applyRule(word, rnum)
        return lemma

    # Apply a rule to an inflection
    def _applyRule(self, inflection, rnum):
        rule = self.rules[rnum]
        il_rm, ll_add, is_double = self._csvToTuple(rule)
        # Remove characters
        rm_len = len(il_rm)
        if il_rm:
            if il_rm != inflection[-rm_len:]:
                #logging.warning('ending differs from rule: %s / %s' % (inflection, il_rm))
                pass # it may be fairly common that the model picks a class that isn't valid
            lemma = inflection[:-rm_len]
        else:
            lemma = inflection
        # Add back on letters
        lemma += ll_add
        # Apply double letter if needed
        if is_double == 'True':
            lemma = lemma[:-1]
        return lemma

    # Convert the rule csv string to a tuple
    @staticmethod
    def _csvToTuple(line):
        t = line.split(',')
        if len(t) != 3:
            raise ValueError('Invalid line: %s' % str(t))
        return t
