import numpy as np
from allennlp.commands.elmo import ElmoEmbedder, \
    DEFAULT_OPTIONS_FILE, DEFAULT_WEIGHT_FILE
import os
class plugin_elmo:

    def concatenate(self, elmo_embeddings):
        """Helper for elmo layer concatenation."""

        return [np.concatenate(elmo_embeddings[:, i, :]) for i in range(elmo_embeddings.shape[1])]

    def __init__(self, level, option, **kwargs):
        self.sentence_length = kwargs["sentence_length"]
        self.level = level
        assert level in ["embedding"], "Index not reasonable for elmo plugin"
        self.shape = (self.sentence_length, 3072)
        # use 5.5B default elmo model
        self.options_file = DEFAULT_OPTIONS_FILE
        self.weight_file = DEFAULT_WEIGHT_FILE

        if option is not None:
            if os.path.isdir(option):
                json = [x for x in os.listdir(option) if x.endswith("json")]
                hdf5 = [x for x in os.listdir(option) if x.endswith("hdf5")]
                if len(json) ==1 and len(hdf5) == 1:
                    self.options_file = option+"/"+json[0]
                    self.weight_file = option+"/"+hdf5[0]
            elif option == 'small':
                self.options_file = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x1024_128_2048cnn_1xhighway/elmo_2x1024_128_2048cnn_1xhighway_options.json'
                self.weight_file = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x1024_128_2048cnn_1xhighway/elmo_2x1024_128_2048cnn_1xhighway_weights.hdf5'
            elif option == 'medium':
                self.options_file = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x2048_256_2048cnn_1xhighway/elmo_2x2048_256_2048cnn_1xhighway_options.json'
                self.weight_file = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x2048_256_2048cnn_1xhighway/elmo_2x2048_256_2048cnn_1xhighway_weights.hdf5'
            elif option == 'pt' or option == 'portuguese':
                self.options_file = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/contributed/pt/elmo_pt_options.json'
                self.weight_file = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/contributed/pt/elmo_pt_weights.hdf5'



        # INITIALIZATIONS ######################################################################

        # intialize elmo embedding
        self.elmo_embedder = ElmoEmbedder(self.options_file, self.weight_file)
        print("ELMo Plugin Loaded")
        _tmp = self.elmo_embedder.embed_sentence(["hallo"]).shape
        self.shape = (self.sentence_length,_tmp[0],_tmp[2])

    def load(self, path):
        print("ELMo loaded")
    def getEmbedding(self,w):
        elmo_emb = self.elmo_embedder.embed_sentence(w if w != [] else ['.'])
        elmo_emb = np.transpose(elmo_emb, [1,0,2])

        sentence_embedding = np.full((1,)+self.shape, 0., dtype="float32")
        sentence_embedding[0,:min(elmo_emb.shape[0], self.sentence_length)] = elmo_emb
        return(sentence_embedding)
    def getDim(self):
        return self.shape

#
# p = plugin_elmo(level="embedding",option = "/disk1/users/jborst/Data/Embeddings/elmo_german_de-ws", sentence_length=140)
# e = p.getEmbedding(["This","is","a","Sentence","."])
# e.shape