import numpy as np
from raziel.vocab import Vocabulary


class plugin_multilabel:
    def __init__(self, level, option, **kwargs):
        self.vocab= Vocabulary()
        self.vocab.setTagset(kwargs["tagset"])
        self.name = "multilabel"
        self.level = level
        self.word_length = kwargs["word_length"]
        self.sentence_length = kwargs["sentence_length"]
        self.maximum_tagsetsize=self.vocab.numOfTags
        if kwargs.get("maximum_tagsetsize", None) is not None:
            self.maximum_tagsetsize = kwargs.get["maximum_tagsetsize"]

        assert level in ["index"], "only 'index' supported"

        self.option = "categorical"
        if option is not None:
            self.option = option
        assert option in ["sparse","categorical"] or None, \
            "Multilabel option not in sparse or categrorical"

        if option == "sparse":
            self.shape = (self.sentence_length, self.maximum_tagsetsize)
        elif option == "categorical":
            self.shape = (self.sentence_length, self.vocab.numOfTags)

        print("Multilabel plugin loaded")


    def getEmbedding(self, w ):
        index = [self.vocab.getTagsetIndex(x) for x in w]
        if self.option=="sparse":
            array = np.full((1,) + self.shape, 0., dtype="int32")
            for i, row in enumerate(index):
                array[0, i,:min(len(row),self.shape[1])] = row
            return array

        if self.option == "categorical":
            array = np.full((1,) + self.shape, 0., dtype="int32")
            for i, tags in enumerate(index):
                for tag in tags:
                    array[0, i, tag]=1
            return array


    def getDim(self):
        return self.shape
