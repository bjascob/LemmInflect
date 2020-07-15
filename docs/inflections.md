
# The Inflection API

The `Inflection` class converts words from their base form to a user-specified inflection type.  The class aggregates dictionary based lookup and rule based inflections, including the nerual-network models used to select the appropriate rules.  It is implemented as a singleton that is instantiated for the first time when you call any of its methods from `lemminflect`.

Only the base form of a word can be inflected and the library methods here expect the incoming word to be a lemma.  If your word is not in its base form, first call the [lemmatizer](lemmatizer.md) to get the base form.  When using the spaCy extension, lemmatization is handled internally.


## Examples
Usage as a library
```
> from lemminflect import getInflection, getAllInflections, getAllInflectionsOOV
> getInflection('watch', tag='VBD')
('watched',)

> getAllInflections('watch')
{'NN': ('watch',), 'NNS': ('watches', 'watch'), 'VB': ('watch',), 'VBD': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',),  'VBP': ('watch',)}

> getAllInflections('watch', upos='VERB')
{'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)}

> getAllInflectionsOOV('xxwatch', upos='NOUN')
{'NN': ('xxwatch',), 'NNS': ('xxwatches',)}
```

Usage as a extension to spaCy
```
> import spacy
> import lemminflect
> nlp = spacy.load('en_core_web_sm')
> doc = nlp('I am testing this example.')
> doc[4]._.inflect('NNS')
examples
```

##  Methods
**getInflection**
```
getInflection(lemma, tag, inflect_oov=True)
```
The method returns the inflection for the given lemma based on te PennTreebank tag.  It first calls `getAllInflections` and if none were found, calls `getAllInflectionsOOV`.  The flag allows the user to disable the rules based inflections.  The return from the method is a tuple of different spellings for the inflection.

Arguments

* lemma: the word to inflect
* tag: the Penn-Treebank tag
* inflect_oov: if `False` the rules sytem will not be used.


**getAllInflections**
```
getAllInflections(lemma, upos=None)
```
This method does a dictionary lookup of the word and returns all lemmas.  Optionally, the `upos` tag may be used to limit the returned values to a specific part-of-speech.  The return value is a dictionary where the key is the Penn Treebank tag and the value is a tuple of spellings for the inflection.

Arguments

* **lemma:** the word to inflect
* **upos:** Universal Dependencies part of speech tag the returned values are limited to

**getAllInflectionsOOV**
```
getAllInflectionsOOV(lemma, upos)
```
Similary to `getAllInflections`, but uses the rules system to inflect words.

Arguments

* **lemma:** the word to inflect
* **upos:** Universal Dependencies part of speech tag the returned values are limited to


**Spacy Extension**
```
Token._.inflect(tag, form_num=0, inflect_oov=True, on_empty_ret_word=True)

```
The extension is setup in spaCy automatically when `lemminflect` is imported.  The above function defines the method added to `Token`.  Internally spaCy passes token information to a method in `Inflections` which first lemmatizes the word.  It then calls `getInflection` and then returns the specified form number (ie.. the first spelling).

Arguments

* **form_num:** When multiple spellings exist, this determines which is returned
* **inflect_oov:** When `False`, only the dictionary will be used, not the OOV/rules system
* **on_empty_ret_word:** If no result is found, return the original word

**setUseInternalLemmatizer**
```
setUseInternalLemmatizer(TF=True)
```
To inflect a word, it must first be lemmatized.  To do this the spaCy extension calls the lemmatizer.  Either the internal lemmatizer or spaCy's can be used.  This function only impacts the behavior of the extension.  No lemmatization is performed in the library methods.

Arguments

* TF: If `True`, use the LemmInflect lemmatizer, otherwise use spaCy's
