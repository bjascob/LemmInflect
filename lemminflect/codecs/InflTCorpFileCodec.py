import gzip


class Entry(object):
    def __init__(self, lemma, category, source):
        self.lemma    = lemma
        self.category = category
        self.source   = source


# Helper class for reading/writing the lookup csv file
class InflTCorpFileCodec(object):
    @staticmethod
    def fromString(line):
        lemma, category, source = line.strip().split(',')
        return lemma, category, source

    @staticmethod
    def toString(lemma, category, source):
        line = '%s,%s,%s\n' % (lemma, category, source)
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
