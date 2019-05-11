from collections import Counter
from ..core.LexicalUtils import catAndTypeToTag
from ..slexicon.SKey import *

class Unigrams(object):
    def __init__(self, fn):
        self.counter      = self.load(fn)
        self.counter_word = self.convertToWordKey(self.counter)

    # Get the counts for a word. Optional tag is the penn treebank pos
    def getCount(self, word, tag=None):
        if tag is not None:
            return self.counter.get((word,tag), 0)
        else:
            return self.counter_word.get((word), 0)

    # Get the counts for the base word (ie. lemma) given the SPECIALIST Lexicon's category
    # !! Note that for nouns, this looks at the first letter to determine if it's a proper
    # noun or not.  This works for the look-up tables where everyhing is normalized but
    # will cause a problem if trying to use this on a sentence (ie.. first word capitalized).
    def getCountForLemma(self, word, category):
        count = 0
        if category == SKey.VERB:
            count += self.getCount(word, 'VB')
            count += self.getCount(word, 'MD')
        elif category == SKey.ADJ:
            count += self.getCount(word, 'JJ')
        elif category == SKey.ADV:
            count += self.getCount(word, 'RB')
        elif category == SKey.NOUN:
            if word and word[0].isupper():
                count += self.getCount(word, 'NNP')
            else:
                count += self.getCount(word, 'NN')
        return count

    # Get the counts for the word given the SPECIALIST Lexicon's category and and inflection type
    def getCountForInflections(self, word, category, infl_type):
        count = 0
        is_proper = word[0].isupper()
        tags = catAndTypeToTag(category, infl_type, is_proper)
        for tag in tags:
            count += self.getCount(word, tag)
        return count

    # Save the class instance's counter to a file
    def save(self, fn, min_count=1):
        self.saveCounter(fn, self.counter, min_count)

    # Save a counter object to a csv file
    @staticmethod
    def saveCounter(fn, counter, min_count=1):
        with open(fn, 'w') as f:
            for key, count in counter.most_common():
                if count >= min_count:
                    f.write('%d,%s,%s\n' % (count, key[0], key[1]))

    # Load the data from a csv
    @staticmethod
    def load(fn):
        counter = Counter()
        with open(fn) as f:
            for line in f:
                parts = line.strip().split(',')
                # Weed out empty lines and words with commas in them
                if not parts or len(parts) != 3:
                    continue
                # Add to counter
                key = (parts[1], parts[2])
                count = int(parts[0])
                counter[key] = count
        return counter

    # create a second counter that uses only the word as a key
    @staticmethod
    def convertToWordKey(counter):
        counter_word = Counter()
        for key, count in counter.items():
            word, _ = key
            counter_word[word] += count
        return counter_word
