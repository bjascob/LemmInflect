import gzip
from   ..slexicon.SKey import *


# Helper class for reading/writing lookup csv file
class InflectionLUCodec(object):
    # SPECIALIST LEXICON keys, used for writing
    # This represents the order of the forms written to lu.csv is SLexicon key terms
    slex_dict = {}
    slex_dict[SKey.NOUN]  = [SKey.PLURAL]
    slex_dict[SKey.ADJ]   = [SKey.COMPARATIVE, SKey.SUPERLATIVE]
    slex_dict[SKey.ADV]   = [SKey.COMPARATIVE, SKey.SUPERLATIVE]
    slex_dict[SKey.VERB]  = [SKey.PAST, SKey.PAST_PART, SKey.PRES_PART, SKey.THIRD_PRES]
    #slex_dict[SKey.AUX]   = [SKey.PAST, SKey.PAST_PART, SKey.PRES_PART, SKey.THIRD_PRES]
    #slex_dict[SKey.MODAL] = [SKey.PAST]
    # Penn treebank tags, used for reading.
    # This represents the order of forms read from lu.csv in Penn tag terms
    penn_dict = {}
    penn_dict[SKey.NOUN]  = ['NNS']                         # base is SINGULAR = NN
    penn_dict[SKey.ADJ]   = ['JJR', 'JJS']                  # base is POSITIVE = JJ
    penn_dict[SKey.ADV]   = ['RBR', 'RBS']                  # base is POSITIVE = RB
    penn_dict[SKey.VERB]  = ['VBD', 'VBN', 'VBG', 'VBZ']    # base is INFINATIVE = VB, VBP
    #penn_dict[SKey.AUX]   = ['VBD', 'VBN', 'VBG', 'VBZ']    # will be overridden below
    #penn_dict[SKey.MODAL] = ['VBD']                         # will be overridden below

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
        elif category in [SKey.VERB]:
            forms_dict['VB'] = (word,)
            forms_dict['VBP'] = (word,)
        # Don't read aux and modal from the look-up.  Get them later
        elif category in [SKey.AUX, SKey.MODAL]:
            forms_dict['VB'] = (word,)
        else:
            raise ValueError('Unrecognized category: %s' % category)
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
        # Update the dictionary with hard-coded values for aux and modals.
        infl_dict = cls.updateForAuxMod(infl_dict)
        return infl_dict

    # On reading, hard-code aux/modals since the don't follow the rules very well
    # This will override any previously read in values
    @staticmethod
    def updateForAuxMod(d):
        # Modal auxillary verbs
        d['can']    = {'VB':('can',),   'VBD':('could',)}
        d['may']    = {'VB':('may',),   'VBD':('might',)}
        d['will']   = {'VB':('will',),  'VBD':('would',)}
        d['shall']  = {'VB':('shall',), 'VBD':('should',)}
        d['must']   = {'VB':('must',),  'VBD':('must',)}
        d['ought']  = {'VB':('ought',), 'VBD':('ought',)}
        d['dare']   = {'VB':('dare',)}
        # Auxillaries verbs
        d['be']     = {'VB':('be',), 'VBD':('was', 'were'), 'VBG':('being',), 'VBN':('been',),
                       'VBP':('am', 'are'), 'VBZ':('is',)}
        d['do']     = {'VB':('do','does'), 'VBD':('did',)}
        d['have']   = {'VB':('have', 'has'), 'VBD':('had',), 'VBG':('having',)}
        return d
