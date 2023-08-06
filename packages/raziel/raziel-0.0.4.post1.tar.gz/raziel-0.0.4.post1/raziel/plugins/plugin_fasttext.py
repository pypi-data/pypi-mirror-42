import numpy as np
from gensim.models.fasttext import FastText as ft
class plugin_fasttext:
    def __init__(self, level, option, **kwargs):
        self.name = "custom"
        self.level = level
        self.sentence_length = kwargs["sentence_length"]
        assert level in ["embedding"], "only 'embedding' supported"
        self.option = option
        assert option is not None, "Custom needs a path to a vector file"

        self.embedding = ft.load_fasttext_format(option)

        self.shape = (self.sentence_length, self.embedding.vector_size)
        print("Fasttext Plugin Loaded")

    def getEmbedding(self,w):
        e = np.full((len(w), self.embedding.vector_size),0)
        try:
            e = np.array([self.embedding.wv[x] for x in w])
        except:
            Warning("Fasttext could not convert: " + " ".join(w))
        for i in np.where(~e.any(axis=1))[0]:
            e[i] = e[i] + 1e-30

        array = np.full((1, self.sentence_length, self.embedding.vector_size), 0.,dtype="float32")
        array[0,:min(self.sentence_length, e.shape[0]),:] = e[:min(self.sentence_length, e.shape[0]),:]
        return array
    def getDim(self):
        return (self.embedding.get_dimension(),)
