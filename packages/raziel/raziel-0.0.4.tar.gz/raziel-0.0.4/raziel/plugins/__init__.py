from raziel.plugins.plugin_fasttext import *
from raziel.plugins.plugin_elmo import *
from raziel.plugins.plugin_flair import *
from raziel.plugins.plugin_chars import plugin_chars
from raziel.plugins.plugin_custom import plugin_custom
from raziel.plugins.plugin_label import plugin_label
from raziel.plugins.plugin_multilabel import plugin_multilabel
from raziel.plugins.plugin_list import plugin_list
from raziel.plugins.plugin_bert import plugin_bert
plugins_dict = { "fasttext": plugin_fasttext,
                 "flair":plugin_flair,
                 "elmo": plugin_elmo,
                 "character": plugin_chars,
                 "custom": plugin_custom,
                 "label":plugin_label,
                 "multilabel":plugin_multilabel,
                 "list": plugin_list,
                 "bert": plugin_bert}