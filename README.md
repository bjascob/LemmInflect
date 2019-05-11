# ![(icon)](https://github.com/bjascob/LemmInflect/blob/master/docs/images/icons8-citrus-80.png) &nbsp; LemmInflect

**A python module for English lemmatization and inflection.**

LemmInflect uses an extensive dictionary to lemmatize and inflect English words into forms specified by the user.  The module also works with out-of-vocabulary (OOV) words by applying neural network techniques to classify word forms and apply morphing rules.

The system acts as a standalone module or an extension to **[spaCy](https://spacy.io/).** The included methods allow the user to lemmatize words or inflect them based on Penn Treebank part-of-speech tags.  Alternate methods also allow retrieval of a tagged list of all inflections for a given lemma.

A more simplistic inflection only system is available as **[pyInflect](https://github.com/bjascob/pyInflect).**  LemmInflect was created to address some of the shortcoming of that project and add features, such as...

* Independence from the spaCy lemmatizer
* Neural nets to disambiguate out of vocab morphology
* Unigrams to dismabiguate spellings and multiple word forms

Unlike pyInflect, the new system is derived from the **[NIH's SPECIALIST Lexicon](https://lsg3.nlm.nih.gov/LexSysGroup/Projects/lexicon/current/web/index.html)** which contains an extensive set information on English word forms.



## Requirements and Installation
The only external requirement to run LemmInflect is `numpy` which is used for the matrix math that drives the neural nets.  These nets are relatively small and don't require significant CPU power to run.

To install do..

`pip3 install lemminflect`

The project was built and tested under Python 3 and Ubuntu but should run on any Linux, Windows, Mac, etc.. system.  It is untested under Python 2 but may function in that environment with minimal or no changes.

The code base also includes library functions and scripts to create the various data files and neural nets.  This includes such things as...
* Unigram Extraction from the Gutenberg and Billion Word Corpra
* Python scripts for loading and parsing the SPECIALIST Lexicon
* Nerual network training based on Keras and Tensorflow

If you want to use the setup scripts, there are additional dependencies such as NLTK, Keras, and Tensorflow (or other Keras backend).  None of these are required for run-time inflection or lemmatization.


## Usage as an Extension to Spacy
To use with Spacy, you need Spacy version 2.0 or later.  Versions 1.9 and earlier do not support the extension methods used here.

To use as an extension to Spacy, first import the module.  This will create new `lemma` and `inflect` methods for each spaCy `Token`.  The `inflect` method takes a Penn Treebank tag as its parameter.  That method returns the inflected form of the word based on the supplied treekbank tag.
```
> import spacy
> import lemminflect
> nlp = spacy.load('en_core_web_sm')
> tokens = nlp('I am testing this example.')
> tokens[2]._.lemma()
test

> tokens[4]._.inflect('NNS')
examples
```

## Usage Standalone
To use standalone, call the methods `getAllInflections` and/or  `getInflection`.  The first method returns all entries in the inflection lookup as a dictionary of forms, where each form entry is a tuple with one or more spellings/forms for a given treebank tag.  The optional parameter `upos` can be used to limited the returned data to specific parts of speech.  The method `getInflection` takes a lemma and a Penn Treebank tag and returns a tuple of the specific inflection(s) associated with that tag.  Similarly, the methods `getAllLemmas` and `getLemma` will return the lemma for the word.
```
> from lemminflect import getAllInflections, getInflection
> from lemminflect import getAllLemmas, getLemma
> getAllInflections('watch')
{'NN': ('watch',), 'NNS': ('watches', 'watch'), 'VB': ('watch',), 'VBD': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',),  'VBP': ('watch',)}

> getAllInflections('watch', upos='VERB')
{'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)}

> getInflection('watch', tag='VBD')
('watched',)

> getAllLemmas('watches')
{'NOUN': ('watch',), 'VERB': ('watch',)}

getLemma('watches', upos='VERB')
('watch',)
```
When the tuple contains multiple words, they are sorted by their unigram corpus probability so the first form (`form[0]`) is the most common.

For a list of methods and parameters see the section below.

## Issues
If you find a bug, please report it on the **[GitHub issues list](https://github.com/bjascob/LemmInflect/issues)**.  However be aware that when in comes to returning the correct inflection there are a number of different types of issues that can arise.  Some of these are not  readily fixable.  Issues with inflected forms include...
* Multiple spellings for an inflection (ie.. arthroplasties, arthroplastyes or arthroplastys)
* Mass form and plural types (ie.. people vs peoples)
* Forms that depend on context (ie.. further vs farther)
* Infections that are not fully specified by the tag (ie.. be/VBD can be "was" or "were")

One common issue is that some forms of the verb "be" are not completely specified by the treekbank tag.  For instance be/VBD inflects to either "was" or "were" and be/VBP inflects to either "am", or "are".  In order to disambiguate these forms, other words in the sentence need to be inspected.  At this time, LemmInflect doesn't include this functionality.


## Tags
The module determines the inflection(s) returned by suppling either a **[Universal Dependencies](https://universaldependencies.org/u/pos/)** or **[Penn Treebank](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)** tag.  Not all of the tags in these sets are used by LemmInflect.  The following is a list of the various types and tags used...

    upos = 'ADJ'
    * JJ      Adjective
    * JJR     Adjective, comparative
    * JJS     Adjective, superlative

    upos = 'ADV'
    * RB      Adverb
    * RBR     Adverb, comparative
    * RBS     Adverb, superlative

    upos = 'NOUN'
    * NN      Noun, singular or mass
    * NNS     Noun, plural
    *
    upos = 'PROPN'
    * NNP     Proper noun, singular or mass
    * NNPS    Proper noun, plural

    upos = 'VERB', 'AUX'
    * VB      Verb, base form
    * VBD     Verb, past tense
    * VBG     Verb, gerund or present participle
    * VBN     Verb, past participle
    * VBP     Verb, non-3rd person singular present
    * VBZ     Verb, 3rd person singular present
    * MD      Modal

## Function Reference
Note the `Lemmatizer` and `Inflections` objects are implemented as singletons so you can safely instantiate them multiple times.  Data files are lazy loaded and will only be loaded with the first instance created.
```
Methods from lemminflect that utilize the Lemmatizer() class
    def getAllLemmas(word, upos=None)
    def getAllLemmasOOV(word, upos)
    def getLemma(word, upos, lemmatize_oov=True)
    def spacy.Token._.lemma(form_num=0, lemmatize_oov=True, on_empty_ret_word=True)

Methods from lemminflect that use the Inflections() class
    def getAllInflections(lemma, upos=None)
    def getAllInflectionsOOV(lemma, upos)
    def getInflection(lemma, tag, inflect_oov=True)
    def spacy.Token._.inflect(tag, form_num=0, inflect_oov=True, on_empty_ret_word=True)
    def setUseInternalLemmatizer(TF=True)

Parameters for these functions are..
    upos : Universal Dependencies part of speech the return is limited to.
    tag :  The Penn Treekbank tag used to specify the returned word form.
    lemmatize_oov / inflect_oov : When False, only the dictionary will be used, not the OOV/rules system.
    form_num : When multiple spellings exist, this determines which is returned.
    on_empty_ret_word : If no result is found, return the original word.
```
For inflections, the word is first internally lemmatized to it's base form and then inflected to the requested form.  The function `setUseInternalLemmatizer` determines if the spaCy extension method `inflect` uses the spaCy lemmatizer or LemmInflect's.
