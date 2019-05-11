#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
import readline
import numpy
from   lemminflect.kmodels.ModelLemmaInData import ModelLemmaInData
from   lemminflect.core.LemmatizerRules     import LemmatizerRules
from   lemminflect import config


if __name__ == '__main__':

    # Create the lemmatizer
    lemmatizer = LemmatizerRules(kitype='keras')

    # Run the model on user data
    print('Enter an inflection to lemmatize or q to quit')
    print('After the inflection add a comma and then the category')
    print('Where category is noun, verb, adj, adv')
    while 1:
        text = input('> ')
        if not text or text == 'q':
            break
        infl, category = text.split(',')
        # process the data
        vec = ModelLemmaInData.wordToVec(infl, category)
        rnum, rstring = lemmatizer.kinfer.run(vec)
        print('Applying rnum=%d : %s' % (rnum, rstring))
        lemma = lemmatizer._applyRule(infl, rnum)
        print('Lemma is : ', lemma)
        print()
