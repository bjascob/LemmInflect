#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import os
from   fnmatch import fnmatch
from   collections import Counter
import spacy
import lemminflect
from   lemminflect.utils.ProgressBar   import ProgressBar
from   lemminflect.utils.CorpusUtils   import isASCIIWord
from   lemminflect import config

# Get all the files in a directory
def getFilenames(corp_dir):
    return [os.path.join(corp_dir, fn) for fn in os.listdir(corp_dir) if fnmatch(fn, 'news*')]

# Load a file and split it into sentences
def loadFile(fn, max_sents):
    sents = []
    with open(fn, errors='replace') as f:
        for line in f:
            sents.append(line.strip())
            if len(sents) >= max_sents:
                break
    return sents

if __name__ == '__main__':
    # Configuration
    corp_fn   = sorted(getFilenames(config.bwcorp_dir))[0]  # don't use same file as overrides
    max_sents = int(1e3)
    lemminflect.setUseInternalLemmatizer(True)              # Use internal or spaCy lemmatizer

     # Load the corpus to test with
    print('Loading corpus from ', corp_fn)
    sents = loadFile(corp_fn, max_sents)
    print('Loaded {:,} test sentences'.format(len(sents)))
    print()

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
    print("Instances where the system's inflection doesn't match the original word.")
    print("Note that this assume the original word was tagged correctly.")
    print("Watch for invalid tags, and ignore those errors.")
    print("Remember the lemmatizer only tags the broad UPOS category, not the details Penn Tag.")
    print('Errors:      word/Tag : lemma -> inflection')
    for error, count in errors.most_common():
        print('%4d : %s' % (count, error))
    print()
