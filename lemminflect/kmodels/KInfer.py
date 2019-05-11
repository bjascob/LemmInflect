from   abc import ABC, abstractmethod
import numpy as np
from   .KerasModel import limitTFMem
from   ..utils.DataContainer import DataContainer


# Factory style method for creating the KInfer object
def getKInferInstance(kitype, model_fn):
    if kitype == 'numpy':
        return KInferWithNumpy(model_fn)
    elif kitype == 'keras':
        return KInferWithKeras(model_fn)
    else:
        raise ValueError('Unhandled kitype = ' % kitype)


# Base class for Keras model inference
class KInfer(ABC):
    def __init__(self):
        self.meta = None

    # Run the input vector through the model.
    # This returns the argmax and the enumerated output strings.
    @abstractmethod
    def run(self, in_vec):
        pass

    # Return the output enumeration string
    def getOutputEnum(self):
        return self.meta['output_enum']

    # Load the model data from the DataContainer
    def _loadModelContainer(self, fn):
        dc = DataContainer.load(fn)
        self.meta = dc.meta
        return dc.config, dc.weights

    # Convert the network's output vector to an index and string
    def _netOutToValue(self, vec):
        index = np.argmax(vec)
        string = self.getOutputEnum()[index]
        return index, string


# Keras based inference
class KInferWithKeras(KInfer):
    def __init__(self, fn):
        super(KInferWithKeras, self).__init__()
        self._load(fn)

    def run(self, in_vec):
        X = np.expand_dims(in_vec, 0)
        Y = self.model.predict(X, verbose=0)
        return self._netOutToValue(Y[0])

    def _load(self, fn):
        import keras    # Lazy import keras
        if keras.backend.backend() == 'tensorflow':
            limitTFMem()
        config, weights = self._loadModelContainer(fn)
        self.model = keras.Model.from_config(config)
        self.model.set_weights(weights)



# Numpy based inference.
# Note that keras supports a lot of complicated model configurations.  This class in only
# setup to handle the very limited subset used in LemmInflect
class KInferWithNumpy(KInfer):
    def __init__(self, fn):
        super(KInferWithNumpy, self).__init__()
        self.config, self.weights = self._loadModelContainer(fn)

    def run(self, in_vec):
        layers = self.config['layers']
        # input layer
        assert layers[0]['class_name'] == 'InputLayer'
        in_shape = layers[0]['config']['batch_input_shape'] # (None, nsteps, nfeats)
        assert in_shape[1] == in_vec.shape[0]
        assert in_shape[2] == in_vec.shape[1]
        x = in_vec
        # Remaining dense or flatten layers
        wnum = 0
        for layer in layers[1:]:
            ltype = layer['class_name']
            if ltype == 'Flatten':
                x = flatten(x)
            elif ltype == 'Dense':
                W = self.weights[wnum]
                b = self.weights[wnum+1]
                wnum += 2
                x = np.dot(x, W) + b
                x = applyActivation(x, layer['config']['activation'])
        return self._netOutToValue(x)

    def _printModelData(self):
        print('Weights:')
        for weight in self.weights:
            print('  ', weight.shape)
        print('Config:')
        for k, v in self.config.items():
            if k == 'layers':
                for layer in v:
                    print('   layer = ', layer)
            else:
                print('  ', k,v)


### Misc functions used in computing the net ###
def flatten(x):
    return np.reshape(x, (-1,))

def relu(x):
    return x * (x > 0)

def softmax(x, axis=-1):
    y = np.exp(x - np.max(x, axis, keepdims=True))
    return y / np.sum(y, axis, keepdims=True)

def applyActivation(x, atype):
    if atype == 'relu':
        return relu(x)
    elif atype == 'softmax':
        return softmax(x)
    else:
        raise ValueError('Unhandled activation type = %s' % atype)
