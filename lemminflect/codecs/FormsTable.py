import re
import gzip


class FormsTable(object):
    def __init__(self, table_fn):
        self.data = self._load(table_fn)

    # Parse a a file of inflections with lines like...
    #   percentage,noun: (percentage,singular,reg)  (percentages,plural,reg)
    @staticmethod
    def _load(table_fn):
        data = {}   # key=(infl, category)  value=forms which are [inflection, infl_type, source]
        with gzip.open(table_fn, 'rb') as f:
            for line in f:
                line = line.decode()
                key, forms = line.split(':')
                base, category = key.split(',')
                forms = re.findall('\(.*?\)',forms)
                forms = [f[1:-1].split(',') for f in forms]
                # Load this into the lookup
                key = (base, category)
                if key not in data:
                    data[key] = forms
                else:
                    raise ValueError('Duplicate key for %s/%s' % (base,category))
        return data
