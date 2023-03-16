#!/usr/bin/env python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import os
import sys
import time
import warnings
from   acclib.LemmatizerTest import LemmatizerTest, Entry
from   lemminflect.utils.ProgressBar    import ProgressBar
from   lemminflect import config


###################################################################################################
# Test speed
###################################################################################################
class EmptyLemmatizer(object):
    def __init__(self):
        self.name = 'EmptyLemmatizer'
        self.version_string = 'Empty Lemmatizer (inflection is returned)'

    def getLemmas(self, entry):
        return set( [entry.infl] )


###################################################################################################
# LemmInflect
###################################################################################################
class LILemmatizer(object):
    def __init__(self):
        global lemminflect
        import lemminflect
        self.name = 'LemmInflect'
        self.version_string = 'LemmInflect version: %s' % lemminflect.__version__
        # Force loading dictionary and model so lazy loading doesn't show up in run times
        lemmas = lemminflect.getAllLemmas('testing', 'VERB')
        lemmas = lemminflect.getAllLemmasOOV('xxtesting', 'VERB')

    # Use only the dictionary methods
    def getLemmaDictOnly(self, entry, upos):
            lemmas = lemminflect.getAllLemmas(entry.infl, upos)
            lemma = lemmas.get(upos, ())
            if not lemma:
                return ()
            return lemma[0]

    # Use only the model methods
    def getLemmaOOVOnly(self, entry, upos):
        lemmas = lemminflect.getAllLemmasOOV(entry.infl, upos)
        lemma = lemmas.get(upos, ())
        if not lemma:
            return ()
        return lemma[0]

    # Standard combined method
    def getLemma(self, entry, upos):
        lemmas = lemminflect.getLemma(entry.infl, upos)
        if not lemmas:
             return ()
        return lemmas[0]

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    # With LemmInflect 0.1.0 and the 119,194 test set, there are 88,182 words OOV
    def getLemmas(self, entry):
        possible_lemmas = set()
        for upos in entry.upos_list:
            #lemma = self.getLemmaDictOnly(entry, upos)
            #lemma = self.getLemmaOOVOnly(entry, upos)
            lemma = self.getLemma(entry, upos)
            if lemma:
                possible_lemmas.add(lemma)
        return possible_lemmas


###################################################################################################
# Spacy
###################################################################################################
class SpacyLemmatizer(object):
    def __init__(self, smodel):
        import spacy
        from   spacy.language import Language
        self.name = 'Spacy'
        self.version_string = 'Spacy version: %s' % spacy.__version__
        # Inner class holds the state "pos" for a single token which is settable
        class POSSetter:
            def __init__(self):
                self.pos = 'INVALID'    # will raise and error if called with this
            def __call__(self, doc):
                doc[0].pos_ = self.pos
                return doc
        # Create the pipeline component
        @Language.factory('pos_setter')
        def pos_setter(nlp, name):
            return POSSetter()
        # Setup the pipeline with only 2 valid components
        self.nlp = spacy.load('en_core_web_sm', enable = ['lemmatizer'])
        self.nlp.add_pipe('pos_setter', 'pos_hacker', first=True)
        self.setter = self.nlp.get_pipe('pos_hacker')

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        possible_lemmas = set()
        for upos in entry.upos_list:
            self.setter.pos = upos
            # Getting  spacy/pipeline/lemmatizer.py:211: UserWarning: [W108] because the pipeline
            # is splitting appart 8 entries like "hows" to ["how" and "s"], shes, whens,...
            # Since the pipeline does not have a tokenizer and only has ['pos_setter', 'lemmatizer'] I guess
            # this logic must be in the lemmatizer.
            # Since the right answer for these is to remove the "s", just ignore this
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                doc = self.nlp(entry.infl)
            # For debug only
            # if len(doc) > 1:
            #     print('Skipping', entry.infl, entry.lemma, entry.pos_type, upos, entry.upos_list)
            #     print('doc len=', len(doc), doc)
            #     for t in doc:
            #         print('  token:', t, t.pos_)
            lemma = doc[0].lemma_
            possible_lemmas.add( lemma )
        return possible_lemmas


