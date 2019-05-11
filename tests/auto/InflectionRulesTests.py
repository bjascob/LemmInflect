#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import unittest
import lemminflect
from   lemminflect.core.InflectionRules import InflectionRules
from   lemminflect.slexicon.SKey import *


# Helper to form test cases
class TestCase(object):
    def __init__(self, base, upos, infl_type):
        self.base      = base
        self.upos      = upos
        self.infl_type = infl_type
        self.forms     = {}

    @classmethod
    def formVerb(cls, infl_type, base, third_pres, past_part, pres_part):
        self = cls(base, 'VERB', infl_type)
        self.forms = {SKey.INFINATIVE:base, SKey.THIRD_PRES:third_pres, \
                       SKey.PAST:past_part, SKey.PRES_PART:pres_part}
        return self
    @classmethod
    def formAdj(cls, infl_type, base, comparative, superlative):
        self = cls(base, 'ADJ', infl_type)
        self.forms = {SKey.POSITIVE:base, SKey.COMPARATIVE:comparative, SKey.SUPERLATIVE:superlative}
        return self

    @classmethod
    def formNoun(cls, infl_type, base, plural):
        self = cls(base, 'NOUN', infl_type)
        self.forms = {SKey.SINGULAR:base, SKey.PLURAL:plural }
        return self

    # Verify that all words in this class are in the forms_dict but don't look at the tags
    def inflectionsInDict(self, form_dict, form_num=0):
        self_spells = set(self.forms.values())
        test_spells = []
        for spell in form_dict.values():
            test_spells += spell
        test_spells = set(test_spells)
        return self_spells.issubset(test_spells)

class InflectionRulesTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InflectionRulesTests, self).__init__(*args, **kwargs)

    def runTestCasesWithMorph(self, tests):
        for test in tests:
            infl_forms = InflectionRules.morph(test.base, test.upos, test.infl_type)
            self.assertEqual(infl_forms, test.forms)

    #### The test cases below call into InflectionRules.morph directly
    #### Calls into InflectionRules use upos (ie.. NOUN,..) and infl_types like SKey.SINGULAR
    #### These are the SPECIALIST Lexicon fields

    def testRegularVerbs(self):
        tests = []
        tests.append( TestCase.formVerb(SKey.REG, 'dismiss', 'dismisses', 'dismissed','dismissing') )
        tests.append( TestCase.formVerb(SKey.REG, 'waltz', 'waltzes', 'waltzed', 'waltzing') )
        tests.append( TestCase.formVerb(SKey.REG, 'index', 'indexes', 'indexed', 'indexing') )
        tests.append( TestCase.formVerb(SKey.REG, 'detach', 'detaches', 'detached', 'detaching') )
        tests.append( TestCase.formVerb(SKey.REG, 'distinguish', 'distinguishes', 'distinguished', 'distinguishing') )
        tests.append( TestCase.formVerb(SKey.REG, 'tie', 'ties', 'tied', 'tying') )
        tests.append( TestCase.formVerb(SKey.REG, 'agree', 'agrees', 'agreed', 'agreeing') )
        tests.append( TestCase.formVerb(SKey.REG, 'canoe', 'canoes', 'canoed', 'canoeing') )
        tests.append( TestCase.formVerb(SKey.REG, 'dye', 'dyes', 'dyed', 'dyeing') )
        tests.append( TestCase.formVerb(SKey.REG, 'dry', 'dries', 'dried', 'drying') )
        tests.append( TestCase.formVerb(SKey.REG, 'love', 'loves', 'loved', 'loving') )
        tests.append( TestCase.formVerb(SKey.REG, 'talk', 'talks', 'talked', 'talking') )
        self.runTestCasesWithMorph(tests)

    def testDoubledVerbs(self):
        tests = []
        tests.append( TestCase.formVerb(SKey.REGD, 'ban', 'bans', 'banned','banning') )
        tests.append( TestCase.formVerb(SKey.REGD, 'cancel', 'cancels', 'cancelled','cancelling') )
        tests.append( TestCase.formVerb(SKey.REGD, 'clog', 'clogs', 'clogged','clogging') )
        self.runTestCasesWithMorph(tests)

    def testRegularAdjs(self):
        tests = []
        tests.append( TestCase.formAdj(SKey.REG, 'brainy', 'brainier', 'brainiest') )
        tests.append( TestCase.formAdj(SKey.REG, 'gray', 'grayer', 'grayest') )
        tests.append( TestCase.formAdj(SKey.REG, 'fine', 'finer', 'finest') )
        tests.append( TestCase.formAdj(SKey.REG, 'clear', 'clearer', 'clearest') )
        self.runTestCasesWithMorph(tests)

    def testDoubledAdjs(self):
        tests = []
        tests.append( TestCase.formAdj(SKey.REGD, 'dim', 'dimmer', 'dimmest') )
        tests.append( TestCase.formAdj(SKey.REGD, 'fit', 'fitter', 'fittest') )
        tests.append( TestCase.formAdj(SKey.REGD, 'sad', 'sadder', 'saddest') )
        self.runTestCasesWithMorph(tests)

    def testRegularNoun(self):
        tests = []
        tests.append( TestCase.formNoun(SKey.REG, 'fly', 'flies') )
        tests.append( TestCase.formNoun(SKey.REG, 'illness', 'illnesses') )
        tests.append( TestCase.formNoun(SKey.REG, 'waltz', 'waltzes') )
        tests.append( TestCase.formNoun(SKey.REG, 'box', 'boxes') )
        tests.append( TestCase.formNoun(SKey.REG, 'match', 'matches') )
        tests.append( TestCase.formNoun(SKey.REG, 'splash', 'splashes') )
        tests.append( TestCase.formNoun(SKey.REG, 'book', 'books') )
        self.runTestCasesWithMorph(tests)

    def testNounGLReg(self):
        tests = []
        tests.append( TestCase.formNoun(SKey.GLREG, 'focus', 'foci') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'trauma', 'traumata') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'larva', 'larvae') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'ilium', 'ilia') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'taxon', 'taxa') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'analysis', 'analyses') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'cystis', 'cystides') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'foramen', 'foramina') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'index', 'indices') )
        tests.append( TestCase.formNoun(SKey.GLREG, 'matrix', 'matrices') )
        self.runTestCasesWithMorph(tests)

    #### The test cases below call into lemminflect,getAllInflectionsOOV
    #### Calls into this methods uses upos = VERB,... and returns the PennTreebank tag
    #### This is the external facing API

    def testUPosException(self):
        self.assertEqual(lemminflect.getAllInflectionsOOV('test', 'X'), {})

    def testCapitalization(self):
        tests = []
        tests.append( TestCase.formVerb(SKey.REG, 'DISmiss', 'Dismisses', 'Dismissed','Dismissing') )
        tests[-1].forms[SKey.INFINATIVE] = 'Dismiss' # override InflTestHelper's so test is correct
        tests.append( TestCase.formAdj(SKey.REG, 'Brainy', 'Brainier', 'Brainiest') )
        tests.append( TestCase.formNoun(SKey.REG, 'FLY', 'FLIES',) )
        for word in tests:
            infl_dict = lemminflect.getAllInflectionsOOV(word.base, word.upos)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.base, word.forms, infl_dict)
            self.assertTrue(word.inflectionsInDict(infl_dict), msg)

    def testGetInflectionOOV(self):
        self.assertEqual(lemminflect.getInflection('xxbike',    'NN',  inflect_oov=False), ())
        self.assertEqual(lemminflect.getInflection('xxbike',    'NNS', inflect_oov=False), ())
        self.assertEqual(lemminflect.getInflection('xxbike',    'NN',  inflect_oov=True), ('xxbike',))         # reg
        self.assertEqual(lemminflect.getInflection('xxbike',    'NNS', inflect_oov=True), ('xxbikes',))        # reg
        self.assertEqual(lemminflect.getInflection('xxbaggy',   'JJR', inflect_oov=True), ('xxbaggier',))      # reg
        self.assertEqual(lemminflect.getInflection('xxclean',   'RBS', inflect_oov=True), ('xxcleanest',))     # reg
        self.assertEqual(lemminflect.getInflection('xxformat',  'VBG', inflect_oov=True), ('xxformatting',))   # regd
        self.assertEqual(lemminflect.getInflection('xxbacklog', 'VBD', inflect_oov=True), ('xxbacklogged',))   # regd
        self.assertEqual(lemminflect.getInflection('xxgenesis', 'NNS', inflect_oov=True), ('xxgeneses',))      # glreg
        self.assertEqual(lemminflect.getInflection('xxalumus',  'NNS', inflect_oov=True), ('xxalumi',))        # glreg


if __name__ == '__main__':
    # run all methods that start with 'test'
    unittest.main()
