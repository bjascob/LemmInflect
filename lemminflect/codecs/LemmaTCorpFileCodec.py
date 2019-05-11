import gzip

class Entry(object):
    def __init__(self, infl, category, source, lemma):
        self.infl     = infl
        self.category = category
        self.source   = source
        self.lemma    = lemma


# Helper class for reading/writing the lookup csv file
class LemmaTCorpFileCodec(object):
    @staticmethod
    def fromString(line):
        infl, category, source, lemma = line.strip().split(',')
        return infl, category, source, lemma

    @staticmethod
    def toString(infl, category, source, lemma):
        line = '%s,%s,%s,%s\n' % (infl, category, source, lemma)
        return line

    # Load data from disk
    @classmethod
    def load(cls, fn):
        entries = []
        with gzip.open(fn, 'rb') as f:
            for line in f:
                line = line.decode()
                data = cls.fromString(line)
                entry = Entry(*data)
                entries.append( entry )
        return entries
