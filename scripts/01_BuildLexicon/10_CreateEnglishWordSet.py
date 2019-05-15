#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import codecs
import nltk
from   lemminflect import config
from   lemminflect.utils.CorpusUtils import isASCIIWord


def loadDict(dict_fn):
    print('Loading dictionary from ', dict_fn)
    word_set = set()
    with codecs.open(dict_fn, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # split off contractions, etc..
            words = nltk.tokenize.word_tokenize(line)
            for word in words:
                # Get rid non ASCII and words with non-standard characters
                if isASCIIWord(word):
                    word_set.add(word)
    return word_set


if __name__ == '__main__':
    # Source dictionaries.
    dict1_fn    = '/usr/share/dict/american-english'
    dict2_fn    = '/usr/share/dict/british-english'

    # Combine dictionaries
    word_set  = loadDict(dict1_fn)
    word_set |= loadDict(dict2_fn)  # |= same as update

    # Save the dictionary
    print('{:,} total words in the word set.'.format(len(word_set)))
    with open(config.english_dict_fn, 'w') as f:
        for word in sorted(word_set):
            f.write('%s\n' % word)
    print('Data written to ', config.english_dict_fn)
    print()
