#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
import readline
import numpy
from   lemminflect.kmodels.ModelInflInData import ModelInflInData
from   lemminflect.kmodels.KerasModel import KerasModel
from   lemminflect import config


if __name__ == '__main__':

    # Load the model
    print('Loading ', config.model_infl_fn)
    model = KerasModel.load(config.model_infl_fn)
    print()

    # Put in the rules from the model]
    output_classes = model.meta['output_enum']

    # Run the model on user data
    print('Enter lemma,category predict the inflection type or q to quit')
    print('Where category is noun, verb, adj, adv')
    while 1:
        text = input('> ')
        if not text or text == 'q':
            break
        lemma, category = text.split(',')
        # process the data
        vec = ModelInflInData.wordToVec(lemma, category)
        vec = numpy.expand_dims(vec, 0)
        output = model.run(vec)[0]
        class_num = numpy.argmax(output)
        infl_type = output_classes[class_num]
        print('The inflection type is: ', infl_type)
        print()
