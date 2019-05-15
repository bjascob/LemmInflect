#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
from   collections import Counter
import nltk
import spacy
import lemminflect
from   lemminflect.utils.ProgressBar   import ProgressBar
from   lemminflect.utils.CorpusUtils   import loadNLTKCorpus, isASCIIWord


if __name__ == '__main__':
    # Configuration
    corp_fns  = ['austen-emma.txt']                # 7,491 sentences
    #corp_fns  = nltk.corpus.gutenberg.fileids()     # 18 files with 94K sentences
    max_chars = int(1e5)
    lemminflect.setUseInternalLemmatizer(True)      # Use internal or spaCy lemmatizer

    # Load the corpus to test with
    print('Loading corpus')
    sents = []
    for fn in corp_fns:
        sents += loadNLTKCorpus(fn, max_chars)
    print('Loaded {:,} test sentences'.format(len(sents)))

    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')
    print()

    # Loop through the sentences
    word_ctr = 0
    errors = Counter()
    pb = ProgressBar(len(sents))
    print('Processing sentences with use internal lemmatizer = ', \
        lemminflect.Inflections().isUsingInternalLemmatizer())
    for i, sent in enumerate(sents):
        if i%10 == 0:
            pb.update(i)
        doc = nlp(sent)
        for word in doc:
            word_ctr += 1
            if word.text.isalpha() and word.tag_ and word.tag_[0] in ['N', 'V', 'R', 'J'] and \
                word.tag_ != 'RP' and word.lemma_ not in ['be', 'do', 'have', 'far']:
                # The inflection method will first lemmatize the word then inflect it to whatever tag
                # is passed in.  If we pass in the same tag as the original work it should inflect back to that word.
                infl = word._.inflect(word.tag_)
                if infl == word.text:   # good
                    pass
                # Note if inflections/lemmatizer has 'on_empty_ret_word' = True (default) will likely
                # never get a None return.  inflect_oov also default to true so this will prevent None returns.
                elif not infl:
                    err = 'OOV : %s,%s' % (word.text, word.tag_)
                    errors[err] += 1
                else:
                    lemma = word.lemma_  #spacy lemma
                    if lemminflect.Inflections().isUsingInternalLemmatizer():
                        lemma = word._.lemma()
                    err = 'fail: %s,%s : %s -> %s' % (word.text, word.tag_, lemma, infl)
                    errors[err] += 1
    pb.clear()
    print()

    # Print the errors
    print()
    print('Errors:      word/Tag : lemma -> inflection')
    for error, count in errors.most_common():
        print('%4d : %s' % (count, error))
    print()
