import gzip
from   ..slexicon.SKey import *


# Helper class for reading/writing lookup csv file
# SPECIALIST Lexicon and the forms_table.dat.gz has 'aux' and 'modal' which are types of verbs
#   * modals are "can, may, shall, will".  The all have only one form, 'past' plus the base form
#     lump modals under generic verbs since their forms are just a subset of a verbs
#   * aux are "be, do, have".  These 3 are oddballs so handle them separately
class InflectionLUCodec(object):
    # SPECIALIST LEXICON keys, used for writing
    slex_dict = {}
    slex_dict[SKey.NOUN]  = [SKey.PLURAL]
    slex_dict[SKey.ADJ]   = [SKey.COMPARATIVE, SKey.SUPERLATIVE]
    slex_dict[SKey.ADV]   = [SKey.COMPARATIVE, SKey.SUPERLATIVE]
    slex_dict[SKey.VERB]  = [SKey.PAST, SKey.PAST_PART, SKey.PRES_PART, SKey.THIRD_PRES]
    slex_dict[SKey.AUX]   = [SKey.PAST, SKey.PAST_PART, SKey.PRES_PART, SKey.THIRD_PRES]
    slex_dict[SKey.MODAL] = [SKey.PAST]
    # Penn treebank tags, used for reading
    penn_dict = {}
    penn_dict[SKey.NOUN]  = ['NNS']                         # base is SINGULAR = NN
    penn_dict[SKey.ADJ]   = ['JJR', 'JJS']                  # base is POSITIVE = JJ
    penn_dict[SKey.ADV]   = ['RBR', 'RBS']                  # base is POSITIVE = RB
    penn_dict[SKey.VERB]  = ['VBD', 'VBN', 'VBG', 'VBZ']    # base is INFINATIVE = VB, VBP
    penn_dict[SKey.AUX]   = []                              # use special aux_verbs below
    penn_dict[SKey.MODAL] = ['VBD']
    # Special rules Aux verbs
    aux_verbs = {}
    aux_verbs['be'] = {'VB':('be',), 'VBD':('was', 'were'), 'VBG':('being',), 'VBN':('been',),
                       'VBP':('am', 'are'), 'VBZ':('is',)}
    aux_verbs['do'] = {'VB':('do','does'), 'VBD':('did',)}
    aux_verbs['have'] = {'VB':('have', 'has'), 'VBD':('had',), 'VBG':('having',)}

    @classmethod
    def toString(cls, word, category, forms_dict):
        forms_str = ''
        for ftype in cls.slex_dict[category]:
            for spelling in forms_dict.get(ftype,[]):
                forms_str += '%s/' % spelling
            if forms_str.endswith('/'):
                forms_str = forms_str[:-1]
            forms_str += ','
        if forms_str.endswith(','):
            forms_str = forms_str[:-1]
        line = '%s,%s,%s\n' % (word, category, forms_str)
        return line

    @classmethod
    def fromString(cls, line):
        parts = line.strip().split(',')
        word = parts[0]
        category = parts[1]
        forms = parts[2:]
        forms_dict = {}
        for i, ftype in enumerate(cls.penn_dict[category]):
            if i < len(forms):
                spellings = tuple(forms[i].split('/'))
                if len(spellings)>1 or spellings[0]:  # empty produces ('',)
                    forms_dict[ftype] = spellings
        # update for base forms
        if category == SKey.NOUN:
            forms_dict['NN'] = (word,)
        elif category == SKey.ADJ:
            forms_dict['JJ'] = (word,)
        elif category == SKey.ADV:
            forms_dict['RB'] = (word,)
        elif category in [SKey.VERB, SKey.MODAL]:
            forms_dict['VB'] = (word,)
            forms_dict['VBP'] = (word,)
        elif category == SKey.AUX:  # handle aux's separately
            return word, SKey.VERB, cls.aux_verbs[word]
        else:
            raise ValueError('Unrecognized category: %s' % category)
        # Convert modals to VERBs
        if category == SKey.MODAL:
            category = SKey.VERB
        return word, category, forms_dict

    # Load inflections_lu.csv
    @classmethod
    def load(cls, fn):
        infl_dict = {}
        with gzip.open(fn, 'rb') as f:
            for line in f:
                line = line.decode()
                word, _, forms_dict = cls.fromString(line)
                if word not in infl_dict:
                    infl_dict[word] = forms_dict
                else:
                    infl_dict[word].update(forms_dict)
        return infl_dict
