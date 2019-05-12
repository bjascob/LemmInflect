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


class LemmatizerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(LemmatizerTests, self).__init__(*args, **kwargs)
        self.nlp = SPACY_NLP

    def runGetAllLemmasTests(self, tests):
        for test in tests:
            base, upos, form = test
            lemmas = lemminflect.getAllLemmas(form, upos).get(upos, {})
            self.assertTrue(base in set(lemmas), msg='base=%s  lemmas=%s'% (base, str(lemmas)))

    def runGetLemmaTests(self, tests):
        for test in tests:
            base, upos, form = test
            lemmas = lemminflect.getLemma(form, upos)
            self.assertTrue(base in set(lemmas), msg='base=%s  lemmas=%s'% (base, str(lemmas)))

    def testRegularVerbs(self):
        tests = []
        tests.append( ('dismiss', 'VERB', 'dismiss') )
        tests.append( ('dismiss', 'VERB', 'dismisses') )
        tests.append( ('dismiss', 'VERB', 'dismissed') )
        tests.append( ('dismiss', 'VERB', 'dismissing') )
        tests.append( ('waltz', 'VERB', 'waltz') )
        tests.append( ('waltz', 'VERB', 'waltzes') )
        tests.append( ('waltz', 'VERB', 'waltzed') )
        tests.append( ('waltz', 'VERB', 'waltzing') )
        tests.append( ('index', 'VERB', 'index') )
        tests.append( ('index', 'VERB', 'indexes') )
        tests.append( ('index', 'VERB', 'indexed') )
        tests.append( ('index', 'VERB', 'indexing') )
        tests.append( ('detach', 'VERB', 'detach') )
        tests.append( ('detach', 'VERB', 'detaches') )
        tests.append( ('detach', 'VERB', 'detached') )
        tests.append( ('detach', 'VERB', 'detaching') )
        tests.append( ('distinguish', 'VERB', 'distinguish') )
        tests.append( ('distinguish', 'VERB', 'distinguishes') )
        tests.append( ('distinguish', 'VERB', 'distinguished') )
        tests.append( ('distinguish', 'VERB', 'distinguishing') )
        tests.append( ('tie', 'VERB', 'tie') )
        tests.append( ('tie', 'VERB', 'ties') )
        tests.append( ('tie', 'VERB', 'tied') )
        tests.append( ('tie', 'VERB', 'tying') )
        tests.append( ('agree', 'VERB', 'agree') )
        tests.append( ('agree', 'VERB', 'agrees') )
        tests.append( ('agree', 'VERB', 'agreed') )
        tests.append( ('agree', 'VERB', 'agreeing') )
        tests.append( ('canoe', 'VERB', 'canoe') )
        tests.append( ('canoe', 'VERB', 'canoes') )
        tests.append( ('canoe', 'VERB', 'canoed') )
        tests.append( ('canoe', 'VERB', 'canoeing') )
        tests.append( ('dye', 'VERB', 'dyes') )
        tests.append( ('dye', 'VERB', 'dye') )
        tests.append( ('dye', 'VERB', 'dyed') )
        tests.append( ('dye', 'VERB', 'dyeing') )
        tests.append( ('dry', 'VERB', 'dry') )
        tests.append( ('dry', 'VERB', 'dries') )
        tests.append( ('dry', 'VERB', 'dried') )
        tests.append( ('dry', 'VERB', 'drying') )
        tests.append( ('love', 'VERB', 'love') )
        tests.append( ('love', 'VERB', 'loves') )
        tests.append( ('love', 'VERB', 'loved') )
        tests.append( ('love', 'VERB', 'loving') )
        tests.append( ('talk', 'VERB', 'talks') )
        tests.append( ('talk', 'VERB', 'talked') )
        tests.append( ('talk', 'VERB', 'talking') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testDoubledVerbs(self):
        tests = []
        tests.append( ('ban', 'VERB', 'ban') )
        tests.append( ('ban', 'VERB', 'bans') )
        tests.append( ('ban', 'VERB', 'banned') )
        tests.append( ('ban', 'VERB', 'banning') )
        tests.append( ('cancel', 'VERB', 'cancel') )
        tests.append( ('cancel', 'VERB', 'cancels') )
        tests.append( ('cancel', 'VERB', 'cancelled') )
        tests.append( ('cancel', 'VERB', 'cancelling') )
        tests.append( ('clog', 'VERB', 'clog') )
        tests.append( ('clog', 'VERB', 'clogs') )
        tests.append( ('clog', 'VERB', 'clogged') )
        tests.append( ('clog', 'VERB', 'clogging') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testRegularAdjs(self):
        tests = []
        tests.append( ('brainy', 'ADJ', 'brainy') )
        tests.append( ('brainy', 'ADJ', 'brainier') )
        tests.append( ('brainy', 'ADJ', 'brainiest') )
        tests.append( ('gray', 'ADJ', 'gray') )
        tests.append( ('gray', 'ADJ', 'grayer') )
        tests.append( ('gray', 'ADJ', 'grayest') )
        tests.append( ('fine', 'ADJ', 'fine') )
        tests.append( ('fine', 'ADJ', 'finer') )
        tests.append( ('fine', 'ADJ', 'finest') )
        tests.append( ('clear', 'ADJ', 'clear') )
        tests.append( ('clear', 'ADJ', 'clearer') )
        tests.append( ('clear', 'ADJ', 'clearest') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testDoubledAdjs(self):
        tests = []
        tests.append( ('dim', 'ADJ', 'dim') )
        tests.append( ('dim', 'ADJ', 'dimmer') )
        tests.append( ('dim', 'ADJ', 'dimmest') )
        tests.append( ('fit', 'ADJ', 'fit') )
        tests.append( ('fit', 'ADJ', 'fitter') )
        tests.append( ('fit', 'ADJ', 'fittest') )
        tests.append( ('sad', 'ADJ', 'sad') )
        tests.append( ('sad', 'ADJ', 'sadder') )
        tests.append( ('sad', 'ADJ', 'saddest') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testRegularNoun(self):
        tests = []
        tests.append( ('advance', 'NOUN', 'advance') )   # Note has multiple spellings
        tests.append( ('advance', 'NOUN', 'advances') )  # Note has multiple spellings
        tests.append( ('fly', 'NOUN', 'fly') )
        tests.append( ('fly', 'NOUN', 'flies') )
        tests.append( ('illness', 'NOUN', 'illness') )
        tests.append( ('illness', 'NOUN', 'illnesses') )
        tests.append( ('waltz', 'NOUN', 'waltz') )
        tests.append( ('waltz', 'NOUN', 'waltzes') )
        tests.append( ('box', 'NOUN', 'box') )
        tests.append( ('box', 'NOUN', 'boxes') )
        tests.append( ('match', 'NOUN', 'match') )
        tests.append( ('match', 'NOUN', 'matches') )
        tests.append( ('splash', 'NOUN', 'splash') )
        tests.append( ('splash', 'NOUN', 'splashes') )
        tests.append( ('book', 'NOUN', 'book') )
        tests.append( ('book', 'NOUN', 'books') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testNounGLReg(self):
        tests = []
        tests.append( ('focus', 'NOUN', 'focus') )
        tests.append( ('focus', 'NOUN', 'foci') )
        tests.append( ('trauma', 'NOUN', 'trauma') )
        tests.append( ('trauma', 'NOUN', 'traumata') )
        tests.append( ('larva', 'NOUN', 'larva') )
        tests.append( ('larva', 'NOUN', 'larvae') )
        #tests.append( ('ilium', 'NOUN', 'ilium') )      # not in vocab
        #ests.append( ('ilium', 'NOUN', 'ilia') )        # not in vocab
        #tests.append( ('taxon', 'NOUN', 'taxon') )      # not in vocab
        #tests.append( ('taxon', 'NOUN', 'taxa') )       # not in vocab
        tests.append( ('analysis', 'NOUN', 'analysis') )
        tests.append( ('analysis', 'NOUN', 'analyses') )
        #tests.append( ('cystis', 'NOUN', 'cystis') )    # not in vocab
        #tests.append( ('cystis', 'NOUN', 'cystides') )  # not in vocab
        #tests.append( ('foramen', 'NOUN', 'foramen') )  # not in vocab
        #tests.append( ('foramen', 'NOUN', 'foramina') ) # not in vocab
        tests.append( ('index', 'NOUN', 'index') )
        tests.append( ('index', 'NOUN', 'indices') )
        tests.append( ('matrix', 'NOUN', 'matrix') )
        tests.append( ('matrix', 'NOUN', 'matrices') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testCapitalization(self):
        tests = []
        tests.append( ('Dismiss', 'VERB', 'DISMiss') )
        tests.append( ('Dismiss', 'VERB', 'Dismisses') )
        tests.append( ('DISMISS', 'VERB', 'DISMISSING') )
        self.runGetAllLemmasTests(tests)
        self.runGetLemmaTests(tests)

    def testSpacyExtension(self):
        token = self.nlp('biggest')[0]
        self.assertEqual(token._.lemma(), 'big')
        token = self.nlp('I DISMiss it.')[1]
        self.assertEqual(token._.lemma(), 'Dismiss')
        token = self.nlp('I am DISMISSING it.')[2]
        self.assertEqual(token._.lemma(), 'DISMISS')

    def testProperNouns(self):
        lemmas = lemminflect.getLemma('Alaskans', 'NOUN', lemmatize_oov=False)
        self.assertEqual(len(lemmas), 0 )
        lemmas = lemminflect.getLemma('Alaskans', 'PROPN', lemmatize_oov=False)
        self.assertEqual(len(lemmas), 1 )
        self.assertEqual(lemmas[0], 'Alaskan')
        lemmas = lemminflect.getLemma('Axxlaskans', 'NOUN', lemmatize_oov=True)
        self.assertEqual(len(lemmas), 1 )
        self.assertEqual(lemmas[0], 'Axxlaskan')
        lemmas = lemminflect.getLemma('Axxlaskans', 'PROPN', lemmatize_oov=True)
        self.assertEqual(len(lemmas), 1 )
        self.assertEqual(lemmas[0], 'Axxlaskan')
        token = self.nlp('The Alaskans went South.')[1]
        self.assertEqual(token._.lemma(lemmatize_oov=False), 'Alaskan')
        token = self.nlp('The Axxlaskans went South.')[1]
        self.assertEqual(token._.lemma(lemmatize_oov=True), 'Axxlaskan')

    def testOverrides(self):
        # run the lemmatizer once to assure the overrides is loaded (ie.. lazy loading)
        lemminflect.getLemma('Alaskans', 'NOUN', lemmatize_oov=False)
        # Hack the code to replace the overrides dictionary
        orig_dict = lemminflect.Lemmatizer().overrides_dict
        lemminflect.Lemmatizer().overrides_dict = {'waltzes':{'VERB':('xxx',)}}
        lemmas = lemminflect.getLemma('waltzes', 'VERB', lemmatize_oov=False)
        self.assertEqual(lemmas, ('xxx',))
        # put the original dictionary back
        lemminflect.Lemmatizer().overrides_dict = orig_dict

    def testUPOSLog(self):
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

if __name__ == '__main__':
    level  = logging.WARNING
    format = '[%(levelname)s %(filename)s ln=%(lineno)s] %(message)s'
    #logging.basicConfig(level=level, format=format)

    # run all methods that start with 'test'
    unittest.main()
