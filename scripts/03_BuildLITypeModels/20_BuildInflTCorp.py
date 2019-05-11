#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
from   lemminflect.codecs.FormsTable import FormsTable
from   lemminflect.codecs.InflTCorpFileCodec import InflTCorpFileCodec
from   lemminflect.slexicon.SKey import *
from   lemminflect import config


if __name__ == '__main__':
    # Config
    print_multi_lemma = False

    # Load forms table
    print('Loading ', config.ftable_fn)
    ftable = FormsTable(config.ftable_fn)

    # Filter out non-inflectable forms, irregular, uncount, inv, plur, sing, ...
    # Keep only reg, regd, glreg. ie.. things that can be inflected
    infl_type_dict = {}
    for (base, category), forms in ftable.data.items():
        # Filter data for inflectable types
        forms = [f for f in forms if f[2] in [SKey.REG, SKey.REGD, SKey.GLREG]]
        if not forms:
            continue
        # Add the inflection, category key to the dict with the value a set of lemmas
        lemma = base.lower()
        for infl, infl_type, source in forms:
            infl = infl.lower()
            key = (lemma,category)
            if key not in infl_type_dict:
                infl_type_dict[key] = set([source])
            else:
                infl_type_dict[key].update([source])

    # Create a 1:1 mapping from (lemma,category) to infl_type by removing multiples\
    infl_td = set()
    for (infl, category), infl_source_set in sorted(infl_type_dict.items()):
        if len(infl_source_set) == 1:
            infl_source = list(infl_source_set)[0]
        else:
            # handle case where there's reg and glreg
            if SKey.REG in infl_source_set and SKey.GLREG in infl_source_set:
                infl_source = SKey.REG
            elif SKey.REG in infl_source_set and SKey.REGD in infl_source_set:
                infl_source = SKey.REG
            else:
                assert False, 'Unhandled case: %s' % str(infl_source_set)

        infl_td.add( (infl, category, infl_source) )


    # Write out the inflection training data
    with gzip.open(config.infl_tcorp_fn, 'wb') as f:
        for lemma, category, source in sorted(infl_td):
            line = InflTCorpFileCodec.toString(lemma, category, source)
            f.write(line.encode())
    print('Inflection training corpus saved to ', config.infl_tcorp_fn)
    print()
