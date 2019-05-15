
# Part-Of-Speech Tags
The module determines the lemma(s) and inflection(s) returned by supplying either a [Universal Dependencies](https://universaldependencies.org/u/pos/) or [Penn Treebank](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) tag.  Not all of the tags in these sets are used by LemmInflect.  The following is a list of the various types and tags used...

## Tag Sets
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


## A Note on AUX and MODAL types
Verbs can be further subdivided into auxiliary verbs, some of which can be modal auxiliary verbs<br/>
The Penn Treebank tags have 'MD' but no 'AUX' category<br/>
UPOS tags have 'AUX' but no 'MD'<br/>
The SPECIALIST Lexicon's "category" system has both<br/>
To make things more confusing, tagging of will often label these words as verbs.  Luckily the list of these words is small.
* AUX verbs: have(has, had), be(is, was, been), do(does, did)
* MODAL verbs: can, could, may, might, will, would, shall, should, must, ought, dare
