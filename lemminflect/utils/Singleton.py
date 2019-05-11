# See https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
# This version should be compatible with both Python 2 and 3

class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass
