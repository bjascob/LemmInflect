#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
from   collections import Counter
from   lemminflect.utils.Unigrams import Unigrams
from   lemminflect.utils.CorpusUtils import isASCIIWord
from   lemminflect import config


# Filter for non-ascii words but keep hyphens
# Filter out Penn tags we aren't inerested in
# Note that reloading the csv file below, will filter out any words with commas in them
def cleanCounter(counter):
    new_counter = Counter()
    for key, count in counter.items():
        word, pos = key
        # Filter out words that don't look like ascii words
        if not isASCIIWord(word):
            continue
        # Filter out odd POS types. May be spacy specific
        if pos in ['HYPH', 'NFP', 'SYM', 'XX', 'ADD']:  
            continue
        # Lower-case anything that is not a proper noun
        if pos not in ['NNP', 'NNPS']:
            word = word.lower()
            key = (word, pos)
        # Sum counts since keys may be combined when lower-casing words
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
