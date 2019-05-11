# Keys in the extracted lexicon
# These are also the keys used to parse the NIH lexicon, although keys
# that are only used for parsing and don't end up in the final are not
# included here.
class SKey(object):
    # The "categories", aka Part-of-Speech in Lexicon
    NOUN        = 'noun'
    ADJ         = 'adj'
    ADV         = 'adv'
    VERB        = 'verb'
    AUX         = 'aux'
    MODAL       = 'modal'
    PRON        = 'pron'
    DET         = 'det'
    PREP        = 'prep'
    CONJ        = 'conj'
    COMPL       = 'compl'
    # keys that appear in "features" post extraction
    GENDER      = 'gender'
    STATIVE     = 'stative'
    PROPER      = 'proper'
    BROAD_NEG   = 'broad_negative'
    INTERR      = 'interrogative'
    DEMONST     = 'demonstrative'
    INTRAN      = 'intran'
    TRAN        = 'tran'
    DITRAN      = 'ditran'
    LINK        = 'link'
    CPLXTRAN    = 'cplxtran'
    COMPL       = 'compl'
    MOD_TYPE    = 'modification_type'
    POSITION    = 'position'
    TYPE        = 'type'
    # variant inflection keys (found in the Lexicon)
    IRREG       = 'irreg'           # irregular
    REG         = 'reg'             # regular
    REGD        = 'regd'            # regular final consonant is doubled
    GLREG       = 'glreg'           # greco-latin regular
    UNCOUNT     = 'uncount'         # uncount noun
    GCOUNT      = 'groupuncount'    # group uncount noun
    METAREG     = 'metareg'         # Meta-linguistic regular nouns
    PLUR        = 'plur'            # fixed plural nouns
    SING        = 'sing'            # fixed singular nouns
    INV         = 'inv'             # invariant adjective/adverb or invariant noun
    INV_PERIPH  = 'inv;periph'      # invariant periphrastic adjectives
    # Variant form keys for nouns (these are not keys in Lexicon)
    SINGULAR    = 'singular'
    PLURAL      = 'plural'
    # Variant form keys for verbs (these are not keys in Lexicon)
    INFINATIVE  = 'infinitive'
    THIRD_PRES  = 'third_pres'
    PAST        = 'past'
    PAST_PART   = 'past_part'
    PRES_PART   = 'pres_part'
    PRESENT     = 'pres'            # key in lexicon for aux/modals
    # Variant form keys for adjectives and adverbs (these are not keys in Lexicon)
    POSITIVE    = 'positive'
    COMPARATIVE = 'comparative'
    SUPERLATIVE = 'superlative'
