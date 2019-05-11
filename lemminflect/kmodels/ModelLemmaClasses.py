

class ModelLemmaClasses(object):
    def __init__(self, fn=None):
        self.rules = []         # list of strings
        if fn is not None:      # load from file
            self.rules = self._load(fn)
        # Create a dictionary of rules for quick index lookup
        self.rules_dict = {r:i for i, r in enumerate(self.rules)}

    # Get the class index of the rule for either a tuple or string
    def getRuleIndex(self, rule):
        if isinstance(rule, tuple):
            rule = self._tupleToCSV(rule)
        return self.rules_dict[rule]

    # Look at the difference between the inflection and the leamm and figure out
    # letters to remove, add and if it follows the doubling rule
    @staticmethod
    def computeSuffixRule(infl, lemma):
        # Figure out the common letters and the differences in the
        # inflection letters and the lemma letters
        ncomm = min(len(infl), len(lemma))
        for i in range(ncomm):
            if infl[i] != lemma[i]:
                ncomm = i
                break
        common = infl[:ncomm]
        il_rem = infl[ncomm:]
        ll_add = lemma[ncomm:]
        # Now handle the special case where the last letter is doubled
        # Without this all the regular-doubled form rules have an entry
        # for each possible letter, or at least what's in the train set.
        is_doubled = False
        if il_rem and il_rem[0] == common[-1]:
            is_doubled = True
            il_rem = il_rem[1:]
        return il_rem, ll_add, is_doubled

    # Save the set of rules in sorted order
    @classmethod
    def saveFromRuleTuples(cls, fn, rules):
        assert isinstance(rules, set)
        with open(fn, 'w') as f:
            for rule in sorted(rules):
                string = cls._tupleToCSV(rule)
                f.write('%s\n' % string)

    # Load the rules
    @staticmethod
    def _load(fn):
        rules = []
        with open(fn) as f:
            for line in f:
                line = line.strip()
                rules.append(line)
        return rules

    # Convert a tuple to a csv string
    @staticmethod
    def _tupleToCSV(t):
        return '%s,%s,%s' % (t[0], t[1], t[2])
