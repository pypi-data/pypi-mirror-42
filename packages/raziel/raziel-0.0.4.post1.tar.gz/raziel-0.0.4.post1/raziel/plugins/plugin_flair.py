from flair.embeddings import FlairEmbeddings # init embedding
from flair.data import Sentence
from flair.embeddings import StackedEmbeddings

import numpy as np
class plugin_flair:
    def __init__(self, level, option,**kwargs):
        assert level=="embedding", "Only level embedding supported"
        self.sentence_length = kwargs["sentence_length"]
        # init standard GloVe embedding
        self.embeddings = []
        if option is not None:
            assert isinstance(option, list), "Flair options must be a list of embeddings"
            for emb in option:
                self.embeddings.append(FlairEmbeddings(emb))


        # init standard character embeddings
        self.stacked_embeddings = StackedEmbeddings(embeddings=self.embeddings)
        print("Flair Plugin Loaded (Contextualised String Embedding)...")

        self.shape= (self.sentence_length, self.stacked_embeddings.embedding_length)

    def load(self,path):
        print("Flair loaded")

    def getEmbedding(self,w):
        embeddedSentence = Sentence(" ".join(w))
        self.stacked_embeddings.embed(embeddedSentence)
        embedArray = np.array([e.embedding.tolist() for e in embeddedSentence])
        if len(embedArray.shape)==1:
            embedArray = embedArray[np.newaxis,:]
        array = np.full((1, )+self.shape, 0., dtype="float32")
        array[0, :min(self.sentence_length, embedArray.shape[0]),:] = embedArray
        return array

    def getDim(self):
        return self.shape
#
#
# p = plugin_flair("embedding",option=["german-forward","german-backward"], sentence_length=140)
# p.getEmbedding(["hello","world"]).shape