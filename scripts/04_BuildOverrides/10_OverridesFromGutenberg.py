#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
from   collections import Counter, defaultdict
import nltk
import spacy
import lemminflect
from   lemminflect.utils.CorpusUtils     import loadNLTKCorpus
from   lemminflect.utils.ProgressBar     import ProgressBar
from   lemminflect.codecs.OverridesCodec import OverridesCodec
from   lemminflect import config
from   lemminflect.utils.CorpusUtils     import isASCIIWord


# This script creates an overrides file that allows the system to overcome issues with
# the way Spacy lemmatizes words and invalid data in the AGID.
# The created file is a mapping from lemma/tag to the "best" inflection.  Note that
# this only overrides methods where the treebank tag is used, not ones where the
# simplified AGID tag (V, N or A) is used.
# Note that if the AGID version is changed this script should be re-run.  Additionally
# if Spacy changes their lemmatizer or if a different lemmatizer is used consider re-running
# this script.
if __name__ == '__main__':
    # Configuration
    #corp_fns  = ['austen-emma.txt']                # 7,491 sentences
    corp_fns  = nltk.corpus.gutenberg.fileids()     # 18 files with 94K sentences
    max_chars = int(1e9)
    req_count = 4       # require at least the many instances in corpus for an override
    lemminflect.setUseInternalLemmatizer(True)      # use lemminflect or spaCy's lemmatizer
    inflect_oov = True                              # test/inflect out-of-vocab words
    multiples_fn = 'CorpMultiInfls.txt'

    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')
    print('Using spaCy version ', spacy.__version__)

     # Load the corpus to test with
    print('Loading corpus')
    sents = []
    for corp_fn in corp_fns:
        sents += loadNLTKCorpus(corp_fn, max_chars)
    print('Loaded {:,} test sentences'.format(len(sents)))
    print()

    # Create an empty overrides file before calling lemminflect because it loads this file on
    # first use.  This will mess-up the overrides creation process since overrides will be used.
    # Fix this issue by creating an empty file
    open(config.infl_overrides_fn, 'w').close()

    # Loop through the sentences and count the instances of (lemma, tag, corpus_word)
    # corpus_word is considered the "correct" inflection for the lemma/tag
    print('Processing sentences.  Using the internal lemmatizer = ', \
        lemminflect.Inflections().isUsingInternalLemmatizer())
    infl_ctr = Counter()
    pb = ProgressBar(len(sents))
    for i, sent in enumerate(sents):
        doc = nlp(sent)
        for word in doc:
            if not isASCIIWord(word.text) or not word.tag_:
                continue
            # Skip "be" since it's an oddball case where the inflection can't be determiened
            # from the Penn tag alone.
            if word.lemma_.lower() == 'be':
                continue
            # Only inflect Nouns, Verbs, Adverbs and Adjectives (and not Particles)
            ptype = word.tag_[0]
            if ptype in ['N', 'V', 'R', 'J'] and word.tag_!='RP':
                infl = word._.inflect(word.tag_, inflect_oov=inflect_oov)
                # Note if inflections/lemmatizer has 'on_empty_ret_word' = True (default) will likely
                # never get a None return. inflect_oov also default to true so this will prevent None returns.
                if infl is None:
                    continue
                lemma = word.lemma_  #spacy lemma
                if lemminflect.Inflections().isUsingInternalLemmatizer():
                    lemma = word._.lemma()
                key = (lemma, word.tag_, word.text.lower())
                infl_ctr[key] += 1
        pb.update(i)
    pb.clear()
    print('Completed.  Loaded {:,} lemma/tag/infl keys'.format(len(infl_ctr)))
    print()

    # Now create a new dictionary that only uses the lemma and tag as the key
    # and keeps a list of (corpus_word, count)
    lemma_tag_dict = defaultdict(list)
    for (lemma, tag, word), count in infl_ctr.items():
        lemma_tag_dict[(lemma,tag)].append( (word, count) )

    # Sort through the new dictionary and decide which is the correct word to use for the inflection.
    # This is trivial when only one form exist but when there are multiple, choose the one
    # with the hightest count (or alphabetical if the count is equal).
    # Save a list of the entries with multiple words for info / debug.
    print('Sorting through entries for overrides and multiple entries')
    overrides_f = open(config.infl_overrides_fn, 'w')
    multiples_f = open(multiples_fn, 'w')
    for (lemma, tag), mappings in sorted(lemma_tag_dict.items()):
        assert mappings
        if len(mappings) == 1:
            best_infl_word  = mappings[0][0]  # mappings is a list of (word, count)
            best_infl_count = mappings[0][1]
        elif len(mappings) > 1:
            # Choose the one with the highest count. If equal, choose alphabetically.
            # Note that counts are rarely equal when using the entire corpus.  This mostly occurs
            # for mispellings that only show-up once and these will get filtered out by "req_count".
            # So, we won't be too concerned if alphabetical isn't the perfect fall-back heuristic.
            mappings = sorted(mappings, key=lambda x:x[0])               # sort alphabetically
            mappings = sorted(mappings, key=lambda x:x[1], reverse=True) # sort highest count first
            best_infl_word  = mappings[0][0]
            best_infl_count = mappings[0][1]
            # Write out for info / debug
            multiples_f.write('  %s/%s -> %s\n' % (lemma, tag, str(mappings)))
        # Skip overrides for cases where there's only a few instances in the corpus
        if best_infl_count < req_count:
            continue
        # Now that we know what we want the lemma/tag to inflect to, check with pyinflect to see
        # what it's actually doing and if it's different, write an override.
        infl_list = lemminflect.getInflection(lemma, tag)
        infl = infl_list[0] if infl_list else ''    # choose form 0, the default
        if infl != best_infl_word:
            overrides_f.write('%s' % OverridesCodec.toString(lemma, tag, best_infl_word))
    multiples_f.close()
    overrides_f.close()
    print('Overrides file saved to: ', config.infl_overrides_fn)
    print('Multiple entries saved to: ', multiples_fn)
