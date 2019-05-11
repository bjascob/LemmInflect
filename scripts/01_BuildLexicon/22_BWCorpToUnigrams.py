#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import os
from   fnmatch import fnmatch
from   collections import Counter
import multiprocessing as mp
import spacy
from   lemminflect.utils.ProgressBar import ProgressBar
from   lemminflect.utils.Unigrams import Unigrams
from   lemminflect import config


# To get the raw BWCorpus data do..
#   wget http://statmt.org/wmt11/training-monolingual.tgz
#   tar --extract -v --file training-monolingual.tgz --wildcards training-monolingual/news.20??.en.shuffled
#    This gives the raw unprocessed, text

# Get all the files in a directory
def getFilenames(corp_dir):
    return [os.path.join(corp_dir, fn) for fn in os.listdir(corp_dir) if fnmatch(fn, 'news*')]

# Load a file and split it into sentences
def loadFile(fn, max_sents):
    sents = []
    with open(fn, errors='replace') as f:
        for line in f:
            sents.append(line.strip())
            if len(sents) >= max_sents:
                break
    return sents

# Chunk up an iterable
# Yield successive n-sized chunks from l.
def chunkList(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Use spacy to count unigrams in a file
def countSent(sents):
    counter = Counter()
    for sent in sents:
        doc = nlp(sent)     # nlp loaded in __main__
        for token in doc:
            if token.tag_.isalpha() and token.tag_ not in ['HYPH', 'NFP', 'SYM', 'XX', 'ADD']:
                key = (token.text, token.tag_)
                counter[key] += 1
    return counter

# Trim the counter
def trimCounter(counter, min_count):
    del_keys = [k for k, count in counter.items() if count < min_count]
    for key in del_keys:
        del counter[key]
    return counter

# number of sentences per file `wc -l *`
#   13,984,262 news.2007.en.shuffled
#   34,737,842 news.2008.en.shuffled
#   44,041,422 news.2009.en.shuffled
#   17,676,013 news.2010.en.shuffled
#    2,466,169 news.2011.en.shuffled
#  112,905,708 total
#
# On 28 thread i9-7940x
#   100K sents in about 40 seconds ==> 750 minutes (12.5 hours) for all
#   9.4M sents per hour
#
# The ~3,000 file Gutenberg corpus has 23,521,987 sentences but for
# some reason, to get the word-count to come out the same, only need to
# load 2M * 5 from the BWCorpus (ie.. BWCorpus sentences are 2x the size)
# The typical Gutenberg corp file has 8,000 sentences
if __name__ == '__main__':
    # Config
    max_files  = 99         # there are 5 total
    max_sents  = int(2e6)   # num sentences from each file
    count_size = int(1e3)   # number of sentences to count in each call
    min_count  = 2          # trim unigram counts less than this number

    # Load spaCy
    print('Loading spaCy')
    nlp = spacy.load('en_core_web_sm')
    print()

    # Get the files and process them
    fns = sorted(getFilenames(config.bwcorp_dir)[:max_files])
    print('Processing {:,} files'.format(len(fns)))
    counter = Counter()
    for fn in fns:
        # Load the file and chop the sentences up into groups to process (aka count)
        # This way we don't have to sum the counters together so often in the parent process.
        # Leave the default chunksize (python uses chunksize ~= len(iterable)/4*nprocs), since
        # changing it doesn't seem to have a big performnace impact.
        print('Loading ', fn)
        sents = loadFile(fn, max_sents)
        sent_groups = [chunk for chunk in chunkList(sents, count_size)]
        # Run processing
        print('Processing')
        # Create a pool and require the worker to close after every n tasks
        # If not specified, the worker never closes and memory usage climbs ridiculously.
        # The time to count each sentence group is large enough that setting this doesn't have
        # much of a performance impact.
        pool = mp.Pool(maxtasksperchild=8)
        pb = ProgressBar(len(sent_groups))
        i = 0
        pb.update(i)
        for new_counts in pool.imap_unordered(countSent, sent_groups):
            counter += new_counts
            i += 1
            pb.update(i)
        pb.clear()
        pool.close()
        pool.join()
        # Clip off any low count word/pos keys and save the file
        counter = trimCounter(counter, min_count)
        print('Saving counts to %s' % config.unigrams_bw_all_fn)
        Unigrams.saveCounter(config.unigrams_bw_all_fn, counter)
    print('done')
