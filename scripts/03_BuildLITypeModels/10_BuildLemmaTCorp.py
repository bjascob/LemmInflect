#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
from   lemminflect.codecs.FormsTable import FormsTable
from   lemminflect.codecs.LemmaTCorpFileCodec import LemmaTCorpFileCodec
from   lemminflect.slexicon.SKey import *
from   lemminflect import config


if __name__ == '__main__':
    # Config
    print_multi_lemma = False

    # Load forms table
    print('Loading ', config.ftable_fn)
    ftable = FormsTable(config.ftable_fn)

    # Filter out non-lemmatization forms, irregular, uncount, inv, plur, sing, ...
    # Keep only reg, regd, glreg. ie.. things that can be lemmatized with rules
    # Invert the forms table so we have a dictionary with inflections,category as the keys
    lemma_td = {}
    for (base, category), forms in ftable.data.items():
        # Filter data for inflectable types
        forms = [f for f in forms if f[2] in [SKey.REG, SKey.REGD, SKey.GLREG]]
        if not forms:
            continue
        # Invert it.  Use lower-case for everything
        # add the inflection, category key to the dict with the value a set of lemmas
        lemma = base.lower()
        for infl, infl_type, source in forms:
            infl = infl.lower()
            key = (infl,category,source)
            if key not in lemma_td:
                lemma_td[key] = set([lemma])
            else:
                lemma_td[key].add(lemma)

    # Write out the lemma lookup
    # Don't use words where there's multiple lemma since we don't know which is correct
    # Only 82 out of 60,561 words come from multiple lemmas
    if print_multi_lemma:
        print('Printing inflections with multiple lemmas - these will be skipped.')
    ctr = 0
    with gzip.open(config.lemma_tcorp_fn, 'wb') as f:
        for (infl, category, source), forms in sorted(lemma_td.items()):
            assert len(forms) != 0
            # print some debug info on multiple strings
            if len(forms) > 1:
                ctr += 1
                if print_multi_lemma:
                    s1 = '%s/%s' % (infl, category)
                    string = '%-36s : %s' % (s1, str(forms))
                    print(string)
                continue    # Don't put this in the csv
            # Write
            lemma = list(forms)[0]
            line = LemmaTCorpFileCodec.toString(infl, category, source, lemma)
            f.write(line.encode())
    print()
    print('{:,} out of {:,} words come from multiple lemmas'.format(ctr, len(lemma_td)))
    print()

    print('Lemma training corpus file saved to ', config.lemma_tcorp_fn)
    print()
