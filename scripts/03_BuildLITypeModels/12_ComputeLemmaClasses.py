#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')    # make '..' first in the lib search path
import gzip
from   lemminflect.kmodels.ModelLemmaInData  import ModelLemmaInData
from   lemminflect.kmodels.ModelLemmaClasses import ModelLemmaClasses
from   lemminflect.slexicon.SKey import *
from   lemminflect import config


if __name__ == '__main__':
    # Config
    print_debug = False

    print('Loading ', config.lemma_tcorp_fn)
    indata = ModelLemmaInData(config.lemma_tcorp_fn)
    print('Loaded {:,} entries'.format(len(indata.entries)))
    print()

    # Create Rule set
    print('Creating lemmatization rules')
    rule_set = set()
    for entry in indata.entries:
        il_rem, ll_add, is_doubled = ModelLemmaClasses.computeSuffixRule(entry.infl, entry.lemma)
        if print_debug:
            s1 = '%s->%s' % (entry.infl, entry.lemma)
            s2 = '  / doubled' if is_doubled else ''
            print('%-24s : %4s / %s %s' % (s1, il_rem, ll_add, s2))
        rule_set.add( (il_rem, ll_add, is_doubled) )
    print()

    # Save it
    print('{:,} total entries in rule set'.format(len(rule_set)))
    print('Saving rules to ', config.model_lemma_cl_fn)
    ModelLemmaClasses.saveFromRuleTuples(config.model_lemma_cl_fn, rule_set)
