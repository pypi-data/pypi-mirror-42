import numpy as np
import os
import pathlib
import logging
from raziel.plugins import plugins_dict
from raziel.vocab import Vocabulary
from tqdm import tqdm





class Raziel:
    def __init__(self, dm = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        self.vocab = Vocabulary()
        self.externalPlugins = {}

        self.charVocabularysize = None
        self.max_word_length = 60
        self.max_sequence_length = 140

        self.pluginDimension = {}
        self.numOfTags = None


        self.scheme = ""
        self.defaultDirectory = os.path.join(pathlib.Path.home().as_posix(), ".raziel")

        self.data_manager = dm
        self.transform_chain= None


    def setLogging(self,level):
        if level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        if level.lower() == "error":
            self.logger.setLevel(logging.ERROR)
        if level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)

    def load_plugins(self, params):
        assert isinstance(params, dict)
        self.pluginDimension={}
        self.externalPlugins={}
        for key, val in params.items():
            self.externalPlugins[key] = plugins_dict[key]()
            self.externalPlugins[key].load(val)
            self.pluginDimension[key] = self.externalPlugins[key].getDim()
            if self.wordEmbeddingDimension is None:
                Warning("Word embedding dimension not set.")


    def toScheme (self, tagset, scheme="iobes", outside="O"):
        scheme = scheme.lower()
        if scheme == "iobes" or scheme == "bioes":
            return ([outside]+["I-"+x for x in tagset]+["B-"+x for x in tagset]+["E-"+x for x in tagset]+["S-"+x for x in tagset])
        elif (scheme == "bilou"):
            return (
            [outside] + ["B-" + x for x in tagset] + ["I-" + x for x in tagset] + ["L-" + x for x in tagset] + ["U-" + x for x in tagset])
        elif (scheme == "bio" or scheme == "iob"):
            return ([outside] + ["B-" + x for x in tagset] + ["I-" + x for x in tagset])
        elif(scheme == "noprefix"):
            return [outside] + tagset

        return(tagset)

    def setTagset(self, tagset, scheme="iobes", outside="O"):
        self.scheme = scheme
        self.vocab.setTagset(self.toScheme(tagset, scheme=scheme, outside=outside))


    def chain(self, get):
        #print (get)
        self.transform_chain = {}
        kwargs = {
            "sentence_length": self.max_sequence_length,
            "word_length": self.max_word_length,
            "tagset": self.vocab.tagset
        }
        for name, description in get.items():
            self.transform_chain[name] = (description[0], plugins_dict[description[1]](level=description[2], option=description[3], **kwargs))

    def transform(self, purpose = "general"):
        data = self.data_manager[purpose]
        traindata = {}
        traindata["lengths"] = data.groupby("sentence_id").count()["token"].tolist()
        traindata["raw"] = []
        dataset_size = len(set(data["sentence_id"].tolist()))
        for name, (column, plugin) in self.transform_chain.items():
            array = np.full((dataset_size,) + plugin.shape, 0.)
            print(name)
            for i, sentence in tqdm(enumerate(data.groupby("sentence_id"))):
                traindata["raw"].append(sentence[1]["token"].tolist())
                array[i] = plugin.getEmbedding(sentence[1][column].tolist())
            traindata[name]=array
        return traindata

    def transform_iter(self, batch_size=100,purpose = "general"):
        for data in self.data_manager.iter(batch_size=batch_size, purpose=purpose):
            traindata = {}
            traindata["lengths"] = np.array(data.groupby("sentence_id").count()["token"].tolist(),dtype=np.int32)
            traindata["sentence_ids"] = list(set(data["sentence_id"].tolist()))
            for name, (column, plugin) in self.transform_chain.items():
                array = np.full((batch_size,) + plugin.shape, 0.)
                print(name)
                for i, sentence in tqdm(enumerate(data.groupby("sentence_id"))):
                    array[i] = plugin.getEmbedding(sentence[1][column].tolist())
                traindata[name]=array
            yield traindata

    def getEmbeddingLayer(self):
        layers = {}
        for name, (column, plugin) in self.transform_chain.items():
            if hasattr(plugin, "vocab"):
                if hasattr(plugin.vocab, "wordEmbedding") and plugin.vocab.wordEmbedding is not None:
                    layers[name] = plugin.vocab.getEmbeddingLayer()
        return layers

    def schemetransformer(self, column, scheme="BIOES", multilabel=False, purpose="general"):
        scheme = scheme.upper()
        scheme= "BIOES" if scheme =="IOBES" else scheme
        data = self.data_manager.get_data(purpose=purpose)
        transforming_column = [tagset if isinstance(tagset,list) else [tagset] for tagset in data[column].tolist()]

        newtags_column = []
        for i, tagset in enumerate(transforming_column):
            if "O" in tagset or "O" == tagset:
                newtags_column.append(tagset)
            elif scheme == "NOPREFIX":
                newtags_column.append([t.split("-")[-1] for t in tagset])
            else:
                currentTagset = [t.split("-")[-1] for t in tagset]
                newtags = []
                if i == 0:
                    nextTagset = [t.split("-")[-1] for t in transforming_column[i + 1]]
                    for t in currentTagset:
                        if t in nextTagset:
                            newtags_column.append("B-" + t)
                        else:
                            if scheme == "BIOES": newtags.append("S-" + t)
                            if scheme == "BIO1": newtags.append("I-" + t)
                            if scheme == "BIO2": newtags.append("B-" + t)
                            newtags_column.append(newtags)
                elif i == len(transforming_column) - 1:
                    previousTagset = [t.split("-")[-1] for t in
                                  transforming_column[i - 1]]
                    for t in currentTagset:
                        if t in previousTagset:
                            if scheme == "BIOES": newtags.append("E-" + t)
                            if scheme == "BIO1": newtags.append("I-" + t)
                            if scheme == "BIO2": newtags.append("I-" + t)
                        else:
                            if scheme == "BIOES": newtags.append("S-" + t)
                            if scheme == "BIO1": newtags.append("I-" + t)
                            if scheme == "BIO2": newtags.append("B-" + t)
                    newtags_column.append(newtags)
                else:

                    nextTagset = [t.split("-")[-1] for t in
                                  transforming_column[i + 1]]
                    previousTagset = [t.split("-")[-1] for t in
                                  transforming_column[i - 1]]
                    newtags = []
                    for t in currentTagset:
                        if t in previousTagset and t in nextTagset:
                            newtags.append("I-" + t)
                        elif t in previousTagset and t not in nextTagset:
                            if scheme == "BIOES": newtags.append("E-" + t)
                            if scheme == "BIO1": newtags.append("I-" + t)
                            if scheme == "BIO2": newtags.append("I-" + t)
                        elif t not in previousTagset and t in nextTagset:
                            newtags.append("B-" + t)
                        else:
                            if scheme == "BIOES": newtags.append("S-" + t)
                            if scheme == "BIO1": newtags.append("I-" + t)
                            if scheme == "BIO2": newtags.append("B-" + t)
                    newtags_column.append(newtags)

        if not multilabel:
            newtags_column = [x[0] for x in newtags_column]
        self.data_manager.update({column: newtags_column}, level="token",purpose=purpose)

def main():
    m = "cnn_features"



if __name__ == "__main__":
    main()