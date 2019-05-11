import  numpy
from    ..utils.DataContainer import DataContainer


# Set tensorflow configs to only grow the memory to what is needed.
# Alternately, a specific amount can be set initially.
# It's not clear from the docs if the memory will grow beyond the amount
# set by per_process_gpu_memory_fraction (ie.. this may disable "allow_growth")
# (by default tensorflow allocates all available memory)
def limitTFMem(pct_mem_res=None):
    # Lazy import tensorflow
    import  tensorflow as tf
    config = tf.ConfigProto()
    if pct_mem_res:
        config.gpu_options.per_process_gpu_memory_fraction=pct_mem_res
    config.gpu_options.allow_growth=True
    tf.Session(config=config)


class KerasModel(object):
    def __init__(self):
        self.model = None
        self.meta  = {}

    # Load the extended model from a file
    @classmethod
    def load(cls, filename):
        import keras    # Lazy import keras
        limitTFMem()
        self = cls()
        dc = DataContainer.load(filename)
        self.meta  = dc.meta
        self.model = keras.Model.from_config(dc.config)
        self.model.set_weights(dc.weights)
        return self

    # Save the extended model to a file.  This saves the keras model data plus extra meta-data.
    # Doing it this way doesn't keep the training config / optimizer.  The model would have to be
    # recompiled before it could be trained any more.
    # Saving the data this way is about 1/3 the size of a standard keras .hdf5 file and gzipping
    # gives another 5-10% size decrease.
    def save(self, filename):
        dc = DataContainer()
        dc.meta    = self.meta
        dc.config  = self.model.get_config()
        dc.weights = self.model.get_weights()
        dc.save(filename)

    # Get the input shape (ie.. 3D sample#, word#, wvec#)
    def getInputShape(self):
        return self.model.get_input_shape_at(0)

    # Model takes in multiple list of vectors  (ie. 3D matrix = sample#, word#, wordvec)
    # Returns an output vector for each sample (ie. 2D matrix = sample#, outvec)
    def run(self, inputMat3D):
        X = numpy.asarray( inputMat3D )
        Y = self.model.predict(X, verbose=0)
        return Y
