from .KerasModel   import KerasModel, limitTFMem


# Model what words need a determiner before them
class ModelInfl(KerasModel):
    def __init__(self):
        super(ModelInfl, self).__init__()

    # Construct the model
    # class_names is a list of each class's name in the output
    def create(self, input_len, input_letters, output_classes):
        # Lazy import keras
        from    keras import Input, Model
        from    keras.layers  import Dense, Flatten
        limitTFMem()

        # Save the names of the output classes for later use (attrib_dict in base class)
        self.meta['input_enum']  = input_letters
        self.meta['output_enum'] = output_classes

        # Setup the sizes of the network
        input_shape = (input_len, len(input_letters))
        dense1_dim  = 64
        output_dim  = len(output_classes)

        # Build the model
        # Note that the loading using keras.Model.from_config() didn't work with the Sequential
        # model, I had to use the functional API.
        inputs  = Input(shape=input_shape, name='input')
        flatten = Flatten(name='flatten')(inputs)
        dense1  = Dense(dense1_dim, activation='relu', name='dense1')(flatten)
        outputs = Dense(output_dim, activation='softmax', name='output')(dense1)
        self.model = Model(inputs=inputs, outputs=outputs, name='lemma_model')
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', \
            metrics=['accuracy'])

    # Train the net.
    # xdata and ydata is the input and output data (must be consistant with .build)
    # nepochs is the maximum number of epochs and stop_loss is the early stoping criteria
    def train(self, xdata, ydata, batch_size, nepochs, **kwargs):
        limitTFMem()
        self.model.fit(xdata, ydata, batch_size=batch_size, epochs=nepochs, **kwargs)
