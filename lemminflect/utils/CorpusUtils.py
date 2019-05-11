

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
