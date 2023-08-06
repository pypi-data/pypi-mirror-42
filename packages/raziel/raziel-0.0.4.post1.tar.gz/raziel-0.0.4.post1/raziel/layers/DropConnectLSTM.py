from keras.layers import LSTM
import keras.backend as K


class DropConnectLSTM(LSTM):
    def __init__(self, recurrent_dropconnect=0., dropconnect = 0., **kwargs):
        self.dropconnect = 1. - dropconnect
        self.recurrent_dropconnect = 1. - recurrent_dropconnect
        super(DropConnectLSTM, self).__init__(**kwargs)
        if 0. < self.dropconnect < 1. or 0. < self.recurrent_dropconnect < 1.:
            self.uses_learning_phase = True
        self.supports_masking = True

    def call(self, x, mask = None, **kwargs):
        if 0. < self.dropconnect < 1.:
            self.cell.kernel = K.in_train_phase(K.dropout(self.cell.kernel, self.dropconnect), self.cell.kernel)
            self.cell.bias = K.in_train_phase(K.dropout(self.cell.bias, self.dropconnect), self.cell.bias)
        if 0. < self.recurrent_dropconnect < 1.:
            self.cell.kernel = K.in_train_phase(K.dropout(self.cell.recurrent_kernel, self.recurrent_dropconnect), self.cell.kernel)
        return super(LSTM, self).call(x,mask,**kwargs)