###################################################################################################
# CLiPS pattern.en
###################################################################################################
class PatternLemmatizer(object):
    def __init__(self):
        global pattern_lemmatize
        from pattern.en import lemma as pattern_lemmatize
        import pattern
        self.name = 'PatternEN'
        self.version_string = 'Pattern.en version: %s' % pattern.__version__

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        possible_lemmas = set()
        for upos in entry.upos_list:
            lemma = pattern_lemmatize(entry.infl)
            possible_lemmas.add( lemma )
        return possible_lemmas


###################################################################################################
# Stanford CoreNLP Server
###################################################################################################
class SNLPLemmatizer(object):
    def __init__(self):
        from acclib.StanfordParserClient import StanfordParserClient
        self.name = 'StanfordCoreNLP'
        self.version_string = 'StanfordCoreNLP version: 2018-10-05'
        self.snlp = StanfordParserClient()

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        lemma = self.snlp.getParse(entry.infl)
        if lemma is None:
            return set()
        else:
            return set([lemma])


###################################################################################################
# Stanza via Stanford CoreNLP (java calls handled via Stanza)
###################################################################################################
class StanzaLemmatizer(object):
    def __init__(self, batch_size=1000):
        import stanza
        self.batch_size = batch_size
        self.name = 'Stanza'
        self.version_string = 'Stanza version: %s' % stanza.__version__
        # Setup the classpath. Note that for released versions the libraries are in the main path
        # so we can skip the lib/* and liblocal/* 
        # os.environ['CLASSPATH'] = '/home/bjascob/Libraries/StanzaDev/CoreNLP/*' \
        #                           ':/home/bjascob/Libraries/StanzaDev/CoreNLP/lib/*' \
        #                           ':/home/bjascob/Libraries/StanzaDev/CoreNLP/liblocal/*'
        os.environ['CLASSPATH'] = '/home/bjascob/Libraries/StanfordNLP/stanford-corenlp-4.5.4/*'

    # Add the penn treebank tags based on the pos_type (V, A or N)
    # See https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    def addPTBTags(self, entry):
        if entry.pos_type == 'V':
            entry.tag_list = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        elif entry.pos_type == 'A':
            entry.tag_list = ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']
        elif entry.pos_type == 'N':
            entry.tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
        else:
            raise ValueError('entry.pos_type = "%s" is not allowed' % entry.pos_type)

    # iterator to split a list into n segments
    @staticmethod
    def chunker(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmasBatched(self, tester):
        from stanza.server.morphology import Morphology
        # Stanza's morphology class uses PennTreebank tags so add these to each entry
        for entry in tester:
            self.addPTBTags(entry)
        i, pb = 0, ProgressBar(len(tester))
        #fdebug = open('debug_stanza.dat', 'w')
        for chunk in self.chunker(list(tester), self.batch_size):
            # Note that tag_list may have multiple entries so words and tags will generally be longer than
            # the number of entries which needs to be disentangled below.
            words   = [entry.infl for entry in chunk for _    in entry.tag_list]
            tags    = [upos       for entry in chunk for upos in entry.tag_list]
            with Morphology(classpath="$CLASSPATH") as morph:
                result = morph.process(words, tags)
                # Disentangle the words/tags list for entries
                ptr = 0
                for entry in chunk:
                    possible_lemmas = set()
                    for upos in entry.tag_list:
                        possible_lemmas.add(result.words[ptr].lemma)
                        ptr += 1
                    # fdebug.write('%s %s %s -> %s %s\n' % (str(entry.infl), str(entry.tag_list),
                    #     str(entry.lemma), str(possible_lemmas), str(entry.lemma in possible_lemmas)))
                    tester.addResult(entry, possible_lemmas)
            i += len(chunk)
            pb.update(i)
        pb.clear()
        #fdebug.close()


###################################################################################################
# NLTK WordNet
###################################################################################################
class NLTKLemmatizer(object):
    def __init__(self):
        import nltk
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.name = 'NLTK'
        self.version_string = 'NLTK version: %s' % nltk.__version__

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        possible_lemmas = set()
        for upos in entry.upos_list:
            lemma = self.lemmatizer.lemmatize(entry.infl, entry.pos_type.lower())
            possible_lemmas.add( lemma )
        return possible_lemmas


###################################################################################################
# Common test function for all lemmatizers
###################################################################################################
def testLemmatizer(tester, lemmatizer, results_dir):
    tester.resetTest()
    print('Processing inflections')
    ntests = len(tester)
    st = time.time()
    # Do a bunch to speed-up server calls (added for Stanza code)
    if hasattr(lemmatizer, 'getLemmasBatched'):
        lemmatizer.getLemmasBatched(tester)
    # Common for for doing 1 lemma at a time
    elif hasattr(lemmatizer, 'getLemmas'):
        pb = ProgressBar(ntests)
        for i, entry in enumerate(tester):
            if i%1000 == 0: pb.update(i)
            possible_lemmas = lemmatizer.getLemmas(entry)
            tester.addResult(entry, possible_lemmas)
        pb.clear()
    else:
        raise RuntimeError('lemmatizer does not have a lemmatizing method')
    duration = time.time() - st
    print()

    # Print some stats
    print(lemmatizer.version_string)
    print('{:,} total test cases where {:,} had no returns.'.format(ntests,tester.lemma_no_ret))
    print('{:.1f} usecs per lemma'.format(int(1e6*duration/ntests)))
    print('{:,} incorrect lemmas = {:.1f}% accuracy'.format((tester.lemma_errors),
        100.*(1-tester.lemma_errors/ntests)))
    print('Results by pos type')
    for i in range(3):
        print('  {:8} : {:7,} / {:6,} = {:5.1f}% accuracy'.format(\
            tester.vanUPOS(i), tester.van_errors[i], tester.van_counts[i],
            100.*(1-tester.van_errors[i]/tester.van_counts[i])))
    print()

    # Save off the lemma error set
    if isinstance(lemmatizer, EmptyLemmatizer):
        return
    lemma_err_fn = os.path.join(results_dir, lemmatizer.name + '.txt')
    print('Saving lemma error set to ', lemma_err_fn)
    with open(lemma_err_fn, 'w') as f:
        f.write('%-24s %-24s != %s\n' % ('Word/POS', 'Corpus', 'Lemmatizer'))
        f.write('-'*60 + '\n')
        for infl, corp_lemma, upos, possible_lemmas in sorted(tester.lemma_err_set):
            s1 = '%s/%s' % (infl, upos)
            f.write('%-24s %-24s != %s\n' % (s1, corp_lemma, possible_lemmas))


if __name__ == '__main__':
    # config
    results_dir = '/tmp/'
    smodel      = 'en_core_web_sm'
    batch_size  = 999999

    # Load the corpus to test with
    print('Loading corpus ', config.acc_lemma_corp_fn)
    tester = LemmatizerTest(config.acc_lemma_corp_fn)
    print('Loaded {:,} test cases'.format(len(tester)))
    print()

    print('Enter test number to run or nothing to quit')
    print('0: Empty - Inflection is returned')
    print('1: LemmInflect')
    print('2: spaCy')
    print('3: NLTK')
    print('4: Stanza (does java calls to CoreNLP)')
    print('5: StanfordCoreNLP Client --> Be sure to start the server')
    print('6: CLiPS pattern.en')    # Doesn't install in Ubuntu 22.04 (only compatible up to python 3.6)

    print()
    while True:
        text = input('> ')
        if text == 'q' or not text:
            break
        print()
        if text == '0':
            lemmatizer = EmptyLemmatizer()
        elif text == '1':
            lemmatizer = LILemmatizer()
        elif text == '2':
            lemmatizer = SpacyLemmatizer(smodel)
        elif text == '3':
            lemmatizer = NLTKLemmatizer()
        elif text == '4':
            lemmatizer = StanzaLemmatizer(batch_size=batch_size)
        elif text == '5':
            lemmatizer = SNLPLemmatizer()
        elif text == '6':
            lemmatizer = PatternLemmatizer()
        else:
            print('Unrecognized test')
            continue
        testLemmatizer(tester, lemmatizer, results_dir)
        print()
