# ![(icon)](docs/img/favicon.ico) &nbsp; LemmInflect

**A python module for English lemmatization and inflection.**


## About
LemmInflect uses a dictionary approach to lemmatize English words and inflect them into forms specified by a user supplied [Universal Dependencies](https://universaldependencies.org/u/pos/) or [Penn Treebank](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) tag.  The library works with out-of-vocabulary (OOV) words by applying neural network techniques to classify word forms and choose the appropriate morphing rules.

The system acts as a standalone module or as an extension to the [spaCy](https://spacy.io/) NLP system.

The dictionary and morphology rules are derived from the [NIH's SPECIALIST Lexicon](https://lsg3.nlm.nih.gov/LexSysGroup/Projects/lexicon/current/web/index.html) which contains an extensive set information on English word forms.

A more simplistic inflection only system is available as [pyInflect](https://github.com/bjascob/pyInflect).  LemmInflect was created to address some of the shortcoming of that project and add features, such as...

* Independence from the spaCy lemmatizer
* Neural nets to disambiguate out of vocab morphology
* Unigrams to dismabiguate spellings and multiple word forms


## Documentation
For the latest documentation, see **[ReadTheDocs](https://lemminflect.readthedocs.io/en/latest/)**.


## Accuracy of the Lemmatizer
The accuracy of LemmInflect and several other popular NLP utilities was tested using the [Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other) as a baseline.  The AGID has an extensive list of lemmas and their corresponding inflections.  Each inflection was lemmatized by the test software and then compared to the original value in the corpus. The test included 119,194 different inflected words.

```
| Package          | Verb  |  Noun | ADJ/ADV | Overall |  Speed  |
|----------------------------------------------------------------|
| LemmInflect      | 96.1% | 95.4% |  93.9%  |  95.6%  | 42.0 uS |
| CLiPS/pattern.en | 93.6% | 91.1% |   0.0%  |  n/a    |  3.0 uS |
| Stanford CoreNLP | 87.6% | 93.1% |   0.0%  |  n/a    |  n/a    |
| spaCy            | 79.4% | 88.9% |  60.5%  |  84.7%  |  5.0 uS |
| NLTK             | 53.3% | 52.2% |  53.3%  |  52.6%  | 13.0 uS |
|----------------------------------------------------------------|
```
* Speed is in micro-seconds per lemma and was conducted on a i9-7940x CPU.
* The Stanford and CLiPS lemmatizers don't accept part-of-speech information and in the case of the pattern.en, the methods was setup specifically for verbs, not as a lemmatizer for all word types.
* The Stanford CoreNLP lemmatizer is a Java package and testing was done via the built-in HTML server, thus the speed measurement is invalid.


## Requirements and Installation
The only external requirement to run LemmInflect is `numpy` which is used for the matrix math that drives the neural nets.  These nets are relatively small and don't require significant CPU power to run.

To install do..

`pip3 install lemminflect`

The project was built and tested under Python 3 and Ubuntu but should run on any Linux, Windows, Mac, etc.. system.  It is untested under Python 2 but may function in that environment with minimal or no changes.

The code base also includes library functions and scripts to create the various data files and neural nets.  This includes such things as...
* Unigram Extraction from the Gutenberg and Billion Word Corpra
* Python scripts for loading and parsing the SPECIALIST Lexicon
* Nerual network training based on Keras and Tensorflow

None of these are required for run-time operation.  However, if you want of modify the system, see the [documentation](https://lemminflect.readthedocs.io/en/latest/test_dev/) for more info.


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
The library provides lower-level functions to access the dictionary and the OOV rules directly.  For a detailed description see [Lemmatizer](https://lemminflect.readthedocs.io/en/latest/lemmatizer/) or [Inflections](https://lemminflect.readthedocs.io/en/latest/inflections/).


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

## Issues
If you find a bug, please report it on the [GitHub issues list](https://github.com/bjascob/LemmInflect/issues).  However be aware that when in comes to returning the correct inflection there are a number of different types of issues that can arise.  Some of these are not  readily fixable.  Issues with inflected forms include...
* Multiple spellings for an inflection (ie.. arthroplasties, arthroplastyes or arthroplastys)
* Mass form and plural types (ie.. people vs peoples)
* Forms that depend on context (ie.. further vs farther)
* Infections that are not fully specified by the tag (ie.. be/VBD can be "was" or "were")

One common issue is that some forms of the verb "be" are not completely specified by the treekbank tag.  For instance be/VBD inflects to either "was" or "were" and be/VBP inflects to either "am", or "are".  In order to disambiguate these forms, other words in the sentence need to be inspected.  At this time, LemmInflect doesn't include this functionality.
