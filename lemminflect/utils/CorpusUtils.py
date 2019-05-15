import re

# load sentences from the nltk corpus
# To see available files do... print(nltk.corpus.gutenberg.fileids())
def loadNLTKCorpus(corp_fn, max_chars=int(1e12)):
    # only import nltk if required
    import nltk
    text = nltk.corpus.gutenberg.raw(corp_fn)
    corpus_len = len(text)
    text = text[:max_chars]
    print('{:,} characters from {}, truncated to {:,}'.format(corpus_len, corp_fn, len(text)))
    text = text.replace('\n', ' ')
    sents = nltk.tokenize.sent_tokenize(text)
    sents = sents[1:-1] # clip the first and last
    return sents

# ^ => start of string   $ => end of string
# + => match 1 to unliminted times
# [a-zA-Z\-] match a single character a-z, A-Z - or '
# re.search: Scan through string and return the first location where the re produces a match
# This will return a match object if ONLY the defined characters are present
is_ascii_regex = re.compile(r'^[a-zA-Z\-\']+$')

# To check to to see the strings only contain ASCII characters a to z, hyphen and apostrophe
# Additionally check that a word doesn't start or end with a hyphen or that is has more than one.
def isASCIIWord(word):
    if not word or word[0] == '-' or word[-1] == '-' or '--' in word:
        return False
    if is_ascii_regex.search(word):
        return True
    return False
