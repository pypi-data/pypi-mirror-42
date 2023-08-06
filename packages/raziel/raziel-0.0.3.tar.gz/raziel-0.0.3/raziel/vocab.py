import string
import numpy as np
import logging
# from . import helpers



class Vocabulary:
	def __init__(self):
		self.data = None
		self.specialToken = "UNK"
		self.lowercase=False

		self.alphabet = list(string.ascii_letters+"0123456789"+string.punctuation+"äöüÄÖÜ \n")
		self.wordList = None
		self.tagset = None

		self.lookupAlphabet = None
		self.lookupWords = None
		self.lookupWordsReverse = None
		self.lookupTagset = None
		self.lookupTagsetReverse = None

		self.wordEmbedding=None
		self.wordEmbeddingSize = None
		self.vocabularySize = 0
		self.alphabetSize = None
		self.numOfTags = None


		self.conllData = None

		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.setLevel(logging.WARNING)

	###################################################
	# Setter

	def setCharacterset(self, alphabet = None):
		self.logger.debug("Setting alphabet...")
		if alphabet:
			self.alphabet = list(alphabet)
		self.alphabetSize = len(self.alphabet) + 1
		self.logger.debug("Setting alphabetsize to %i" % (self.alphabetSize,))
		self.lookupAlphabet = dict(zip(self.alphabet,list(range(1,self.alphabetSize))))
		self.lookupAlphabetReverse = dict(zip(list(range(1, self.alphabetSize)),self.alphabet))

	def setTagset(self, tagset = None):
		if not tagset:
			self.logging.error("Tagset empty in self.setTagset()...")
			exit()
		self.tagset=tagset
		self.numOfTags = len(tagset)
		self.logger.debug("Setting tagsetsize to %i" % (self.numOfTags,))
		self.lookupTagset =dict(zip(self.tagset,list(range(0,self.numOfTags))))
		self.logger.debug("Creating reverse lookups for tags...")
		self.lookupTagsetReverse =dict(zip(list(range(0,self.numOfTags)) ,self.tagset))

	def setWordEmbedding(self, path=None):
		self.logger.debug("Loading static word embedding")
		from gensim.models import KeyedVectors as kv
		self.logger.debug("Trying " + path)
		self.wordEmbedding = kv.load_word2vec_format(path)

		self.logger.debug("Loaded %i vectors " % (len(self.wordEmbedding.index2word),) )
		self.logger.debug("Stacking 0 and special token ")
		self.wordEmbedding.vectors = np.vstack((
			np.array([0]* self.wordEmbedding.vector_size), # the vector for the masking
			self.wordEmbedding.vectors,
			np.array([0] * self.wordEmbedding.vector_size),  # the vector for the special token
		))

		self.wordEmbedding.index2word.insert(0,"")
		self.wordEmbedding.index2word.append(self.specialToken)


		self.vocabularySize = len(self.wordEmbedding.index2word)-1
		self.logger.debug("Setting vocabularysize to %i . (Loaded vectors + special token)" % (self.vocabularySize,))
		self.wordEmbeddingSize = self.wordEmbedding.vector_size

		self.wordList = self.wordEmbedding.index2word[1:  len(self.wordEmbedding.index2word)+1]
		self.logger.debug("Creating lookup..")
		self.lookupWords = dict(zip(self.wordList,list(range(1,self.vocabularySize +1))))

	################################################################
	# Getters
	def  getEmbeddingLayer(self,trainable = False):
		"Get the loaded pretrained embedding as a keras layer, ready to be imported to the neural network"
		if self.wordEmbedding:
			return (self.wordEmbedding.get_keras_embedding(train_embeddings=trainable))
		else:
			self.logger.warning("Trying to get a word embedding layer with no static embedding loaded.")
			return(None)

	def getWordIndex(self, tokens = None):
		if type(tokens) == list :
			if self.lowercase:
				return([self.lookupWords.get(item.lower(),self.vocabularySize) for item in tokens])
			else:
				return([self.lookupWords.get(item,self.vocabularySize) for item in tokens])

		elif type(tokens) == str:
			if self.lowercase:
				return(self.lookupWords.get(tokens.lower(),self.vocabularySize))
			else:
				return(self.lookupWords.get(tokens,self.vocabularySize))
	def getWordIndexReverse(self, tokens=None):
		if self.lookupWordsReverse is None:
			self.lookupWordsReverse = dict(zip( list(self.lookupWords.values()),list(self.lookupWords.keys()) ))
		if type(tokens) == list:
			return ([self.lookupWordsReverse.get(item, 'unk') for item in tokens])
		else:
			return (self.lookupWordsReverse.get(tokens, 'unk'))



	def getAlphabetIndex(self, tokens=None):
		if type(tokens) == list:
			return ([self.lookupAlphabet.get(item, self.alphabetSize) for item in tokens])
		elif type(tokens) == str:
			return (self.lookupAlphabet.get(tokens, self.alphabetSize))

	def getAlphabetIndexReverse(self, tag=None):
		if type(tag) == list:
			return ([self.lookupAlphabetReverse.get(item, 'unk') for item in tag])
		else:
			return (self.lookupAlphabetReverse.get(tag, 'unk'))

	def getTagsetIndex(self, tag=None):
		if type(tag) == list:
			return ([self.lookupTagset[item] for item in tag])
		elif type(tag) == str:
			return (self.lookupTagset[tag])

	def getTagsetIndexReverse(self, tag=None):
		if type(tag) == list:
			return ([self.lookupTagsetReverse.get(item, None) for item in tag])
		else:
			return (self.lookupTagsetReverse.get(tag, None))


	def __getstate__(self):
		blacklist = ["logger", "wordEmbedding"]
		print("Static loaded word Embeddings won't be saved outside the model!")
		return {key: self.__dict__[key] for key in self.__dict__.keys() if key not in blacklist}
	def __setstate__(self, state):
		for key in state.keys():
			self.__dict__[key] = state[key]
			self.logger = logging.getLogger(self.__class__.__name__)
			self.logger.setLevel(logging.WARNING)




def main():
	vocab = Vocabulary()
	vocab.readConll("/home/jb/git/ptagger/resources/BIOES/test_small2.txt")
	vocab.setWordEmbedding("/home/jb/git/ptagger/resources/cc.de.300.10K.vec")
	# vocab.getWordIndex("Parlament")
	vocab.setCharacterset()
	vocab.setTagset(["O","S-PER","S-LOC","S-ORG","S-MISC","B-PER","B-LOC","B-ORG","B-MISC","I-PER","I-LOC","I-ORG","I-MISC","E-PER","E-LOC","E-ORG","E-MISC"])
	#
	#
	trainingsdata = vocab.getTraindata(get = ["words","chars","tags"])

if __name__ == "__main__":
	main()