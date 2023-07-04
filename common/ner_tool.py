import os
import fool
from stanfordcorenlp import StanfordCoreNLP

stanford_model = StanfordCoreNLP(f'{os.path.dirname(os.path.abspath(__file__))}/stanford-corenlp-4.5.4',
                                 lang='en')


class NerTool:

    def __init__(self):
        pass

    def get_ner_en(self, text):
        '''
        pip install stanfordcorenlp
        '''
        return stanford_model.ner(text)

    def get_ner_zh(self, text):
        '''
        pip install foolnltk
        tensorflow2.0及以上版本一些API发生了变化，卸载安装1.X的版本就可以使用。如果不想卸载tensorflow2.0，可以做以下修改，亲测可用，本人修改后运行fool.cut(text)和fool.analysis(text)都没问题：
        1.安装tensorflow_addons: pip install tensorflow-addons
        2.找到Anaconda3下的Lib/site-packages/fool
        3.修改model.py文件中的代码：
        第8行改为from tensorflow_addons.text import viterbi_decode
        4.修改predictor.py文件中的代码：
        第8行改为from tensorflow_addons.text import viterbi_decode
        第32行改为with tf.io.gfile.GFile(path, "rb") as f:
        第33行改为graph_def = tf.compat.v1.GraphDef()
        第53行改为self.sess = tf.compat.v1.Session(graph=self.graph)
        '''
        return fool.analysis(text)
