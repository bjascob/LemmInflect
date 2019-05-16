#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
from   lemminflect.codecs.FormsTable  import FormsTable
from   lemminflect.utils.Unigrams     import Unigrams
from   lemminflect.core.Inflections   import InflectionLUCodec
from   lemminflect.slexicon.SKey      import *
from   lemminflect import config


# Take in a list of tuples with the form (inflection, infl_type, source) and return
# a list candidates spellings.
# Extract only the desired inflection type.
def formsToCandidates(forms, infl_type, prefer_irreg):
    candidate_forms = [f for f in forms if f[1] == infl_type]
    # filter for irregulars
    if prefer_irreg:
        irreg_forms = [f for f in candidate_forms if f[2] == SKey.IRREG]
        if irreg_forms:
            candidate_forms = irreg_forms
    # Turn the list of tuples into a list of unique spellings
    candidates = set([infl for infl, infl_type, source in candidate_forms])
    return sorted(candidates)


# Notes on multiple spellings for a given inflection type:
# For 38,618 words there are 8,322 inflections with multiple spellings (prefer_irreg=False)
# When multiple forms exist they are sorted based on the count in Google Unigrams.  The
# consequnce of this is usually that the base form will be used since that's typically the
# most common.  This happens a lot for uncount nouns like people where plural can be people
# or peoples.  For "people" that's probably what we want but that's not the case all the time.
# In the lemmatizer, choosing the 2nd spelling for plurals will usually get you the 's' version
# while the 1st spelling (the default value) is the uncount or mass version.
# This could be improved upon if I have a unigram corpus tagged with Penn tags so I could get
# the frequency of NNS instead of just noun.
if __name__ == '__main__':
    # Config
    prefer_irreg = False    # only score irregular forms if they exist for the word

    # Load forms table
    print('Loading ', config.ftable_fn)
    ftable = FormsTable(config.ftable_fn)

    # Load the unigrams
    print('Loading ', config.unigrams_fn)
    unigrams = Unigrams(config.unigrams_fn)
    print()

    # Write out the inflections lookup
    print('Processing inflection data')
    multi_spell_ctr = 0
    with gzip.open(config.inflection_lu_fn, 'wb') as f:
        for (base, category), forms in sorted(ftable.data.items()):
            # Skip aux and modals. They will be added from hard-coded values on load
            if category in [SKey.MODAL, SKey.AUX]:
                continue
            # forms are lists of [inflection, infl_type, source] that needs to be disambiguated
            forms_dict = {}
            infl_types = sorted(set([f[1] for f in forms]))
            for infl_type in infl_types:
                spells = formsToCandidates(forms, infl_type, prefer_irreg)
                assert spells
                # prioritize spellings when multiples exist
                if len(spells) > 1:
                    multi_spell_ctr += 1
                    counts = [unigrams.getCountForInflections(s, category, infl_type) for s in spells]
                    spells = [s for s,_ in sorted(zip(spells,counts), key=lambda p:p[1], reverse=True)]
                forms_dict[infl_type] = spells
            line = InflectionLUCodec.toString(base, category, forms_dict)
            f.write(line.encode())
    print('Created inflections for {:,} words'.format(len(ftable.data)))
    print('There were {:,} inflections with multiple spellings to prioritize'.format(multi_spell_ctr))
    print()
    print('Inflection data saved to ', config.inflection_lu_fn)
