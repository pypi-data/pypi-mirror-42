import numpy as np
from raziel.vocab import Vocabulary
import keras

class plugin_chars:

    def __init__(self, level, option, **kwargs):
        self.vocab = Vocabulary()
        self.name = "characters"
        self.word_length = kwargs["word_length"]
        self.sentence_length = kwargs["sentence_length"]
        self.level= level
        assert level in ["index"], "%s needs 'index' as output. Embedding will be coming soon"
        if option is None:
            self.vocab.setCharacterset()
        else:
            assert isinstance(option, str), "Option for Characters must " \
                                            "be a string with all the characters"
            self.vocab.setCharacterset(option)

        if level == "index":
            self.shape = (self.sentence_length, self.word_length)

        print("Char Dict loaded")

    def getEmbedding(self, w):

        characters = np.full((1, self.sentence_length ,self.word_length), 0., dtype="float32")
        indices = keras.preprocessing.sequence.pad_sequences(
            [self.vocab.getAlphabetIndex(list(word)) for word in w], maxlen=self.word_length, padding="post", value=0.)

        characters[0,:min(self.sentence_length,indices.shape[0]),:] = indices
        return(characters)

    def getDim(self):
        return None
