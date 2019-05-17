#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import os
import sys
import time
from   acclib.LemmatizerTest import LemmatizerTest, Entry
from   lemminflect.utils.ProgressBar    import ProgressBar
from   lemminflect import config

# Test speed
class EmptyLemmatizer(object):
    def __init__(self):
        self.name = 'EmptyLemmatizer'
        self.version_string = 'Empty Lemmatizer (inflection is returned)'

    def getLemmas(self, entry):
        return set( [entry.infl] )

# LemmInflect
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

# Spacy
class SpacyLemmatizer(object):
    def __init__(self, smodel):
        import spacy
        self.lemmatizer = spacy.load(smodel).vocab.morphology.lemmatizer
        self.name = 'Spacy'
        self.version_string = 'Spacy version: %s' % spacy.__version__

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        possible_lemmas = set()
        for upos in entry.upos_list:
            # The 3rd param, morphology=None, only impacts the call to is_base_form()
            # so omitting it should only impact trying to lemmatize a lemma.
            lemmas = self.lemmatizer(entry.infl, upos)
            lemma = lemmas[0]    # See morphology.pyx::lemmatize
            possible_lemmas.add( lemma )
        return possible_lemmas

# CLiPS pattern.en
class PatternLemmatizer(object):
    def __init__(self):
        global pattern_lemmatize
        from pattern.en import lemma as pattern_lemmatize
        self.name = 'PatternEN'
        import pattern
        self.version_string = 'Pattern.en version: %s' % pattern.__version__

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        possible_lemmas = set()
        for upos in entry.upos_list:
            lemma = pattern_lemmatize(entry.infl)
            possible_lemmas.add( lemma )
        return possible_lemmas

# Stanford CoreNLP
class SNLPLemmatizer(object):
    def __init__(self):
        from acclib.StanfordParserClient import StanfordParserClient
        self.snlp = StanfordParserClient()
        self.name = 'StanfordCoreNLP'
        self.version_string = 'StanfordCoreNLP version: 2018-10-05'

    # get the lemmas for every upos (pos_type='a' will have adv and adj)
    def getLemmas(self, entry):
        lemma = self.snlp.getParse(entry.infl)
        if lemma is None:
            return set()
        else:
            return set([lemma])

# NLTK WordNet
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


def testLemmatizer(tester, lemmatizer, results_dir):
    tester.resetTest()
    print('Processing inflections')
    ntests = len(tester)
    pb = ProgressBar(ntests)
    st = time.time()
    for i, entry in enumerate(tester):
        if i%1000 == 0: pb.update(i)
        possible_lemmas = lemmatizer.getLemmas(entry)
        tester.addResult(entry, possible_lemmas)
    duration = time.time() - st
    pb.clear()
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

    # Load the corpus to test with
    print('Loading corpus ', config.acc_lemma_corp_fn)
    tester = LemmatizerTest(config.acc_lemma_corp_fn)
    print('Loaded {:,} test cases'.format(len(tester)))
    print()

    print('Enter test number to run or nothing to quit')
    print('0: Empty - Inflection is returned')
    print('1: LemmInflect')
    print('2: spaCy')
    print('3: CLiPS pattern.en')
    print('4: Stanford CoreNLP --> Be sure to start the server')
    print('5: NLTK')
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
            lemmatizer = PatternLemmatizer()
        elif text == '4':
            lemmatizer = SNLPLemmatizer()
        elif text == '5':
            lemmatizer = NLTKLemmatizer()
        else:
            print('Unrecognized test')
            continue
        testLemmatizer(tester, lemmatizer, results_dir)
        print()
