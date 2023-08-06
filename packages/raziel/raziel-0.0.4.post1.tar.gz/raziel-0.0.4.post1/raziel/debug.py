# import sys; sys.path.insert(0, "/home/jborst/tmp/utsi")
#
#
# from utsi import DataManager
# dm = DataManager()
#
# dm.read_conll("/disk1/users/jborst/Data/Test/NER/CoNLL-2003/de/BIOES/test_2c_small.txt", purpose="test",columns=["token","ner"])
# # dm.read_json("/disk1/users/jborst/Data/Test/NER/Wiki/test_comma.json", purpose="test")
#

# from raziel.Raziel import Raziel
# bb = Raziel(dm)
# bb.schemetransformer("ner","noprefix")
# #
# # with open("/disk1/users/jborst/Data/Test/NER/Wiki/tagset", "r") as tagsetInput:
# #     tagset = tagsetInput.read().split("\n")[:-1] + ["/education"]
# # bb.setTagset(tagset, scheme="noprefix")
# # bb.language = "de"
# # bb.sequence_length = 140
# # bb.character_length = 60
# # # bb.setTagset(tagset=["LOC", "PER", "ORG", "MISC"], scheme="iobes")
# #
# # traindata = bb.chain({
# #     # "chars": ("token", "character", "index", None),
# #     # "w2v":          ("token", "custom", "embedding", "/disk1/users/jborst/Data/Pretrained Word Embeddings/german/cc.de.300.10K.vec"), # only act on something as file
# #     #"elmo":         ("token", "elmo", "embedding", None),
# #     "mentions":    ("mentions",   "multilabel", "index", "sparse" ),
# #     # "fasttext":     ("token", "fasttext", "embedding", "/disk1/users/jborst/Data/Pretrained Word Embeddings/german/cc.de.300.bin")
# #     # "ner_embedding": ("ner", "custom", "embedding", "/disk1/users/jborst/Data/Pretrained Word Embeddings/test.txt")
# # })
# # for data in bb.transform_iter(10,"test"):
# #     print(data)
# #     break
# #
# #
# import sys;
# sys.path.insert(0,"/home/jborst/tmp/utsi")
# sys.path.insert(0,"/home/jborst/tmp/raziel")
# sys.path.insert(0,"/home/jborst/tmp/ptagger")
# from tqdm import tqdm
# import numpy as np
# import itertools
# from utsi import DataManager
# from raziel.Raziel import Raziel
# dm = DataManager()
# bb = Raziel(dm)
# #
# # scheme = "iobes"
# #
# # bb.data_manager.read_conll("/disk1/users/jborst/Data/Test/NER/CoNLL-2003/de/BIOES/train.txt", purpose="embed")
# # bb.data_manager.read_conll("/disk1/users/jborst/Data/Test/NER/CoNLL-2003/de/BIOES/valid.txt", purpose="embed")
# # bb.data_manager.read_conll("/disk1/users/jborst/Data/Test/NER/CoNLL-2003/de/BIOES/test.txt", purpose="test")
# # tagset = ["PER", "ORG", "LOC", "MISC"]
# # bb.setTagset(tagset, scheme=scheme)
# # # bb.schemetransformer("ner", scheme)
# # bb.max_sequence_length = 10
# #
# # bb.chain({
# #    "embeddings": ("token", "custom", "embedding","/disk1/users/jborst/Data/Pretrained Word Embeddings/german/cc.de.300.10K.vec"),
# #     "tags": ("ner", "label", "index", "sparse")
# # })
# #
# # data = bb.transform("test")
#
# dm = DataManager()
# dm.read_conll("/home/jborst/semEval_task1.conll",columns=["token", "pos", "lposition","rposition", "relation"])
# sample = dm.random(100)
# from utsi.tasks.implementations_ethds3 import ETH3DS
# p=ETH3DS()
# p.initialize()
# p.train(dm.get_data(sample))
# p.run(data=dm.get_data())

import tensorflow as tf
import sys;
sys.path.insert(0,"/home/jborst/tmp/utsi")
sys.path.insert(0,"/home/jborst/tmp/raziel")
sys.path.insert(0,"/home/jborst/tmp/ptagger")
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

from tqdm import tqdm
import numpy as np
import itertools
from utsi import DataManager
from raziel import Raziel
dm = DataManager()
bb = Raziel(dm)
bb.data_manager.read_conll("/disk1/users/jborst/Data/Test/NER/GermEval2014/iobes/train/train_outer.conll", purpose="train", columns=["token","ner"])
# bb.data_manager.read_conll("/disk1/users/jborst/Data/Test/NER/GermEval2014/iobes/devel/devel_outer.conll", purpose="valid",columns=["token","ner"])
# bb.data_manager.read_conll("/disk1/users/jborst/Data/Test/NER/GermEval2014/iobes/test/test_outer.conll", purpose="test",columns=["token","ner"])
tagset = ["PER", "ORG", "LOC", "OTH", "PERpart", "ORGpart","LOCpart","OTHpart","PERderiv","ORGderiv","LOCderiv","OTHderiv"]
bb.setTagset(tagset, scheme="BIOES")
bb.schemetransformer("ner", "BIOES", multilabel=False)
bb.language = "de"
bb.sequence_length = 140
bb.character_length = 60