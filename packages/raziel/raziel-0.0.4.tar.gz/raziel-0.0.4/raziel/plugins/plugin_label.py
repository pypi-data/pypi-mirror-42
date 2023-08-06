import numpy as np
from raziel.vocab import Vocabulary
import keras

class plugin_label:
    def __init__(self, level, option, **kwargs):
        self.vocab= Vocabulary()
        self.vocab.setTagset(kwargs["tagset"])
        self.name = "custom"
        self.level = level
        self.word_length = kwargs["word_length"]
        self.sentence_length = kwargs["sentence_length"]
        assert level in ["index"], "only 'index' supported"

        self.option = "sparse"
        if option is not None:
            self.option = option
        assert option in ["sparse","categorical"] or None, "Label option can only be sparse or categroical"

        if option == "sparse":
            self.shape = (self.sentence_length, )
        elif option == "categorical":
            self.shape = (self.sentence_length, self.vocab.numOfTags)

        print("Label plugin loaded")


    def getEmbedding(self, w ):
        index = self.vocab.getTagsetIndex(w)
        index_array = np.full((1, self.sentence_length), 0., dtype="int32")
        index_array[0, :min(self.sentence_length, len(index))] = index[:min(self.sentence_length, len(index))]
        if self.option=="sparse":
            return index_array
        if self.option == "categorical":
            return keras.utils.to_categorical(index_array, self.vocab.numOfTags)


    def getDim(self):
        return (self.vocab.wordEmbeddingSize,)

