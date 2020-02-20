#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import logging
import unittest
import lemminflect


class TestAuxModContract(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAuxModContract, self).__init__(*args, **kwargs)

    def checkAuxLemmas(self, lemma, infls):
        for infl in infls:
            lemmas = lemminflect.getLemma(infl, 'AUX')
            self.assertEqual(len(lemmas), 1)
            self.assertEqual(lemmas[0], lemma)

    def testAuxModalLemmas(self):
        # Modal auxilliary verbs
        self.checkAuxLemmas('can',   ['can', 'could'])
        self.checkAuxLemmas('may',   ['may', 'might'])
        self.checkAuxLemmas('will',  ['will', 'would'])
        self.checkAuxLemmas('shall', ['shall', 'should'])
        self.checkAuxLemmas('must',  ['must'])
        self.checkAuxLemmas('ought', ['ought'])
        self.checkAuxLemmas('dare',  ['dare'])
        # Auxilliary verbs
        self.checkAuxLemmas('be',    ['be', 'was', 'were', 'being', 'been', 'am', 'are', 'is'])
        self.checkAuxLemmas('do',    ['do', 'does', 'did'])
        self.checkAuxLemmas('have',  ['have', 'has', 'had'])

    # Note that d1.items() >= d2.items() is a python3 method for comparing sets
    # It is checking if every element of d2 is in d1
    def testAuxModalInflections(self):
        # Modals auxilliary verbs
        infls = lemminflect.getAllInflections('can')
        self.assertTrue(infls.items() >= {'VB': ('can',), 'VBD': ('could',)}.items())
        infls = lemminflect.getAllInflections('may')
        self.assertTrue(infls.items() >= {'VB': ('may',), 'VBD': ('might',)}.items())
        infls = lemminflect.getAllInflections('will')
        self.assertTrue(infls.items() >= {'VB': ('will',), 'VBD': ('would',)}.items())
        infls = lemminflect.getAllInflections('shall')
        self.assertTrue(infls.items() >= {'VB': ('shall',), 'VBD': ('should',)}.items())
        infls = lemminflect.getAllInflections('must')
        self.assertTrue(infls.items() >= {'VB': ('must',), 'VBD': ('must',)}.items())
        infls = lemminflect.getAllInflections('ought')
        self.assertTrue(infls.items() >= {'VB': ('ought',), 'VBD': ('ought',)}.items())
        infls = lemminflect.getAllInflections('dare')
        self.assertTrue(infls.items() >= {'VB': ('dare',)}.items())
        # Auxilliary verbs
        infls = lemminflect.getAllInflections('be')
        self.assertTrue(infls.items() >= {'VB': ('be',), 'VBD': ('was', 'were'), \
            'VBG': ('being',), 'VBN': ('been',), 'VBP': ('am', 'are'), 'VBZ': ('is',)}.items())
        # Originally coded this way but I don't think this is correct
        #infls = lemminflect.getAllInflections('do')
        #self.assertTrue(infls.items() >= {'VB': ('do', 'does'), 'VBD': ('did',)}.items())
        #infls = lemminflect.getAllInflections('have')
        #self.assertTrue(infls.items() >= {'VB': ('have', 'has'), 'VBD': ('had',), \
        #    'VBG': ('having',)}.items())

    # ["'d", "'ll", "'m", "'re", "'s", "'ve"]
    def testContractionLemmas(self):
        lemmas = lemminflect.getAllLemmas("'d")
        self.assertTrue(lemmas.items() >= {'AUX': ('will', 'have')}.items())
        lemmas = lemminflect.getAllLemmas("'ll")
        self.assertTrue(lemmas.items() >= {'AUX': ('will',)}.items())
        lemmas = lemminflect.getAllLemmas("'m")
        self.assertTrue(lemmas.items() >= {'AUX': ('be',)}.items())
        lemmas = lemminflect.getAllLemmas("'re")
        self.assertTrue(lemmas.items() >= {'AUX': ('be',)}.items())
        lemmas = lemminflect.getAllLemmas("'s")
        self.assertTrue(lemmas.items() >= {'AUX': ('be',)}.items())
        lemmas = lemminflect.getAllLemmas("'ve")
        self.assertTrue(lemmas.items() >= {'AUX': ('have',)}.items())
        lemmas = lemminflect.getAllLemmas("'ve")
        self.assertTrue(lemmas.items() >= {'AUX': ('have',)}.items())

    # At least for now, inflections don't include spellings for contractions
    # This just doesn't seem useful
    #def testContractionInflections(self):
    #    pass



if __name__ == '__main__':
    level  = logging.WARNING
    format = '[%(levelname)s %(filename)s ln=%(lineno)s] %(message)s'
    #logging.basicConfig(level=level, format=format)

    # run all methods that start with 'test'
    unittest.main()
