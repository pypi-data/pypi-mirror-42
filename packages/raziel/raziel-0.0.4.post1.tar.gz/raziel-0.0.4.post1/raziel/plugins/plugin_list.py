import numpy as np
from raziel.vocab import Vocabulary

class plugin_list:
    def __init__(self, level, option, **kwargs):
        self.vocab= Vocabulary()
        self.vocab.setTagset(option)
        self.name = "list"
        self.level = level
        self.word_length = kwargs["word_length"]
        self.sentence_length = kwargs["sentence_length"]
        assert level in ["index"], "only 'index' supported"

        self.option = "sparse"
        if option is not None:
            self.option = option
        self.shape = (self.sentence_length, )
        print("List plugin loaded")


    def getEmbedding(self, w ):
        index = self.vocab.getTagsetIndex(w)
        index_array = np.full((1, self.sentence_length), 0., dtype="int32")
        index_array[0, :min(self.sentence_length, len(index))] = index[:min(self.sentence_length, len(index))]
        return index_array


    def getDim(self):
        return (self.vocab.wordEmbeddingSize,)

