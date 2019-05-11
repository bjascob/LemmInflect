#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import re
import codecs
import nltk
from   lemminflect import config


# To check to to see the unicodes strings only contain ASCII characters
# a to z, hyphen and '.  Recode the word as an ASCII string.
def isASCIIWord(word):
    # ^ => start of string   $ => end of string
    # + => match 1 to unliminted times
    # [a-zA-Z\-] match a single character a-z, A-Z or -
    # re.search: Scan through string and return the first location where the re produces a match
    # This will return a match object if ONLY the defined characters are present
    regex = re.compile(r'^[a-zA-Z\-\']+$')
    if regex.search(word):
        return True
    return False

# !! Note that this is going to get rid of n't, etc..
#    could consider unidecode + nltk.tokenize.word_tokenize(line)
#    to strip non-ascii and preserve contractions
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
