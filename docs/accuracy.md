# Accuracy of the Lemmatizer

The accuracy of LemmInflect and several other popular NLP utilities was tested using the
[Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other) as a
baseline. This is not a "gold" standard dataset but it has an extensive list of
lemmas and their corresponding inflections and appears to be generaly a "good" set for testing.
Each inflection was lemmatized by the test software and then compared to the original value in the
corpus. The test included 119,194 different inflected words.

## Results
```
| Package                      | Verb  |  Noun | ADJ/ADV | Overall |  Speed   |
|-----------------------------------------------------------------------------|
| LemmInflect 0.2.3            | 96.1% | 95.4% |  93.9%  |  95.6%  |  42.0 uS |
| Stanza 1.5.0 + CoreNLP 4.5.2 | 94.0% | 96.4% |  93.1%  |  95.5%  |  30.0 us |
| spaCy 3.5.0                  | 79.5% | 88.9% |  60.5%  |  84.7%  | 393.0 uS |
| NLTK 3.8.1                   | 53.3% | 52.2% |  53.3%  |  52.6%  |  12.0 uS |
|-----------------------------------------------------------------------------|
```
Speed is in micro-seconds per lemma and was conducted on a i9-7940x CPU. Note since Stanza is making
calls to the java CoreNLP software, all 120K test cases were grouped into a single call. For Spacy,
all pipeline components were disabled except the lemmatizer, but the high per lemma time is probably
a reflection of the generally overhead of the pipeline architecture.

## Notes on test conditions:
The test corpus has almost 120K words, which is more than the typical vocabulary. It's likely the
software packages tested will not have many of these words in their online corpus. Because of this,
the words will be treated as "out-of-vocabulary" which generally produces less reliable lemmatization.
Re-running tests with a smaller vocabulary will yield higher scores across the tested packages.

The corpus does not include the lemma itself as a test case. In some software tasks you may lemmatize
a lemma but those conditions are not simulated here. Including lemmas in the test corpus yields higher
scores across-the-board.
