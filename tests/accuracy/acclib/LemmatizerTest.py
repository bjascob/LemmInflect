

class Entry(object):
    def __init__(self, infl, pos_type, upos_list, lemma):
        self.infl      = infl
        self.pos_type  = pos_type
        self.upos_list = upos_list
        self.lemma     = lemma


# Simple class to provide a common test to mechanism for multiple libraries
# Note this is iter and len methods so it can be iterated over for test cases.
class LemmatizerTest(object):
    def __init__(self, fn):
        self.entries = self._load(fn)
        self.resetTest()

    # Clear all scores and reset the pointer to 0
    def resetTest(self):
        self.entry_ptr = 0
        self.lemma_no_ret  = 0
        self.lemma_errors  = 0
        self.lemma_err_set = set()
        self.van_counts    = [0,0,0]
        self.van_errors    = [0,0,0]

    # Note that test_lemmas is a list since in some cases we don't know
    # if the word is adj or adv
    def addResult(self, entry, possible_lemmas):
        vidx = self.vanIdx(entry.pos_type)
        self.van_counts[vidx] += 1
        if not possible_lemmas:
            self.lemma_no_ret += 1
            self.van_errors[vidx] += 1
            self.lemma_errors += 1
        elif entry.lemma not in possible_lemmas:
            self.van_errors[vidx] += 1
            self.lemma_errors += 1
            plemmas_str = '/'.join(sorted(possible_lemmas))
            self.lemma_err_set.add((entry.infl, entry.lemma, entry.pos_type, plemmas_str))

    @staticmethod
    def vanIdx(pos_type):
        return 'VAN'.index(pos_type)

    @staticmethod
    def vanUPOS(idx):
        return ['VERB', 'ADJ/ADV', 'NOUN'][idx]

    # returns inflection, [possible upos] (because adv/adj is unknown)
    def __iter__(self):
        while True:
            if self.entry_ptr < len(self.entries):
                entry = self.entries[self.entry_ptr]
                self.entry_ptr += 1
                yield entry
            else:
                self.entry_ptr = 0                
                return

    def __len__(self):
        return len(self.entries)

    @staticmethod
    def _toUPOS(pos_type):
        if pos_type == 'V':
            return ['VERB']
        elif pos_type == 'A':
            return ['ADJ', 'ADV']
        elif pos_type == 'N':
            return ['NOUN']
        else:
            assert False, 'Invalid pos_type = %s' % pos_type

    @classmethod
    def _load(cls, fn):
        entries = []
        with open(fn) as f:
            for line in f:
                infl, pos_type, lemma = line.strip().split(',')
                upos_list = cls._toUPOS(pos_type)
                entry = Entry(infl, pos_type, upos_list, lemma)
                entries.append(entry)
        return entries
