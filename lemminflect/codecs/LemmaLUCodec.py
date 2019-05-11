import gzip
from ..core.LexicalUtils import categoryToUPos


# Helper class for reading/writing the lookup csv file
class LemmaLUCodec(object):
    @staticmethod
    def fromString(line):
        word, category, forms = line.strip().split(',')
        forms = tuple(forms.split('/'))
        return word, category, forms

    @staticmethod
    def toString(word, category, forms):
        forms_str = ''
        for form in forms:
            forms_str += '%s/' % form
        forms_str = forms_str[:-1]
        line = '%s,%s,%s\n' % (word, category, forms_str)
        return line

    # Data format is word,category,lemma_spellings (separated by /)
    # Convert from the native "category" to upos on load
    @classmethod
    def load(cls, fn):
        lemma_dict = {}
        with gzip.open(fn, 'rb') as f:
            for line in f:
                line = line.decode()
                word, category, forms = cls.fromString(line)
                upos = categoryToUPos(category)
                if word not in lemma_dict:
                    lemma_dict[word] = {upos:forms}
                else:
                    lemma_dict[word].update( {upos:forms} )
        return lemma_dict
