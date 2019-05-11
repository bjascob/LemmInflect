
# Class for standard variants
class StandardVariant(object):
    def __init__(self, vtype, isgroup=False, irreg=None):
        # variant types can be reg, glreg, uncount, groupcount, metareg, plur, sing, inv
        #   there is also a inv;periph (this is the only place a ";" is used to denote a subclass)
        self.vtype      = vtype     # type of variant
        self.isgroup    = isgroup   # group(x) arround type.  Traditional term is collective.
        self.irreg      = irreg if irreg is not None else {} # dictionary of irregs to their infl


    def __eq__(self, other):
        if self.vtype==other.vtype and self.isgroup==other.isgroup and self.irreg==other.irreg:
            return True
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash( (self.vtype, self.isgroup, self.irreg.values()) )

    def __str__(self):
        s = '%-8s' % self.vtype
        if self.isgroup:
            s += ': isgroup=True'
        if self.irreg:
            s += ' : '
            for k, v in self.irreg.items():
                s += '%s=%s, ' % (k, v)
            s = s[:-2]
        return s

# class for Auxilliary and Modal verbs
class AuxModVariant(object):
    def __init__(self, inflection, form, agreements, negative):
        self.inflection = inflection
        self.form       = form          # ie.. infinitive, past, pres, ...
        self.agreements = agreements
        self.negative   = negative

    def __eq__(self, other):
        if self.inflection==other.inflection and self.form==other.form:
            return True
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash( (self.inflection, self.form) )

    def __str__(self):
        s = '%-12s : %-12s' %(self.inflection, self.form)
        if self.agreements:
            s += ' : ' + str(self.agreements)
        if self.negative:
            s += ' : negative'
        return s


# Container for each entry in the SPECIALIST Lexicon
class SPECIALISTEntry(object):
    def __init__(self):
        self.EUI               = None   # SPECIALIST Lexicon Entity Unique Indentifier
        self.base              = None   # base (lemma) form (ie the singular, infinitive,.. form)
        self.category          = None   # noun, adj, adv, verb, aux, modal, pron, prep, conj, compl
        self.spelling_variant  = []     # different spellings (ie.. color, colour)
        self.features          = {}     # generic {name: value}
        self.acronym_of        = []     # the opposite meaning
        self.nominalization_of = []     # ie realise has nominalization=realisation|noun|E0052110
        self.nominalization    = []     # ie realisation has nominalization_of=realise|verb|E0052111
        self.variants          = set()  # can be either StandardVariant or AuxModVariant class

    def getString(self):
        s = str(self) + '\n'
        if self.spelling_variant:
            s += '  aka: ' + str(self.spelling_variant) + '\n'
        if self.features:
            s += '  feats: ' + str(self.features) + '\n'
        if self.acronym_of:
            s += '  acronyms: ' + str(self.acronym_of) + '\n'
        if self.nominalization_of:
            s += '  nominalization_of: ' + str(self.nominalization_of) + '\n'
        if self.nominalization:
            s += '  nominalization: ' + str(self.nominalization) + '\n'
        if self.variants:
            s += '  variants:\n'
            for variant in self.variants:
                s += '    ' + str(variant) + '\n'
        return s[:-1]

    def __str__(self):
        return '%s : %s / %s' % (str(self.EUI), str(self.base), str(self.category))
