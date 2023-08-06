from elmoformanylangs import Embedder
import numpy as np

class plugin_elmo_many:

    def __init__(self):
        self.e = None
        self.dim = 0
        print("ELMo Plugin Loaded")

    def load(self, path):
        self.e = Embedder(path,batch_size=140)
        self.dim = (3,self.e.sents2elmo(["hello"],output_layer=3)[0].shape[-1])
        print("ELMo loaded")

    def getEmbedding(self,w):
        # elmo_emb = self.e.sents2elmo(w)
        # elmo_emb = np.concatenate([x for x in  self.e.sents2elmo([w],output_layer=3)[0]], axis=- 1)
        elmo_emb = np.swapaxes(self.e.sents2elmo([w], output_layer=3)[0],0,1)
        return(elmo_emb)
    def getDim(self):
        return self.dim
#
# p = plugin_elmo_many()
# p.load("/home/jborst/elmo/")
# e = p.getEmbedding(["hello", "world","german","embeddings"])
#
# e.shape