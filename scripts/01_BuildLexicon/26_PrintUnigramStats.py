#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
from   collections import Counter
from   lemminflect.utils.Unigrams import Unigrams
from   lemminflect import config


# Get the total sum of the counter
def getSumCounts(counter):
    return sum([c for c in counter.values()])

# For debug, print some counts
def printPOSCounts(counter):
    pos_counter = Counter()
    for key, count in counter.items():
        word, pos = key
        pos_counter[pos] += count
    for pos, count in sorted(pos_counter.items()):
        print('  {:6} {:,}'.format(pos, count))

# Load the words from from the file
def loadWordSetFromFile(fn):
    word_set = set()
    with open(fn) as f:
        for line in f:
            word_set.add( line.strip() )
    return word_set

# Get the word set from the Counter
def getWordSetFromCounter(counter):
    word_set = set()
    for word, pos in counter.keys():
        word_set.add(word)
    return word_set


if __name__ == '__main__':
    # Config
    fns = [config.unigrams_gb_clean_fn, config.unigrams_bw_clean_fn,
           config.unigrams_fn]

    for unigram_fn in fns:
        # Load the unigrams
        print('Loading ', unigram_fn)
        unigrams = Unigrams(unigram_fn)
        counter = unigrams.counter

        # Print the total entries and POS counts
        print('The size of the included corpus is {:,} words'.format(getSumCounts(counter)))
        print('There are {:,} total unigram entries'.format(len(counter)))
        if 0:
            print('Counts by POS are..')
            printPOSCounts(counter)
            print()

        # Load the dictionary and get wordsets
        dict_words = loadWordSetFromFile(config.english_dict_fn)
        unigram_words = getWordSetFromCounter(counter)
        missing_set = dict_words.difference(unigram_words)
        print('{:,} words in the unigram set'.format(len(unigram_words)))
        print('{:,} words in the test dictionary'.format(len(dict_words)))
        print('{:,} dictionary words are missing from the unigrams'.format(len(missing_set)))
        if 0:
            print('Dictionary words missing from unigrams')
            for word in sorted(missing_set):
                print('  ', word)
        print()
