
# The Lemmatizer API

The `Lemmatizer` class converts words from their inflected form to their base form.  The class aggregates dictionary based lookup and rule based lemmatization, including the nerual-network models used to select the appropriate rules.  It is implemented as a singleton that is instantiated for the first time when you call any of its methods from `lemminflect`.


## Examples
Usage as a library
```
> from lemminflect import getLemma, getAllLemmas, getAllLemmasOOV, isTagBaseForm
> getLemma('watches', upos='VERB')
('watch',)

> getAllLemmas('watches')
{'NOUN': ('watch',), 'VERB': ('watch',)}

> getAllLemmasOOV('xatches', 'NOUN')
{'NOUN': ('xatch',)}

> isTagBaseForm('JJ')
True
```
Usage as a entension to spaCy
```
> import lemminflect
> import spacy
> nlp = spacy.load('en_core_web_sm')
> doc = nlp('I am testing this example.')
> doc[2]._.lemma()
test
```

##  Methods
**getLemma**
```
getLemma(word, upos, lemmatize_oov=True)
```
This methods aggregates `getAllLemmas` and `getAllLemmasOOV`.  It first tries to find the lemma using the dictionary based lookup.  If no forms are available, it then tries to find the lemma using the rules system.  If a Penn Tag is available, it is best practice to first call `isTagBaseForm` (below), and only call this function if that is `False`.  Doing this will eliminate potentials errors from lemmatizing a word already in lemma form.

Arguments

* **word:** word to lemmatize
* **upos:** Universal Dependencies part of speech the return is limited to
* **lemmatize_oov:** Allow the method to use the rules based lemmatizer for words not in the dictionary

**getAllLemmas**
```
getAllLemmas(word, upos=None)
```
Returns lemmas for the given word.  The format of the return is a dictionary where each key is the `upos` tag and the value is a tuple of possible spellings.

Arguments

* **word:** word to lemmatize
* **upos:** Universal Dependencies part of speech tag the returned values are limited to

**getAllLemmasOOV**
```
getAllLemmasOOV(word, upos)
```
Similar to `getAllLemmas` except that the rules system is used for lemmatization, instead of the dictionary.  The return format is the same as well.

Arguments

* **word:** word to lemmatize
* **upos:** Universal Dependencies part of speech tag the returned values are limited to

**isTagBaseForm**
```
isTagBaseForm(tag)
```
Returns `True` or `False` if the Penn Tag is a lemma form.  This is useful since lemmatizing a lemma can lead to errors.  The upos tags used in the above methods don't have enough information to determine this, but the Penn tags do.

Arguments

* **tag** Penn Treebank tag

**Spacy Extension**
```
Token._.lemma(form_num=0, lemmatize_oov=True, on_empty_ret_word=True)
```
The extension is setup in spaCy automatically when LemmInflect is imported.  The above function defines the method added to `Token`.  Internally spaCy passes the `Token` to a method in `Lemmatizer` which in-turn calls `getLemma` and then returns the specified form number (ie.. the first spelling).  For words who's Penn tag indicates they are already in lemma form, the original word is returned directly.

* **form_num:** When multiple spellings exist, this determines which is returned.  The spellings are ordered from most common to least, as determined by a corpus unigram at the time the dictionary was created.
* **lemmatize_oov:** Allows the method to use the rules based system for words not in the dictionary
* **on_empty_ret_word:** If `True` and the word can not be lemmatized, return the original word.  If `False`, return `None`.  Note that many words like pronouns, nummbers, etc.. do not lemmatize.
