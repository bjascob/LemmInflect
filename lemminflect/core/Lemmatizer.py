from copy import deepcopy
from .LexicalUtils           import getCapsStyle, applyCapsStyle, applyCapsStyleToDict
from ..utils.Singleton       import Singleton
from ..codecs.LemmaLUCodec   import LemmaLUCodec
from ..codecs.OverridesCodec import OverridesCodec
from .LemmatizerRules        import LemmatizerRules
from .. import config


# This is the top-level class that agregates logic.  It calls LemmaRules for OOV words.
class Lemmatizer(Singleton):
    def __init__(self, lemma_lu_fn=config.lemma_lu_fn, overrides_fn=config.lemma_overrides_fn):
        self.lemma_lu_fn = lemma_lu_fn
        self.overrides_fn = overrides_fn

    # Get all lemmas for the specific word.
    # upos is the universal dependencies of NOUN, PROPN, VERB, etc..
    # Note that the lower-case version of the word is used for lookup so if this is
    # a capitalized proper-noun, then upos must be 'PROPN'
    # Returns a dict with upos as key and a tuple of spellings for the values
    # The returned lemmas are capitalized the same was as the incoming word.
    def getAllLemmas(self, word, upos=None):
        caps_style = getCapsStyle(word)
        word = word.lower()
        if upos == 'PROPN':
            word = applyCapsStyle(word, 'first_upper')
            upos = 'NOUN'   # lu_dict originally has category which only has 'noun'
        lemmas = deepcopy(self._getLemmaDict().get(word, {}))
        # Apply any overrides
        overrides = deepcopy(self._getOverridesDict().get(word, {}))
        lemmas.update( overrides )
        # If a upos is provided, filter for it
        if upos:
            lemmas = {k:v for k,v in lemmas.items() if k==upos}
        lemmas = applyCapsStyleToDict(lemmas, caps_style)
        return lemmas

    # Get the lemma for the specific word.  Case of the word won't impact lemmatization
    # results, but the returned lemma will have the the same caps style.
    # upos is the universal dependencies of NOUN, VERB, etc..
    # Return is purposely the same as getAllLemmas so this returns a dict
    # with upos as key and a tuple of the spelling
    def getAllLemmasOOV(self, word, upos):
        caps_style = getCapsStyle(word)
        lemma = self._getOOVLemmatizer().lemmatize(word, upos)
        if lemma is None:
            return {}
        lemma = applyCapsStyle(lemma, caps_style)
        return {upos:(lemma,)}

    # Get the lemma(s) for the upos.  Use OOV rules if needed.
    # Return a tuple of various spellings or an empty set
    def getLemma(self, word, upos, lemmatize_oov=True):
        lemma_dict = self.getAllLemmas(word, upos)          # caps style preserved here
        if not lemma_dict and lemmatize_oov:
            lemma_dict = self.getAllLemmasOOV(word, upos)   # caps style preserved here
        if not lemma_dict:
            return ()
        elif len(lemma_dict) == 1:
            return list(lemma_dict.values())[0]  # dict has only 1 value, but the value is a tuple
        assert False, 'More than 1 category value in lemmas: %s' % str(lemma_dict)

    # Method for extending the spaCy tokens
    # Return the lemma or, if nothing was found, the original word
    def spacyGetLemma(self, token, form_num=0, lemmatize_oov=True, on_empty_ret_word=True):
        lemmas = self.getLemma(token.text, token.pos_, lemmatize_oov)
        if not lemmas:
            if on_empty_ret_word:
                return token.text
            else:
                return None
        elif len(lemmas) > form_num:
            return lemmas[form_num]
        else:
            return lemmas[0]

    # Lazy load dictionary and only do it only once
    def _getLemmaDict(self):
        if not hasattr(self, 'lemma_dict'):
            self.lemma_dict = LemmaLUCodec.load(self.lemma_lu_fn)
        return self.lemma_dict

    # Lazy load the overrides
    def _getOverridesDict(self):
        if not hasattr(self, 'overrides_dict'):
            self.overrides_dict = OverridesCodec.load(self.overrides_fn)
        return self.overrides_dict

    # Lazy load the lemmatizer and only do it only once
    def _getOOVLemmatizer(self):
        if not hasattr(self, 'oov_lemmatizer'):
            self.oov_lemmatizer = LemmatizerRules()
        return self.oov_lemmatizer
