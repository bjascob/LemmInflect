#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import re
from   collections import Counter
from   lemminflect.utils.Unigrams import Unigrams
from   lemminflect import config


# Filter for non-ascii words but keep hyphens
# Filter out Penn tags we aren't inerested in
# Note that reloading the csv file below, will filter out any words with commas in them
def cleanCounter(counter):
    new_counter = Counter()
    # ^ => start of string   $ => end of string
    # + => match 1 to unliminted times
    # [a-zA-Z\-] match a single character a-z, A-Z or -
    # !! Note this will through out contractions (ie.. ' not included)
    # re.search: Scan through string and return the first location where the re produces a match
    # This will return a match object if ONLY the defined characters are present
    regex = re.compile(r'^[a-zA-Z\-]+$')
    for key, count in counter.items():
        word, pos = key
        # Filter out words with more than one hyphen or has an undesired POS type
        if not word:
            continue
        if '--' in word:
            continue
        if word[0] == '-' or word[-1] == '-':
            continue
        if pos in ['HYPH', 'NFP', 'SYM', 'XX', 'ADD']:  # May be spacy specific
            continue
        # Lower-case anything that is not a proper noun
        if pos not in ['NNP', 'NNPS']:
            word = word.lower()
            key = (word, pos)
        # Add anything that contains only letters or hyphens
        # Sum counts since keys may be combined when lower-casing words
        if regex.search(word):
            new_counter[key] += count
    return new_counter


if __name__ == '__main__':

    if 1:
        # Clean the Gutenberg corpus
        print('Loading ', config.unigrams_gb_all_fn)
        gb_counter = Unigrams.load(config.unigrams_gb_all_fn)
        print('Loaded {:,} unigram counts'.format(len(gb_counter)))
        gb_counter = cleanCounter(gb_counter)
        print('Saving counts to %s' % config.unigrams_gb_clean_fn)
        Unigrams.saveCounter(config.unigrams_gb_clean_fn, gb_counter)
        print()

    if 1:
        # Clean the Billion word corpus
        print('Loading ', config.unigrams_bw_all_fn)
        bw_counter = Unigrams.load(config.unigrams_bw_all_fn)
        print('Loaded {:,} unigram counts'.format(len(bw_counter)))
        bw_counter = cleanCounter(bw_counter)
        print('Saving counts to %s' % config.unigrams_bw_clean_fn)
        Unigrams.saveCounter(config.unigrams_bw_clean_fn, bw_counter)
        print()

    if 1:
        # Combine counters and save
        counter = gb_counter + bw_counter
        print('Saving counts to %s' % config.unigrams_fn)
        Unigrams.saveCounter(config.unigrams_fn, counter)
        print()

    print('done')
