#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
import numpy
from   lemminflect.kmodels.ModelInfl       import ModelInfl
from   lemminflect.kmodels.ModelInflInData import ModelInflInData
from   lemminflect.slexicon.SKey import *
from   lemminflect import config


if __name__ == '__main__':

    # Load the inflection data
    print('Loading ', config.infl_tcorp_fn)
    indata = ModelInflInData(config.infl_tcorp_fn)
    print('Loaded {:,} entries'.format(len(indata.entries)))

    # Convert data into training format
    X = []
    Y = []
    input_len = ModelInflInData.WVEC_LEN
    input_letters  = ModelInflInData.getLetterClasses()
    output_classes = [SKey.REG, SKey.REGD, SKey.GLREG]
    output_dict    = {k:i for i,k in enumerate(output_classes)}
    for entry in indata.entries:
        vec = ModelInflInData.wordToVec(entry.lemma, entry.category)
        idx = output_dict[entry.source]
        X.append( vec )
        Y.append( idx )
    X = numpy.asarray(X, dtype='float32')
    Y = numpy.asarray(Y, dtype='int32')
    print('X.shape= ', X.shape)
    print('Y.shape= ', Y.shape)
    print()

    # Create the model
    batch_size = 32
    nepochs    = 20

    model = ModelInfl()
    model.create(input_len, input_letters, output_classes)
    model.model.summary()
    model.train(X, Y, batch_size, nepochs)
    print()

    print('Saving model to ', config.model_infl_fn)
    model.save(config.model_infl_fn)
    print('done')
