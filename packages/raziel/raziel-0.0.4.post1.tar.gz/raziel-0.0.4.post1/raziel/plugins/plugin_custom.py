import numpy as np
from raziel.vocab import Vocabulary
class plugin_custom:
    def __init__(self, level, option, **kwargs):
        self.vocab= Vocabulary()
        self.name = "custom"
        self.level = level
        self.word_length = kwargs["word_length"]
        self.sentence_length = kwargs["sentence_length"]
        assert level in ["index", "embedding"], "only 'index' and 'embedding' supported"
        self.option=option
        assert option is not None, "Custom needs a path to a vector file"
        self.vocab.setWordEmbedding(option)

        if level == "index":
            self.shape = (self.sentence_length, )
        elif level == "embedding":
            self.shape = (self.sentence_length, self.vocab.wordEmbeddingSize)

        print("custom embedding loaded")


    def getEmbedding(self, w, level="embedding"):
        index = self.vocab.getWordIndex(w)

        if self.level == "index":
            index_array=np.full((1,self.sentence_length), 0., dtype="int32")
            index_array[0,:min(self.sentence_length,len(index))] = index
            return index_array
        else:
            embedded = [self.vocab.wordEmbedding.vectors[i] for i in index]
            sentence_embedding = np.full((1, self.sentence_length, self.vocab.wordEmbeddingSize), 0., dtype="float32")
            sentence_embedding[0, :min(len(embedded), self.sentence_length),:] = np.array(embedded[:min(len(embedded), self.sentence_length)])
            return (sentence_embedding)

    def getDim(self):
        return (self.vocab.wordEmbeddingSize,)

# kwargs = {
#             "sentence_length": 100,
#             "word_length": 60
#         }
# p = plugin_custom(level="embedding",option = "/disk1/users/jborst/Data/Pretrained Word Embeddings/glove.840B.300d_10k.w2vformat.txt", **kwargs)
# e = p.getEmbedding(["This","is","a","Sentence","."])
# e.shape