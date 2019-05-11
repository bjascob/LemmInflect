#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import os
import random
from   fnmatch import fnmatch
from   collections import Counter
import multiprocessing as mp
import nltk
import spacy
from   lemminflect.utils.ProgressBar import ProgressBar
from   lemminflect.utils.Unigrams import Unigrams
from   lemminflect import config


# Get all the files in a directory
def getFilenames(corp_dir):
    return [os.path.join(corp_dir, fn) for fn in os.listdir(corp_dir) if fnmatch(fn, '*.txt')]

# Load a file and split it into sentences
def loadFile(fn):
    text = ''
    # some files are not utf-8 so use 'replace' to replace non-ascii with '\ufff' which
    # hopefully will get weeded out later
    with open(fn, errors='replace') as f:
        lines = f.readlines()
        for line in lines:
            text += line.strip() + ' '
    sents = nltk.tokenize.sent_tokenize(text)
    sents = sents[1:-1] # clip the first and last
    return sents

# Use spacy to count unigrams in a file
def countFile(fn):
    counter = Counter()
    sents = loadFile(fn)
    for i, sent in enumerate(sents):
        doc = nlp(sent)     # nlp loaded in __main__
        for token in doc:
            if token.tag_.isalpha() and token.tag_ not in ['HYPH', 'NFP', 'SYM', 'XX', 'ADD']:
                key = (token.text, token.tag_)
                counter[key] += 1
    return counter


if __name__ == '__main__':
    # Config
    random.seed(123)
    max_files = int(1e4)    # 3,067 files total
    min_count = 2

    # Load spaCy
    print('Loading spaCy')
    nlp = spacy.load('en_core_web_sm')
    print()

    # Get the files and process them
    fns = getFilenames(config.gutenberg_dir)[:max_files]
    random.shuffle(fns)
    print('Processing {:,} files'.format(len(fns)))
    pb = ProgressBar(len(fns))
    counter = Counter()
    pool = mp.Pool()
    i = 0
    pb.update(i)
    for new_couts in pool.imap_unordered(countFile, fns):
        counter += new_couts
        i += 1
        pb.update(i)
    pb.clear()
    print()

    print('Saving counts to %s' % config.unigrams_gb_all_fn)
    Unigrams.saveCounter(config.unigrams_gb_all_fn, counter, min_count)
    print('done')
