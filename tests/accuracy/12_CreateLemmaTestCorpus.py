#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import os
from   collections import defaultdict
from   lemminflect import config


# Note the AGID database was converted in pyInflect to infl.csv.
# Use that file here for simplicity instead of adding code to convert it again.
if __name__ == '__main__':
    #see https://github.com/bjascob/pyInflect/blob/master/pyinflect/infl.csv
    infl_fn  = './acclib/infl.csv'

    # Load the lmiting word-set
    word_set = set()
    if 1:
        with open(config.acc_word_set_fn) as f:
            for line in f:
                word_set.add(line.strip())

    # Load the inflection data
    infl_dict = defaultdict(list)
    print('Reading ', infl_fn)
    with open(infl_fn) as f:
        for line in f:
            line     = line.strip()
            parts    = line.split(',')
            lemma    = parts[0]
            pos_type = parts[1]   # verb, adj/adv, noun part-of-speech tag
            if word_set and lemma not in word_set:
                continue
            infls = []
            for infl in parts[2:]:
                if infl == '<>': continue
                spellings = infl.split('/')
                infls += spellings
            for infl in infls:
                # Weed out some oddballs
                if infl == 'a':
                    continue
                if word_set and infl not in word_set:
                    continue
                # Add to test corp
                infl_dict[(infl, pos_type)].append(lemma)
    print('Loaded {:,} different (infl,pos) keys'.format(len(infl_dict)))

    # Look through the dictionary for entries with multiple lemmas and remove them
    # from the test set.
    delkeys = set()
    for key, lemmas in infl_dict.items():
            if len(lemmas) > 1:
                delkeys.add(key)
    print('Found {:,} (infl,pos) keys that have multiple lemmas.'.format(len(delkeys)))
    for key in delkeys:
        del infl_dict[key]

    # Save the data to a file
    # Note the file format is inflection,pos_type,lemma
    print('Saving {:,} remaining entries to {:}'.format(len(infl_dict), config.acc_lemma_corp_fn))
    with open(config.acc_lemma_corp_fn, 'w') as f:
        for (infl, pos_type), lemmas in infl_dict.items():
            assert len(lemmas) == 1
            lemma = lemmas[0]
            f.write('%s,%s,%s\n' % (infl, pos_type, lemma))
    print()
