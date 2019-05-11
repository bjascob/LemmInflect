#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
import numpy
from   lemminflect.kmodels.ModelLemma        import ModelLemma
from   lemminflect.kmodels.ModelLemmaInData  import ModelLemmaInData
from   lemminflect.kmodels.ModelLemmaClasses import ModelLemmaClasses
from   lemminflect import config


if __name__ == '__main__':
    # Load the lemmatization data
    print('Loading ', config.lemma_tcorp_fn)
    indata = ModelLemmaInData(config.lemma_tcorp_fn)
    print('Loaded {:,} entries'.format(len(indata.entries)))

    # Load the lemmatization rules
    print('Loading ', config.model_lemma_cl_fn)
    rules = ModelLemmaClasses(config.model_lemma_cl_fn)

    # Convert data into training format
    X = []
    Y = []
    input_len = ModelLemmaInData.WVEC_LEN
    input_letters = ModelLemmaInData.getLetterClasses()
    output_rules = rules.rules
    for entry in indata.entries:
        rule = ModelLemmaClasses.computeSuffixRule(entry.infl, entry.lemma)
        idx = rules.getRuleIndex(rule)
        vec = ModelLemmaInData.wordToVec(entry.infl, entry.category)
        X.append( vec )
        Y.append( idx )
    X = numpy.asarray(X, dtype='float32')
    Y = numpy.asarray(Y, dtype='int32')
    print('X.shape= ', X.shape)
    print('Y.shape= ', Y.shape)
    print()

    # Create the model
    batch_size = 32
    nepochs    = 50

    model = ModelLemma()
    model.create(input_len, input_letters, output_rules)
    model.model.summary()
    model.train(X, Y, batch_size, nepochs)
    print()

    print('Saving model to ', config.model_lemma_fn)
    model.save(config.model_lemma_fn)
    print('done')
