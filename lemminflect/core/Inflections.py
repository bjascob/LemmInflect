import logging
from   copy import deepcopy
from   ..utils.Singleton import Singleton
from   .InflectionRules  import InflectionRules, MorphologyStyleModel
from   .LexicalUtils     import pennTagAlts, tagToUPos, uposToTags
from   .LexicalUtils     import getCapsStyle, applyCapsStyleToDict, applyCapsStyle
from   ..codecs.InflectionLUCodec import InflectionLUCodec
from   ..codecs.OverridesCodec import OverridesCodec
from   .Lemmatizer import Lemmatizer
from   .. import config


# This is the top-level class that agregates logic to get inflections
# from the dictionary or by using InflectionRules
class Inflections(Singleton):
    DICT_UPOS_TYPES = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'AUX']
    def __init__(self, infl_lu_fn=config.inflection_lu_fn, overrides_fn=config.infl_overrides_fn):
        self.infl_lu_fn = infl_lu_fn
        self.overrides_fn = overrides_fn
        self.logger = logging.getLogger(__name__)
        self.setUseInternalLemmatizer(True)     # only for _spacyGetInfl

    # Pass in the lemmatizer or None to use spaCy's
    def setUseInternalLemmatizer(self, TF):
        if TF:
            self.int_lemma = Lemmatizer()
        else:
            self.int_lemma = None

    def isUsingInternalLemmatizer(self):
        return self.int_lemma is not None

    # Get all inflections in the DB
    # Note that the lower-case version of the word is used for lookup so if this is
    # a capitalized proper-noun, then upos must be 'PROPN'
    # Return a dictionary of forms with the Penn Treebank tag as the key and a tuple
    # of the possible spellings as the valueif token.pos_ in self.DICT_UPOS_TYPES:
    def getAllInflections(self, lemma, upos=None):
        if upos is not None and upos not in self.DICT_UPOS_TYPES:
            self.logger.warning('Invalid upos type = %s', upos)
            return {}
        caps_style = getCapsStyle(lemma)
        lemma = lemma.lower()
        if upos == 'PROPN':
            lemma = applyCapsStyle(lemma, 'first_upper')
            upos = 'NOUN'   # infl_dict originally has category which only has 'noun'
        # Get the forms for the lemma from the main database
        forms = deepcopy(self._getInflDict().get(lemma, {}))
        # Apply any overrides
        overrides = deepcopy(self._getOverridesDict().get(lemma, {}))
        forms.update( overrides )
        # If there's a upos defined then return only those types
        if upos is not None:
            candidate_tags = uposToTags(upos)
            for key in list(forms.keys()):
                if key not in candidate_tags:
                    del forms[key]
        forms = applyCapsStyleToDict(forms, caps_style)
        return forms

    # Get all inflections using the Inflection Rules
    # Return a dictionary of inflections, keyed by Penn Tag  and a tuple
    # of the possible spellings as the value
    def getAllInflectionsOOV(self, lemma, upos):
        if upos not in self.DICT_UPOS_TYPES:
            self.logger.warning('Invalid upos type = %s', upos)
            return {}
        caps_style = getCapsStyle(lemma)
        morph_style = self._getInflStyleModel().getStyle(lemma, upos)
        if upos == 'VERB':
            if morph_style == 'reg':
                verbs = InflectionRules.buildRegVerb(lemma)
            else:
                verbs = InflectionRules.buildDoubledVerb(lemma)
            forms = {'VB':(lemma,), 'VBZ':(verbs[0],), 'VBN':(verbs[1],), \
                     'VBD':(verbs[1],), 'VBG':(verbs[2],)}
        elif upos in ['ADJ', 'ADV']:
            if morph_style == 'reg':
                atype = InflectionRules.buildRegAdjAdv(lemma)
            else:
                atype = InflectionRules.buildDoubledAdjAdv(lemma)
            if upos == 'ADJ':
                forms = {'JJ':(lemma,), 'JJR':(atype[0],), 'JJS':(atype[1],)}
            else:
                forms = {'RB':(lemma,), 'RBR':(atype[0],), 'RBS':(atype[1],)}
        elif upos in ['NOUN', 'PROPN']:
            if morph_style == 'reg':
                nouns = InflectionRules.buildRegNoun(lemma)
            else:
                nouns = InflectionRules.buildGrecNoun(lemma)
            forms = {'NN':(lemma,), 'NNS':(nouns[0],)}
        else:
            forms = {}
        forms = applyCapsStyleToDict(forms, caps_style)
        return forms

    # Get a single inflections for the tag.  Use OOV rules if needed.
    # Return a tuple of possible spellings
    def getInflection(self, lemma, tag, inflect_oov=True):
        # Get the forms for the lemma from the main database
        # and use the treebank tag to find the correct return value
        # If we don't find anything in the dictionary, use the rules
        #
        # There's an issue with proper-nouns that getAllInflections needs upos to
        # know if a noun's proper.  However, we don't want to limit the return
        # to a specific upos, otherwise the alternate tags below won't work.  We don't
        # need those for proper nouns so only pass in upos for 'PROPN'.
        upos = tagToUPos(tag)
        if upos == 'PROPN':
            forms = self.getAllInflections(lemma, upos)  # caps style preserved here
        else:
            forms = self.getAllInflections(lemma)  # caps style preserved here
        # Reverse the proper-noun hack.  Since the corpus only has noun in it, the tags will
        # all be NN or NNS (no NNP)
        form = self._extractForm(forms, tag)
        if form is None:
            # Look for a good form under the alternate tags
            for alt_tag in pennTagAlts(tag):
                form = forms.get(alt_tag, None)
                if form:
                    break
        # If still nothing, inflect oov
        if form is None and inflect_oov:
            forms = self.getAllInflectionsOOV(lemma, upos)      # caps style preserved here
            form = self._extractForm(forms, tag)
        if form is None:
            return ()
        return form

    # Reverse the proper-noun hack.  Since the corpus only has noun in it, the tags will
    # all be NN or NNS (no NNP)
    @staticmethod
    def _extractForm(forms, tag):
        if tag == 'NNP':
            form = forms.get('NN', None)
        elif tag == 'NNPS':
            form = forms.get('NNS', None)
        else:
            form = forms.get(tag, None)
        return form

    # Used with spacy ._.inflect
    # Returns a string or None
    def spacyGetInfl(self, token, tag, form_num=0, inflect_oov=True, on_empty_ret_word=True):
        # Use LemmInflect lemmatizer
        if self.int_lemma is not None:
            lemma = self.int_lemma.spacyGetLemma(token)
        # Use Spacy lemmatizer
        else:
            lemma = token.lemma_
            # handle pronouns.  The isTagBaseForm will force the immediate return
            # of these types anyway.
            if lemma == '-PRON-':
                lemma = token.text
        # If the requested tag to inflect to is a base form already then the lemma is the inflection
        if Lemmatizer.isTagBaseForm(tag):
            return lemma
        # Put the caps style from the word on to the lemma to solve spaCy casing issues with lemmas.
        caps_style = getCapsStyle(token.text)
        lemma = applyCapsStyle(lemma, caps_style)
        # Find the the inflections for the lemma
        inflections = ()
        upos = tagToUPos(tag)
        if upos in self.DICT_UPOS_TYPES:
            inflections = self.getInflection(lemma, tag, inflect_oov)
        if not inflections:
            if on_empty_ret_word:
                return token.text
            else:
                return None
        elif len(inflections) > form_num:
            return inflections[form_num]
        else:
            return inflections[0]

    # Lazy load inflection data and only do it once
    def _getInflDict(self):
        if not hasattr(self, 'infl_dict'):
            self.infl_dict = InflectionLUCodec.load(self.infl_lu_fn)
        return self.infl_dict

    # Lazy load overrides
    def _getOverridesDict(self):
        if not hasattr(self, 'overrides_dict'):
            self.overrides_dict = OverridesCodec.load(self.overrides_fn)
        return self.overrides_dict

    # Lazy load inflection model and only do it once
    def _getInflStyleModel(self):
        if not hasattr(self, 'morph_style_model'):
            self.morph_style_model = MorphologyStyleModel()
        return self.morph_style_model
