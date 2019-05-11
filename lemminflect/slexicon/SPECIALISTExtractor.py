from .SPECIALISTEntry  import SPECIALISTEntry, StandardVariant, AuxModVariant
from .SKey import *


class SPECIALISTExtractor(object):
    def __init__(self, word_set_fn=None):
        self.word_set = set()
        if word_set_fn is not None:
            print('Loading dictionary from ', word_set_fn)
            self.word_set = self._loadWordSet(word_set_fn)
            print('Loaded {:,} words available for inclusion'.format(len(self.word_set)))
            print()
        self.lexicon = []   # simple list of entries

    def extract(self, lexicon_fn):
        print('Parsing ', lexicon_fn)
        records = self._loadRawLexicon(lexicon_fn)
        print('Loaded {:,} records from the SPECIALIST Lexicon'.format(len(records)))
        print()
        # Loop through all raw records, parse them and add to the lexicon
        for record in records:
            entry = self._parseRecord(record)
            # Add to entries to the lexicon
            # _parseRecord returns None if they're not in the word_set
            # Don't add if they're an abbreviation or have a trademark (ie.. brand name)
            if entry and 'trademark' not in entry.features and \
                    'abbreviation_of' not in entry.features:
                # Add the entry to the lexicon.
                assert entry.EUI is not None and entry.base is not None \
                    and entry.category is not None
                self.lexicon.append(entry)

    ###########################################################################
    # Private methods used in parsing
    ###########################################################################

    # Load the dictionary and create a set of allowed words
    @staticmethod
    def _loadWordSet(dict_fn):
        word_set = set()
        with open(dict_fn, 'r') as f:
            lines = f.readlines()
            lines = [l.strip() for l in lines]
            word_set.update(lines)
        return word_set

    # Parse the SPECIALIST lexicon and extract it into "records"
    # which are the components between the braces "{xxx}"
    @staticmethod
    def _loadRawLexicon(lexicon_fn):
        with open(lexicon_fn) as f:
            data = f.read()
            end = -1
            records = []
            while True:
                start = data.find('{', end+1)
                end   = data.find('}', start+1)
                if start < 0 or end < 0:
                    break
                block = data[start+1:end].strip()
                lines = block.split('\n')
                lines = [l.strip() for l in lines]
                records.append(lines)
        return records

    # For each line in the record extract the key and
    # value it exists then update the SPECIALISTEntry with the info
    def _parseRecord(self, record):
        entry = SPECIALISTEntry()
        for line in record:
            key, value = self._extractKeyValue(line)
            self._updateSPECIALISTEntry(entry, key, value)
            # Stop parsing early if we're not going to keep this word
            if self.word_set and key == 'base':
                if value not in self.word_set:
                    return None
        assert entry.EUI is not None and entry.base is not None and \
                entry.category is not None, str(entry)
        return entry

    # Split a line into key=value
    @staticmethod
    def _extractKeyValue(line):
        parts = line.split('=')
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()   # key, value
        elif len(parts) == 1:
            return parts[0].strip(), None
        else:
            assert False, 'Invalid line split: ' + str(parts)

    # Big "switch" statement to handle all the possible keys in the lexicon
    # Note that some of the parsing such as the variants= line requires entry
    # to have certain fields already filled out.  The record is already ordered so
    # that base, cat and spelling_variant always come before that line.
    def _updateSPECIALISTEntry(self, entry, key, value=None):
        # Required entries for each record
        if key == 'entry':
            assert value, str(value)
            entry.EUI = value
        elif key == 'base':
            assert value,  str(value)
            entry.base = value
        elif key == 'cat':
            assert value,  str(value)
            entry.category = value
        # Handle gender for pronouns. See "The SPECIALIST Lexicon" page 77
        elif SKey.GENDER == key:
            assert SKey.GENDER not in entry.features, str(entry.features)
            entry.features[SKey.GENDER] = value
        # General features without values (ie.. True if present)
        elif key in [SKey.STATIVE, SKey.PROPER, SKey.BROAD_NEG, SKey.INTERR,
                     SKey.DEMONST, 'negative']:
            assert key not in entry.features, str(key)
            entry.features[key] = True
        # Alternate spellings
        elif key == 'spelling_variant':
            assert value,  str(value)
            entry.spelling_variant.append(value)
        # Acroymns
        elif key == 'acronym_of':
            assert value,  str(value)
            parts = value.split('|')    # base | EUI
            if len(parts)==2:
                entry.acronym_of.append(parts[1].strip())  # EUI
        # Nominalizations
        elif key == 'nominalization_of':
            parts = tuple(value.split('|'))     # word | cat | EUI
            assert len(parts)==3, str(parts)
            entry.nominalization_of.append(parts[2])      # EUI
        elif key == 'nominalization':
            parts = tuple(value.split('|'))     # word | cat | EUI
            assert len(parts)==3, str(parts)
            entry.nominalization.append(parts[2])      # EUI
        # Different kinds of variants (aka inflections)
        elif key == 'variants':
            self._updateForVariants(entry, value)
        elif key == 'variant':
            self._updateForVariant(entry, value)
        # Features specific to different parts of speech
        elif key in [SKey.TRAN, SKey.DITRAN, SKey.LINK, SKey.CPLXTRAN] or \
                    key.startswith(SKey.INTRAN):
            self._updateVerbCompl(entry, key, value)
        elif key == SKey.COMPL:
            self._updateNoun(entry, key, value)
        elif key == SKey.MOD_TYPE:
            self._updateAdverb(entry, key, value)
        elif key == SKey.POSITION:
            self._updateAdjective(entry, key, value)
        # Free determiner types
        elif key == SKey.TYPE:
            self._updateTypes(entry, key, value)
        # Other
        elif key in ['abbreviation_of', 'trademark']:
            if not value:
                value = True    #trademark may or may not have a value
            entry.features[key] = value
        else:
            assert False, 'unrecognized key: ' + str(key) + ':' + str(value)

    ###########################################################################
    # General methods for adding features to the entry
    # Some of these are complicated and in the future may require some
    # additional parsing to add them into the lexicon in a useful way.
    ###########################################################################

    # See "The SPECIALIST Lexicon" page 9, 31-35
    # https://lexsrv3.nlm.nih.gov/LexSysGroup/Projects/lexicon/current/docs/designDoc/UDF/lexRecord/syntax/complement/index.html
    # for field: intran, tran, ditran, link and cplxtran
    @classmethod
    def _updateVerbCompl(cls, entry, key, value):
        if key.startswith(SKey.INTRAN):
            parts = key.split(';')
            assert len(parts) <= 2
            if len(parts)==1:
                value = True
            else:
                value = parts[1]
            key = SKey.INTRAN
        assert value
        cls._addToFeatureList(entry, key, value)

    # See "The SPECIALIST Lexicon" page 54
    # field compl=  (there may be multiple lines with this)
    @classmethod
    def _updateNoun(cls, entry, key, value):
        assert value
        cls._addToFeatureList(entry, key, value)

    # See "The SPECIALIST Lexicon" page 11
    # field modification_type=  (there may be multiple lines with this)
    @classmethod
    def _updateAdverb(cls, entry, key, value):
        assert value
        cls._addToFeatureList(entry, key, value)

    # See "The SPECIALIST Lexicon" page 64
    # field position=  (there may be multiple lines with this)
    @classmethod
    def _updateAdjective(cls, entry, key, value):
        assert value
        cls._addToFeatureList(entry, key, value)

    # Free determiner type (all, some,..)
    # See "The SPECIALIST Lexicon" page 34
    @classmethod
    def _updateTypes(cls, entry, key, value):
        assert value
        cls._addToFeatureList(entry, key, value)

    # Simple helper to add a list or append to it
    @classmethod
    def _addToFeatureList(cls, entry, key, value):
        if key not in entry.features:
            entry.features[key] = [value]
        else:
            entry.features[key].append(value)


    ###########################################################################
    # Add Variants of two different styles to the entry
    ###########################################################################

    # The variants= line contains a code indicating the inflectional morphology of each entry
    # See "The SPECIALIST Lexicon" page 7
    # ie.. variant=reg|...  (multiple values including reg, inv,  uncount, plur,..
    @staticmethod
    def _updateForVariants(entry, value):
        isgroup = False
        if value.startswith('group('):
            value = value[6:-1]     # strip group(xx) from ie.. group(irreg|Gully|Gullys|)
            isgroup = True
        parts = value.split('|')
        infl_type = parts[0].strip()
        # for irreg, the inflections are listed since they don't follow the rules
        if SKey.IRREG == infl_type:
            inflections = [i.strip() for i in parts[1:] if i.strip()]
            # The first mode is the base word's mode
            if SKey.NOUN == entry.category:
                forms = [SKey.SINGULAR, SKey.PLURAL]
            elif SKey.VERB == entry.category:
                forms = [SKey.INFINATIVE, SKey.THIRD_PRES, SKey.PAST,
                         SKey.PAST_PART, SKey.PRES_PART]
            elif entry.category in [SKey.ADJ, SKey.ADV]:
                forms = [SKey.POSITIVE, SKey.COMPARATIVE, SKey.SUPERLATIVE]
            else:
                assert False, str(entry.category)
            # Create a dictionary of these
            idict = {}
            for i, inflection in enumerate(inflections):
                idict[forms[i]] = inflection
            # Add the variants to the entry
            variant = StandardVariant(infl_type, isgroup, idict)
            entry.variants.add(variant)
        # Otherwise just add the type so they can be morphed later
        else:
            variant = StandardVariant(infl_type, isgroup)
            entry.variants.add(variant)

    # The variant= line contains modal and auxiliary verbs inflections.
    # These differ from main verbs in the richness of their inflectional paradigm.
    # See "The SPECIALIST Lexicon" page 16
    # ie.. multiple entries for be (E0012152)
    #       variant=aren't;pres(fst_plur,second,thr_plur):negative
    @staticmethod
    def _updateForVariant(entry, value):
        parts = value.split(';')
        inflection = parts[0].strip()
        remainder = parts[1].strip()
        # Check the end of see if it's negated
        idx = remainder.find(':')
        negative = False
        if idx>=0:
            assert remainder[idx+1:] == 'negative'
            negative = True
            remainder = remainder[:idx]
        # Get the list of agreement features
        agreements = []
        idx1 = remainder.find('(')
        idx2 = remainder.find(')')
        if idx1>=0 and idx2>=0:
            assert idx2 > idx1
            agreements = remainder[idx1+1:idx2].split(',')
            remainder = remainder[:idx1]
        # Get the tense code
        tense_code = remainder.strip()
        variant = AuxModVariant(inflection, tense_code, agreements, negative)
        entry.variants.add(variant)
