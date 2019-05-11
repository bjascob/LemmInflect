from ..slexicon.SKey import *


# Converts the Penn Treebank tag string to upos
def tagToUPos(tag):
    if tag is None:
        return None
    tag = tag.upper()
    if tag[0] == 'J':
        return 'ADJ'
    elif tag[0] == 'R' and tag != 'RP':
        return 'ADV'
    elif tag in ['NNP', 'NNPS']:
        return 'PROPN'
    elif tag[0] == 'N':
        return 'NOUN'
    elif tag[0] == 'V' or tag == 'MD':
        return 'VERB'
    else:
        return None

# Convert upos to a list of candidate Penn tags
def uposToTags(upos):
    upos = upos.upper()
    if upos == 'VERB':
        return ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD']
    elif upos == 'ADJ':
        return ['JJ', 'JJR', 'JJS']
    elif upos == 'ADV':
        return ['RB', 'RBR', 'RBS']
    elif upos == 'NOUN':
        return ['NN', 'NNS', 'NNP', 'NNPS']
    else:
        return []

# Convert category to upos
def categoryToUPos(category):
    upos = category.upper()
    if upos == 'MODAL':
        upos = 'VERB'
    return upos

# Convert upos to category
def uposToCategory(upos):
    category = upos.lower()
    if upos == 'PROPN':
        category = 'noun'
    return category

# Convert category and infl_type to tags
slex_dict = {
    (SKey.NOUN, SKey.SINGULAR, False):['NN'],  (SKey.NOUN,SKey.PLURAL, False):['NNS'],
    (SKey.NOUN, SKey.SINGULAR,  True):['NNP'], (SKey.NOUN,SKey.PLURAL, True):['NNPS'],
    (SKey.ADJ, SKey.POSITIVE):['JJ'], (SKey.ADJ, SKey.COMPARATIVE):['JJR'],
    (SKey.ADJ, SKey.SUPERLATIVE):['JJS'],
    (SKey.ADV, SKey.POSITIVE):['RB'], (SKey.ADV, SKey.COMPARATIVE):['RBR'],
    (SKey.ADV, SKey.SUPERLATIVE):['RBS'],
    (SKey.VERB, SKey.INFINATIVE):['VB', 'VBP'], (SKey.VERB, SKey.PAST):['VBD'],
    (SKey.VERB, SKey.PAST_PART):['VBN'], (SKey.VERB, SKey.PRES_PART):['VBG'],
    (SKey.VERB, SKey.THIRD_PRES):['VBZ'] }
def catAndTypeToTag(category, infl_type, is_proper=False):
    if category in [SKey.AUX, SKey.MODAL]:
        category = SKey.VERB
    if category == SKey.NOUN:
        key = (category, infl_type, is_proper)
    else:
        key = (category, infl_type)
    tags = slex_dict.get(key, [])
    return tags

# When the tag doesn't yeild results, the following can be tried.
# Input here is the Penn treebank tag and returned is a list other tags to try.
# There are a number of reasons why the direct mappsings might not work but these could...
#   - inaccurate/ambigous mappings between SPECIALIST tags and the Penn treebank tags
#   - missing forms in the lookup system
#   - improperly tagged words that are tagged close to the correct form
def pennTagAlts(tag):
    # Penn tags have RP (particle) but in the lexicon they are either Adj or Adv and don't
    # have forms other than POSITIVE.  The Adv form is what the normal conversion returns
    if tag == 'RP':
        return ['JJ', 'RB']
    # For regular verbs the Past and Past-Particple forms are the same but only 1 may be
    # in the lexicon so try the other form.
    if tag == 'VBD':
        return ['VBN']
    if tag == 'VBN':
        return ['VBD']
    # Adjectives and Adverbs can act like one another so if one isn't found, try another.
    if tag.startswith('JJ'):
        return ['RB' + tag[2:]]
    if tag.startswith('RB'):
        return['JJ' + tag[2:]]
    # Modal verbs: (can, could) (may, might) (will, would) (shall, should) and "must"
    # I'm just lumping these under verbs when reading in the file
    if tag == 'MD':
        return ['VB', 'VBD']
    # return empty if nothing else to try
    return []

# Get the capitalization style of the word
def getCapsStyle(word):
    if word.isupper():
        return 'all_upper'
    elif word and word[0].isupper():
        return 'first_upper'
    else:
        return 'lower'

# Replicate the capitalization style in the new word
def applyCapsStyle(word, style):
    assert isinstance(word, str)
    if style not in ['all_upper', 'first_upper', 'lower']:
        raise ValueError('Invalid caps style = %s' % style)
    if style=='all_upper':
        return word.upper()
    elif style=='first_upper':
        return word.capitalize()
    else:
        return word.lower()

# Simple helper method to change all words in a tuple
def applyCapsStyleToDict(data, style):
    for key, words in data.items():
        # Check of the values in the dictionary are single string or tuple/list of them
        if isinstance(words, (list, tuple)):
            new_words = [applyCapsStyle(w, style) for w in words]
            data[key] = tuple(new_words)
        else:
            data[key] = applyCapsStyle(words, style)
    return data
