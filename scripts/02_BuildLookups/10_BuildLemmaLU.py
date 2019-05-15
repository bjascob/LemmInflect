#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
from   lemminflect.codecs.FormsTable import FormsTable
from   lemminflect.utils.Unigrams    import Unigrams
from   lemminflect.core.Lemmatizer   import LemmaLUCodec
from   lemminflect.slexicon.SKey     import *
from   lemminflect import config


if __name__ == '__main__':
    # Load forms table
    print('Loading ', config.ftable_fn)
    ftable = FormsTable(config.ftable_fn)

    # Load the unigrams
    print('Loading ', config.unigrams_fn)
    unigrams = Unigrams(config.unigrams_fn)
    print()

    # Invert the forms table so we have a dictionary with inflections,category as the keys
    lemma_lu = {}
    for (base, category), forms in ftable.data.items():
        # A modal is a sub-type of an aux verb. Since upos doesn't have modal,
        # put all modals under aux.
        if category == SKey.MODAL:
            category = SKey.AUX
        # forms is [inflection, infl_type, source], keep only the inflection
        infls = [f[0] for f in forms]
        # add the inflection, category key to the dict with the value a set of lemmas
        for infl in infls:
            key = (infl,category)
            if key not in lemma_lu:
                lemma_lu[key] = set([base])
            else:
                lemma_lu[key].add(base)

    # Write out the lemma lookup
    print('Printing inflections with multiple lemmas')
    ctr = 0
    with gzip.open(config.lemma_lu_fn, 'wb') as f:
        for (base, category), forms in sorted(lemma_lu.items()):
            # order forms by count in unigrams
            if len(forms) > 1:
                # Create a list of tuples for the (form, unigram count), sort it by count then
                # get back out the list of forms (now reverse sorted by count).
                fcounts = [(form, unigrams.getCountForLemma(form, category)) for form in forms]
                fcounts = sorted(fcounts, key=lambda x:x[1], reverse=True)
                forms   = [fcount[0] for fcount in fcounts]
                # print some debug info on multiple strings
                ctr += 1
                if 0:   #for debug
                    s1 = '%s/%s' % (base, category)
                    string = '%-36s : ' % s1
                    for fcount in fcounts:
                        string += '{:}({:.1e})  '.format(fcount[0], fcount[1])
                    print(string)
            # Write
            line = LemmaLUCodec.toString(base, category, forms)
            f.write(line.encode())
    print()
    print('{:,} out of {:,} words come from multiple lemmas and'.format(ctr, len(lemma_lu)))
    print('The order for form spellings is based on the unigram counts (highest first).')
    print()

    print('Lemma lookup saved to ', config.lemma_lu_fn)
    print()
