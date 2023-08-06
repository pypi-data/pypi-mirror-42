from flair.embeddings import BertEmbeddings # init embedding
from flair.data import Sentence
from flair.embeddings import StackedEmbeddings
from flair.embeddings import WordEmbeddings, CharacterEmbeddings

import numpy as np
class plugin_bert:
    def __init__(self, level, option,**kwargs):
        assert level=="embedding", "Only level embedding supported"
        self.sentence_length = kwargs["sentence_length"]
        # init standard GloVe embedding
        if option is None:
            self.embedding = BertEmbeddings()
        else:
            self.embedding = BertEmbeddings(option)

        # init standard character embeddings
        print("Bert Plugin Loaded (Contextualised String Embedding)...")

        self.shape= (self.sentence_length, self.embedding.embedding_length)

    def load(self,path):
        print("Flair loaded")

    def getEmbedding(self,w):
        embeddedSentence = Sentence(" ".join(w))
        self.embedding.embed(embeddedSentence)
        embedArray = np.array([e.embedding.tolist() for e in embeddedSentence])
        if len(embedArray.shape)==1:
            embedArray = embedArray[np.newaxis,:]
        array = np.full((1,) + self.shape, 0., dtype="float32")
        array[0, :min(self.sentence_length, embedArray.shape[0]),
        :] = embedArray
        return array

    def getDim(self):
        return self.shape


# p = plugin_bert("embedding", option="bert-base-cased", sentence_length=140)
# p.getEmbedding(["hallo","welt"])