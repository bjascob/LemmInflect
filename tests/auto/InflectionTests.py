#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import logging
import unittest
import spacy
import lemminflect


# UnitTest creates a separate instance of the class for each test in it.
# Interestingly, the init time doesn't seem to get counted towards the total testing time.
# To avoid calling load multiple times, load in globally and reference it in __init__
# Since lemminflect uses singletons, this isn't an issue with getAllLemmas, etc..
SPACY_NLP = spacy.load('en_core_web_sm')


class InflectionTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InflectionTests, self).__init__(*args, **kwargs)
        self.nlp = SPACY_NLP
        lemminflect.Inflections().setUseInternalLemmatizer(True)   # lemmatize with lemminflect

    def testSpacyInflect01(self):
        sent = 'I seem to be eating.'
        doc = self.nlp(sent)
        self.assertEqual(doc[0]._.inflect('PRP', inflect_oov=False, on_empty_ret_word=False), None)
        self.assertEqual(doc[0]._.inflect('PRP', inflect_oov=False, on_empty_ret_word=True), 'I')

        self.assertEqual(doc[1]._.inflect('VBN'), 'seemed')
        self.assertEqual(doc[1]._.inflect('VBD'), 'seemed')
        self.assertEqual(doc[1]._.inflect('VBG'), 'seeming')
        self.assertEqual(doc[1]._.inflect('VBZ'), 'seems')
        self.assertEqual(doc[1]._.inflect('VBP'), 'seem')
        self.assertEqual(doc[1]._.inflect('VB'),  'seem')

        self.assertEqual(doc[2]._.inflect('VB', inflect_oov=False, on_empty_ret_word=False),  None)

        self.assertEqual(doc[3]._.inflect('VB'),  'be')
        self.assertEqual(doc[3]._.inflect('VBD', 0), 'was')
        self.assertEqual(doc[3]._.inflect('VBD', 1), 'were')
        self.assertEqual(doc[3]._.inflect('VBN'), 'been')
        self.assertEqual(doc[3]._.inflect('VBG'), 'being')
        self.assertEqual(doc[3]._.inflect('VBP', 0),  'am')
        self.assertEqual(doc[3]._.inflect('VBP', 1), 'are')
        self.assertEqual(doc[3]._.inflect('VBZ'), 'is')

        self.assertEqual(doc[4]._.inflect('VBN'), 'eaten')
        self.assertEqual(doc[4]._.inflect('VBD'), 'ate')
        self.assertEqual(doc[4]._.inflect('VBG'), 'eating')
        self.assertEqual(doc[4]._.inflect('VBZ'), 'eats')
        self.assertEqual(doc[4]._.inflect('VBP'), 'eat')
        self.assertEqual(doc[4]._.inflect('VB'),  'eat')

    def testSpacyInflect02(self):
        lemminflect.Inflections().setUseInternalLemmatizer(False) # lemmatize with spaCy
        self.testSpacyInflect01()

    def testGetInfections01(self):
        # Note this test may be a big problematic as the overrides file may change
        # VBN: awoken to awaked
        awake_dict = {'VBD': ('awoke',), 'VBN': ('awoken',), 'VBG': ('awaking',),
            'VBZ': ('awakes',), 'VB': ('awake',), 'VBP': ('awake',)}
        #awake_dict['VBN'] = ('awaked',)     # Applied in overrides but isn't preferred
        self.assertEqual(lemminflect.getAllInflections('awake', 'VERB'), awake_dict)
        self.assertEqual(lemminflect.getAllInflections('awoke', 'VERB'), {})
        with self.assertLogs():
            infls = lemminflect.getAllInflections('awake', 'X') # invalid upos
        self.assertEqual(infls, {})

    def testGetInflection02(self):
        self.assertEqual(lemminflect.getInflection('squirrel', 'NN'),  ('squirrel',))
        self.assertEqual(lemminflect.getInflection('squirrel', 'NNS'), ('squirrels', 'squirrel'))

    def testGetInflection03(self):
        self.assertEqual(lemminflect.getAllInflections('watch'),
            {'NNS': ('watches', 'watch'), 'NN': ('watch',), 'VBD': ('watched',),
            'VBG': ('watching',), 'VBZ': ('watches',), 'VB': ('watch',), 'VBP': ('watch',)})
        self.assertEqual(lemminflect.getAllInflections('watch', 'VERB'),
            {'VBD': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',),
             'VB': ('watch',), 'VBP': ('watch',)})
        self.assertEqual(lemminflect.getInflection('watch', 'VBD'), ('watched',))
        self.assertEqual(lemminflect.getAllInflections('watch', 'ADJ'), {})

    # Verifies that data is not getting deleted from the main repo when filtering for a specific tag
    def testGetInflection04(self):
        self.assertEqual(lemminflect.getAllInflections('watch', 'ADJ'), {})
        self.assertEqual(lemminflect.getInflection('watch', 'JJ', inflect_oov=False), ())
        self.assertEqual(lemminflect.getInflection('watch', 'JJ', inflect_oov=True), ('watch',))
        self.assertEqual(lemminflect.getInflection('watch', 'VBD'), ('watched',))

    def testCapitalization01(self):
        doc = self.nlp('BRAd Is STANDING.')
        self.assertEqual(doc[0]._.inflect('NN', inflect_oov=True), 'Brad')
        self.assertEqual(doc[1]._.inflect('VB'), 'Be')
        self.assertEqual(doc[2]._.inflect('VB'), 'STAND')

    def testProperNouns(self):
        infls = lemminflect.getInflection('Alaskan', 'NN', inflect_oov=False)
        self.assertEqual(len(infls), 0 )
        infls = lemminflect.getInflection('Alaskan', 'NNP', inflect_oov=False)
        self.assertEqual(len(infls), 1 )
        self.assertEqual(infls[0], 'Alaskan')
        infls = lemminflect.getInflection('Alaskan', 'NNPS', inflect_oov=False)
        self.assertEqual(len(infls), 1 )
        self.assertEqual(infls[0], 'Alaskans')
        infls = lemminflect.getInflection('Axxlaskan', 'NNP', inflect_oov=True)
        self.assertEqual(len(infls), 1 )
        self.assertEqual(infls[0], 'Axxlaskan')
        infls = lemminflect.getInflection('Axxlaskan', 'NNPS', inflect_oov=True)
        self.assertEqual(len(infls), 1 )
        self.assertEqual(infls[0], 'Axxlaskans')
        lemminflect.Inflections().setUseInternalLemmatizer(True)   # lemmatize with lemminflect
        token = self.nlp('The Alaskan went South.')[1]
        self.assertEqual(token._.inflect('NNPS', inflect_oov=False), 'Alaskans')
        token = self.nlp('The Axxlaskan went South.')[1]
        self.assertEqual(token._.inflect('NNPS', inflect_oov=True), 'Axxlaskans')

    def testOverrides(self):
        # run the inflection system once to assure the overrides is loaded (ie.. lazy loading)
        lemminflect.getInflection('watch', 'VBD'), ('watched',)
        # Hack the code to replace the overrides dictionary
        orig_dict = lemminflect.Inflections().overrides_dict
        with self.assertLogs():
            lemmas = lemminflect.getLemma('WORD', 'X')
        self.assertEqual(lemmas, ())
        with self.assertLogs():
            lemmas = lemminflect.getAllLemmas('WORD', 'X')
        self.assertEqual(lemmas, {})
        with self.assertLogs():
            lemmas = lemminflect.getAllLemmasOOV('WORD', 'X')
        self.assertEqual(lemmas, {})
        token = self.nlp('I')[0]
        self.assertEqual(token._.lemma(), 'I')
        lemminflect.Inflections().overrides_dict = {'watch':{'VBD':('xxx',)}}
        inflections = lemminflect.getInflection('watch', 'VBD', inflect_oov=False)
        self.assertEqual(inflections, ('xxx',))
        # put the original dictionary back
        lemminflect.Inflections().overrides_dict = orig_dict

    def testUPOSLog(self):
        with self.assertLogs():
            infl = lemminflect.getInflection('WORD', 'X')
        self.assertEqual(infl, ())
        with self.assertLogs():
            infls = lemminflect.getAllInflections('WORD', 'X')
        self.assertEqual(infls, {})
        with self.assertLogs():
            infls = lemminflect.getAllInflectionsOOV('WORD', 'X')
        self.assertEqual(infls, {})
        token = self.nlp('testing')[0]
        self.assertEqual(token._.inflect('X'), 'testing')


if __name__ == '__main__':
    level  = logging.WARNING
    format = '[%(levelname)s %(filename)s ln=%(lineno)s] %(message)s'
    logging.basicConfig(level=level, format=format)

    # run all methods that start with 'test'
    unittest.main()
