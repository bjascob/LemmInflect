import gzip
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

# This class is designed to to save and load generic python objects.  Data may
# be added to a class instance simple by appending an attributes.  The data
# can be save as a standard pickle or gziped pickle.
# Args : obj (object): Optional object who's non-private attributes will be copied
class DataContainer(object):
    def __init__(self, obj=None):
        if obj is not None:
            for key, value in vars(obj).items():
                if not key.startswith('_'):
                    setattr(self, key, value)

    # Save the data to a file.
    def save(self, filename):
        with self._open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Load the data from a file
    @classmethod
    def load(cls, filename):
        with cls._open(filename, 'rb') as f:
            dc = cls()
            dc.__dict__ = pickle.load(f)
        return dc

    @staticmethod
    def _open(filename, mode):
        if filename.split('.')[-1] == 'gz':
            return gzip.open(filename, mode)
        return open(filename, mode)
