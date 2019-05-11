import sys


class ProgressBar(object):
    def __init__(self, end_val, bar_len=20):
        self.end_val = end_val
        self.bar_len = bar_len

    def update(self, val):
        percent = float(val) / self.end_val
        if percent > 1.0:
            percent = 1.0
        hashes = '#' * int(round(percent * self.bar_len))
        spaces = ' ' * (self.bar_len - len(hashes))
        sys.stdout.write('\rPercent: [{0}] {1}%'.format(hashes + spaces, int(round(100 * percent))))
        sys.stdout.flush()

    def clear(self):
        spaces = ' ' * (30 + self.bar_len)
        sys.stdout.write('\r{0}'.format(spaces))
        sys.stdout.write('\r')
