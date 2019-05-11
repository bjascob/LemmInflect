
# Simple reader/writer for lemma and inflection overrides
class OverridesCodec(object):
    @staticmethod
    def toString(word_in, pos, word_out):
        return '%s,%s,%s\n' % (word_in, pos, word_out)

    @staticmethod
    def load(fn):
        d = {}
        with open(fn) as f:
            for line in f:
                line = line.strip()
                if not line or line[0] == '#':
                    continue
                word_in, pos, word_out = line.split(',')
                entry = {pos:(word_out,)}
                if word_in not in d:
                    d[word_in] = entry
                else:
                    d[word_in].update( entry )
        return d
