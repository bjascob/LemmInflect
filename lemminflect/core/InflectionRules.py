import re
from   ..slexicon.SKey import *
from   ..kmodels.KInfer import getKInferInstance
from   ..kmodels.ModelInflInData import ModelInflInData
from   .LexicalUtils import uposToCategory
from   lemminflect import config


# This contains a number of rules for doing simple inflections.
# These rules are derived from SPECIALIST Lexicon documentation
class MorphologyStyleModel(object):
    def __init__(self, kitype=config.kinfer_type, model_fn=config.model_infl_fn):
        self.kinfer = getKInferInstance(kitype, model_fn)
        self.output_classes = self.kinfer.getOutputEnum()

    # Get the morphology style, reg, regd or glreg
    def getStyle(self, lemma, upos):
        category = uposToCategory(upos)
        try:
            vec = ModelInflInData.wordToVec(lemma, category)
        except ValueError:
            return None
        _, style = self.kinfer.run(vec)
        return style


class InflectionRules(object):
    # Main method for creating inflections (aka variants)
    # The following keys are not handled here..
    #   irreg   : irregular forms have no rules
    #   metareg : Abreviations where plural can be 's or s
    # Verb Past/Past Particple note: for regular verbs these 2 forms are the same
    # so for now, by convention only the key PAST will be returned
    @classmethod
    def morph(cls, base, upos, infl_type):
        upos = upos.upper()
        d = {SKey.INFINATIVE:base}
        if upos == 'VERB':
            if SKey.REG == infl_type:
                forms = cls.buildRegVerb(base)
                d.update({SKey.THIRD_PRES:forms[0], SKey.PAST:forms[1], SKey.PRES_PART:forms[2]})
                return d
            elif SKey.REGD == infl_type:
                forms = cls.buildDoubledVerb(base)
                d.update({SKey.THIRD_PRES:forms[0], SKey.PAST:forms[1], SKey.PRES_PART:forms[2]})
                return d
            else:
                return d
        # Adjectives and Adverbs
        elif upos in ['ADJ', 'ADV']:
            d = {SKey.POSITIVE:base}
            if SKey.REG == infl_type:
                forms = cls.buildRegAdjAdv(base)
                d.update({SKey.COMPARATIVE:forms[0], SKey.SUPERLATIVE:forms[1]})
                return d
            elif SKey.REGD == infl_type:
                forms = cls.buildDoubledAdjAdv(base)
                d.update({SKey.COMPARATIVE:forms[0], SKey.SUPERLATIVE:forms[1]})
                return d
            else:   # infl_type in ['inv', 'inv;periph']: ==> no c/s forms, or form with more/most
                return d
        # Nouns
        elif upos == 'NOUN':
            d = {SKey.SINGULAR:base}
            if SKey.REG == infl_type:
                form = cls.buildRegNoun(base)
                d.update({SKey.PLURAL:form[0]})
                return d
            elif SKey.GLREG == infl_type:
                form = cls.buildGrecNoun(base)
                d.update({SKey.PLURAL:form[0]})
                return d
            elif infl_type in [SKey.UNCOUNT, SKey.GCOUNT, SKey.INV]:
                d.update({SKey.PLURAL:base})
                return d
            elif SKey.SING == infl_type:
                return {SKey.SINGULAR:base}
            elif SKey.PLUR == infl_type:
                return {SKey.PLURAL:base}
            else:
                return d
        else:
            return {}

    # Regular Verbs: See "The SPECIALIST Lexicon.pdf", page 8
    # returns list of [3rd_singular, past/past_participle, present_participle]
    @classmethod
    def buildRegVerb(cls, base):
        base = base.lower()
        if re.search(r'(?:[szx]|ch|sh)$', base):
            return [base+'es', base+'ed', base+'ing']
        elif re.search(r'ie$', base):
            return [base+'s', base+'d', base[:-2]+'ying']
        elif re.search(r'(ee|oe|ye)$', base):
            return [base+'s', base+'d', base+'ing']
        elif re.search(r'(?:[^aeiou])y$', base):
            b = base[:-1]
            return [b+'ies', b+'ied', b+'ying']
        elif re.search(r'(?:[^iyeo])e$', base):
            b = base[:-1]
            return [b+'es', b+'ed', b+'ing']
        else:
            return [base+'s', base+'ed', base+'ing']

    # Doubled Verbs: See "The SPECIALIST Lexicon.pdf", page 9
    # What is here assumes that for words in the lexicon we alread knows if the base word
    # is 'reg' or 'regd'.  However, note that this rule doesn't do anything to restrict
    # what words get doubled for cases where you don't know.  The above pdf describes
    # those rules and may be able to discriminate OOV words too, but this needs investigation.
    @classmethod
    def buildDoubledVerb(cls, base):
        base = base.lower()
        third = cls.buildRegVerb(base)[0]
        past = base + base[-1] + 'ed'
        pres = base + base[-1] + 'ing'
        return [third, past, pres]

    # Regular Adjectives/Adverbs: See "The SPECIALIST Lexicon.pdf", page 15
    # Note that adverbs are covered on page 17, but text says the rules are the same
    # return [comparative, superlative]
    @classmethod
    def buildRegAdjAdv(cls, base):
        base = base.lower()
        if re.search(r'(?:[^aeiou])y$', base):
            b = base[:-1]
            return [b+'ier', b+'iest']
        elif re.search(r'(?:[aeiou])y$', base):
            return [base+'er', base+'est']
        elif re.search(r'(?:[^aeiou])e$', base):
            return [base+'r', base+'st']
        else:
            return [base+'er', base+'est']

    # Doubled Adjectives/Adverbs: See "The SPECIALIST Lexicon.pdf", page 16
    @classmethod
    def buildDoubledAdjAdv(cls, base):
        base = base.lower()
        b = base + base[-1]
        return [b+'er', b+'est']

    # Regular nouns:  See "The SPECIALIST Lexicon.pdf", page 19
    # return [plural]
    @classmethod
    def buildRegNoun(cls, base):
        base = base.lower()
        if re.search(r'(?:[^aeiou])y$', base):
            return [base[:-1]+'ies']
        elif re.search(r'(?:[szx]|ch|sh)$', base):
            return [base+'es']
        else:
            return [base + 's']

    # Greco-latin nouns:  See "The SPECIALIST Lexicon.pdf", page 20
    # return [plural]
    @classmethod
    def buildGrecNoun(cls, base):
        base = base.lower()
        if re.search(r'us$', base):
            return [base[:-2] + 'i']
        elif re.search(r'ma$', base):
            return [base[:-2] + 'mata']
        elif re.search(r'a$', base):
            return [base[:-1] + 'ae']
        elif re.search(r'um$', base):
            return [base[:-2] + 'a']
        elif re.search(r'on$', base):
            return [base[:-2] + 'a']
        elif re.search(r'sis$', base):
            return [base[:-3] + 'ses']
        elif re.search(r'is$', base):
            return [base[:-2] + 'ides']
        elif re.search(r'men$', base):
            return [base[:-3] + 'mina']
        elif re.search(r'ex$', base):
            return [base[:-2] + 'ices']
        elif re.search(r'x$', base):
            return [base[:-1] + 'ces']
        else:
            return cls.buildRegNoun(base)
