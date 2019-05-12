#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import logging
import unittest
import numpy
from   lemminflect.core.LemmatizerRules import LemmatizerRules
from   lemminflect.core.Lemmatizer import Lemmatizer


class LemmatizerRulesTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(LemmatizerRulesTests, self).__init__(*args, **kwargs)

    def getTestCases(self):
        tests = []
        tests.append( ('abases', 'VERB', 'abase') )
        tests.append( ('abbreviating', 'VERB', 'abbreviate') )
        tests.append( ('abdications', 'NOUN', 'abdication') )
        tests.append( ('abscissae', 'NOUN', 'abscissa' ) )
        tests.append( ('achier', 'ADJ', 'achy') )
        return tests

    def testNumpyInfer(self):
        oov_lemmatizer = LemmatizerRules(kitype='numpy')
        tests = self.getTestCases()
        for test in tests:
            lemma = oov_lemmatizer.lemmatize( test[0], test[1] )
            self.assertEqual(lemma, test[2])

    def testKerasInfer(self):
        # In my code I see a bunch of warnings from numpy when running keras, but only
        # inside the unittest, not during normal operation.
        numpy.warnings.filterwarnings('ignore')
        oov_lemmatizer = LemmatizerRules(kitype='keras')
        tests = self.getTestCases()
        for test in tests:
            lemma = oov_lemmatizer.lemmatize( test[0], test[1] )
            self.assertEqual(lemma, test[2])

    def testLemmatizer01(self):
        lemmatizer = Lemmatizer()
        tests = self.getTestCases()
        for test in tests:
            lemma_dict = lemmatizer.getAllLemmasOOV( test[0], test[1] )
            self.assertTrue( test[1] in lemma_dict )
            lemmas = lemma_dict[test[1]]
            self.assertEqual(len(lemmas), 1)
            lemma = lemmas[0]
            self.assertEqual(lemma, test[2])

    def testLemmatizer02(self):
        lemmatizer = Lemmatizer()
        with self.assertLogs():
            lemma_dict = lemmatizer.getAllLemmasOOV( 'test', 'X' )
        self.assertEqual(len(lemma_dict), 0)


if __name__ == '__main__':
    level  = logging.WARNING
    format = '[%(levelname)s %(filename)s ln=%(lineno)s] %(message)s'
    #logging.basicConfig(level=level, format=format)

    # run all methods that start with 'test'
    unittest.main()
