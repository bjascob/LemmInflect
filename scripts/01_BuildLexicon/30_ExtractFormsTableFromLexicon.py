#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
from   lemminflect.slexicon.SPECIALISTExtractor import *
from   lemminflect.slexicon.SPECIALISTEntry     import*
from   lemminflect.slexicon.SKey                import *
from   lemminflect.core.InflectionRules         import *
from   lemminflect.core.LexicalUtils            import categoryToUPos
from   lemminflect.core.LexicalUtils            import getCapsStyle, applyCapsStyleToDict
from   lemminflect import config
from   lemminflect.utils.CorpusUtils            import isASCIIWord


# Simple structs to help with collecting data
class Form(object):
    def __init__(self, inflection, infl_type, source):
        self.inflection = inflection
        self.infl_type  = infl_type
        self.source     = source

    def __hash__(self):
        return hash((self.inflection, self.infl_type, self.source))

class Entry(object):
    def __init__(self, base, category):
        self.base     = base
        self.category = category
        self.forms    = set()

    def addFormsFromDict(self, d, source):
        for infl_type, inflection in d.items():
            form = Form(inflection, infl_type, source)
            self.forms.add(form)


# Take in the lexicon entry and the word (aka spelling) to inflect or extract irregulars
def morph(lex_entry, word):
    entry = Entry(word, lex_entry.category)
    for variant in lex_entry.variants:
        # Handle aux/modals
        if isinstance(variant, AuxModVariant):
            # filter out all the negative variants 
            if not variant.negative:
                entry.forms.add( Form(variant.inflection, variant.form, 'auxmod') )
        # Handle irreg, reg, ...
        elif isinstance(variant, StandardVariant):
            # Irregular verbs
            if variant.vtype == SKey.IRREG:
                entry.addFormsFromDict(variant.irreg, SKey.IRREG)
            # Don't morph determiners and pronouns
            elif lex_entry.category in [SKey.PRON, SKey.DET]:
                continue
            # Everything else.. reg, regd, glreg,..
            else:
                upos = categoryToUPos(lex_entry.category)
                caps_style = getCapsStyle(word)
                d = InflectionRules.morph(word, upos, variant.vtype)
                d = applyCapsStyleToDict(d, caps_style)
                if not d:
                    print('No inflection for: ', word, lex_entry.category, variant.vtype)  # should never see this
                    continue
                entry.addFormsFromDict(d,  variant.vtype)
        else:
            assert False, 'Data Error'
    return entry


# Helper function to add an entry to the dictionary
# Don't add empty forms.  For duplicate keys, append forms.
def updateEntries(entries, entry):
    if not entry.forms:
        return entries
    key = (entry.base, entry.category)
    if key in entries:
        entries[key].forms.update( entry.forms )
    else:
        entries[key] = entry
    return entries


if __name__ == '__main__':
    # Setup the extractor by loading the words set of allowable words
    extractor = SPECIALISTExtractor(config.english_dict_fn)
    #extractor = NIHExtractor()  #don't limit the vocab
    extractor.extract(config.lexicon_fn)
    entries = extractor.lexicon
    print('Limiting word set has {:,} words in it'.format(len(extractor.word_set)))
    print('Extracted {:,} words from the Specialist Lexicon'.format(len(entries)))
    print()

    # Special cases
    for entry in entries:
        if entry.EUI == 'E0043086':
            entry.spelling_variant.append("n't")  # not
            break

    # Run through the lexicon and add inflection forms
    # Use a dict to gather data.  Entries are unique for the key = (base, category)
    # Note: there are 55 duplicate entries for this key, in the lexicon
    print('Morphing data')
    table_entries = {}
    for i, lex_entry in enumerate(entries):
        # Morph the base word
        table_entry = morph(lex_entry, lex_entry.base)
        table_entries = updateEntries(table_entries, table_entry)
        # Morph the spelling variants
        for spelling in lex_entry.spelling_variant:
            if not isASCIIWord(spelling):
                continue
            table_entry = morph(lex_entry, spelling)
            table_entries = updateEntries(table_entries, table_entry)
    # Get some stats
    nwords = len(table_entries)
    nforms = sum([len(entry.forms) for entry in table_entries.values()])
    print('Processed {:,} entries from the lexicon.'.format(len(entries)))
    print('  {:,} words/spellings were inflected and have {:,} inflections'.format(nwords, nforms))
    print()

    # Save the data to a csv file
    print('Saving inflection dictionary data to   ', config.ftable_fn)
    table_entries = table_entries.values()
    table_entries = sorted(table_entries, key=lambda x:x.category)
    table_entries = sorted(table_entries, key=lambda x:x.base)
    with gzip.open(config.ftable_fn, 'wb') as f:
        for entry in table_entries:
            string = '%s,%s:' % (entry.base, entry.category)
            for form in entry.forms:
                string += ' (%s,%s,%s) ' % (form.inflection, form.infl_type, form.source)
            string += '\n'
            f.write(string.encode())
    print('done')
