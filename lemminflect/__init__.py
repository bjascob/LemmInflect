import sys
import logging
from   .core.Inflections import Inflections
from   .core.Lemmatizer  import Lemmatizer

__version__ = '0.1.0'


# Lemmatizer is a singleton so this will only instantiate and load the data
# (via the default fn) the first time it's called.
def getAllLemmas(word, upos=None):
    return Lemmatizer().getAllLemmas(word, upos)

def getAllLemmasOOV(word, upos):
    return Lemmatizer().getAllLemmasOOV(word, upos)

def getLemma(word, upos, lemmatize_oov=True):
    return Lemmatizer().getLemma(word, upos, lemmatize_oov)


# Inflections is a singleton so this will only instantiate and load the data
# (via the default fn) the first time it's called.
def getAllInflections(lemma, upos=None):
    return Inflections().getAllInflections(lemma, upos)

def getAllInflectionsOOV(lemma, upos):
    return Inflections().getAllInflectionsOOV(lemma, upos)

def getInflection(lemma, tag, inflect_oov=True):
    return Inflections().getInflection(lemma, tag, inflect_oov)

# Set which lemmatizer to use
def setUseInternalLemmatizer(TF):
    Inflections().setUseInternalLemmatizer(TF)

# Hook into spacy
try:
    import spacy
except ImportError:
    pass
if 'spacy' in sys.modules:
    min_version = '2.0'
    mv = min_version.split('.')
    sv = spacy.__version__.split('.')
    if sv[0] > mv[0] or (sv[0] == mv[0] and sv[1] >= mv[1]):
        spacy.tokens.Token.set_extension('lemma',   method=Lemmatizer().spacyGetLemma)
        spacy.tokens.Token.set_extension('inflect', method=Inflections().spacyGetInfl)
    else:
        logging.warning('Spacy extensions are disabled.  Spacy version is %s.  '
                        'A minimum of %s is required', spacy.__version__, min_version)
