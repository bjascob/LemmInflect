# LemmInflect
**A python module for English word lemmatization and inflection.**

## About
LemmInflect uses a dictionary approach to lemmatize English words and inflect them into forms specified by a user supplied [Universal Dependencies](https://universaldependencies.org/u/pos/) or [Penn Treebank](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) tag.  The library works with out-of-vocabulary (OOV) words by applying neural network techniques to classify word forms and choose the appropriate morphing rules.

The system acts as a standalone module or as an extension to the [spaCy](https://spacy.io/) NLP system.

The dictionary and morphology rules are derived from the [NIH's SPECIALIST Lexicon](https://lsg3.nlm.nih.gov/LexSysGroup/Projects/lexicon/current/web/index.html) which contains an extensive set information on English word forms.


## Library Usage
To lemmatize a word use the method `getLemma()`.  This takes a word and a Universal Dependencies tag and returns the lemmas as a list of possible spellings.  The dictionary system is used first, and if no lemma is found, the rules system is employed.
```
> from lemminflect import getLemma
getLemma('watches', upos='VERB')
('watch',)
```
To inflect words, use the method `getInflection`.   This takes a lemma and a Penn Treebank tag and returns a tuple of the specific inflection(s) associated with that tag.  Similary to above, the dictionary is used first and then inflection rules are applied if needed..
```
> from lemminflect import getInflection
> getInflection('watch', tag='VBD')
('watched',)

> getInflection('xxwatch', tag='VBD')
('xxwatched',)
```
The library provides lower-level functions to access the dictionary and the OOV rules directly.  For a detailed description see [Lemmatizer](lemmatizer.md) or [Inflections](inflections.md).


## Usage as a Spacy Extension
To use as an extension, you need spaCy version 2.0 or later.  Versions 1.9 and earlier do not support the extension methods used here.

To setup the extension, first import `lemminflect`.  This will create new `lemma` and `inflect` methods for each spaCy `Token`. The methods operate similarly to the methods described above, with the exception that a string is returned, containing the most common spelling, rather than a tuple.
```
> import spacy
> import lemminflect
> nlp = spacy.load('en_core_web_sm')
> doc = nlp('I am testing this example.')
> doc[2]._.lemma()
test

> doc[4]._.inflect('NNS')
examples
```
