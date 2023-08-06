from keras.layers import Layer
import keras.backend as K


class WeightedMean(Layer):
    def __init__(self, **kwargs):
        self.output_dim = 3
        super(WeightedMean, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        print(input_shape)
        self.kernel = self.add_weight(name='kernel',
                                      shape=(input_shape[-2],),
                                      initializer='uniform',
                                      trainable=True)
        super(WeightedMean, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        # return K.concatenate([K.repeat_elements(K.expand_dims(K.sum(x*K.expand_dims(self.kernel,axis = 1),axis =-2),1),3,-2),x*K.expand_dims(self.kernel,axis = -1)],-2)
        # return x*K.expand_dims(self.kernel,axis = -1)
        return K.sum(x*K.expand_dims(self.kernel,axis = 1),axis =-2)
    def compute_output_shape(self, input_shape):
        return input_shape[:-2] + (input_shape[-1],)


