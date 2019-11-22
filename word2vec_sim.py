import os
import gensim
import pyltp as ltp
import numpy as np
import pickle


class Word2vecSim:
    def __init__(self):
        #model_file = './data/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
        self.model_file = './data/sgns.baidubaike.bigram-char'
        self.model = gensim.models.KeyedVectors.load_word2vec_format(self.model_file, binary=False)
        #model = gensim.models.Word2Vec.load(model_file)

        self.LTP_DATA_DIR = './data/ltp_data_v3.4.0/'  # ltp模型目录的路径
        self.cws_model_path = os.path.join(self.LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        self.segmentor = ltp.Segmentor()
        self.segmentor.load(self.cws_model_path)
        self.stopwords = [line.strip() for line in open('./data/哈工大停用词表.txt',encoding='UTF-8').readlines()]
        with open('./data/wordlist.pkl', 'rb') as f:
            self.word_list = pickle.load(f)
        self.q_list, self.a_list = self.read_corpus()

        print('sim model init finished ......')
        return

    def sim_main(self, target):
        res = []
        for string in self.q_list:
            res.append([string, self.vector_similarity(string, target)])
            # print(string, Sim.vector_similarity(string, target))
        # print(res)
        # print(sorted(res, key=lambda x: x[1], reverse=True))
        res = sorted(res, key=lambda x: x[1], reverse=True)
        for i in range(5):
            print(i + 1, res[i][0])
        print(6, "以上都不是")
        x = input("请输入你要问的问题序号：")
        if int(x) == 6:
            return "请咨询医生"
        elif 0 < int(x) < 6:
            return self.a_list[self.q_list.index(res[int(x) - 1][0])]
        else:
            return "无效输入，请重新提问"

    def read_corpus(self):
        q_list = []
        a_list = []
        with open('./data/问答对.txt', encoding="utf-8") as f:
            for line in f.readlines():
                # print(line.split('\t'))
                q_list.append(line.split('\t')[0].strip())
                a_list.append(line.split('\t')[1].strip())
        return q_list, a_list

    def sentence_vector(self, s):
        #for punctuation in '？。，（）：?':
            #question = s.replace(punctuation, '')
        question = s.split()
        words_list = list(self.segmentor.segment(question[0]))
        words = [word for word in words_list if word not in self.stopwords]
        # words = segmentor.segment(s)
        # print(list(words))
        v = np.zeros(300)
        for word in words:
            if word not in self.word_list:
                v += np.random.uniform(-0.25, 0.25, 300)
                # print(word)
            else:
                v += self.model[word]
            #print(v)
        v /= len(words)
        return v

    def vector_similarity(self, s1, s2):
        v1, v2 = self.sentence_vector(s1), self.sentence_vector(s2)
        #print(v1, v2)
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        return np.dot(v1, v2) / denom

    def sim_eval(self, target):
        res = []
        candidate = ''
        for string in self.q_list:
            res.append([string, self.vector_similarity(string, target)])
        res = sorted(res, key=lambda x: x[1], reverse=True)
        for i in range(5):
            #print(i + 1, res[i][0])
            candidate = candidate + str(i+1) + res[i][0] + '\n'
        return candidate


if __name__ == "__main__":
    Sim = Word2vecSim()
    while True:
        target = input("输入问题：")
        res = []
        for string in Sim.q_list:
            res.append([string, Sim.vector_similarity(string, target)])
            #print(string, Sim.vector_similarity(string, target))
        #print(res)
        #print(sorted(res, key=lambda x: x[1], reverse=True))
        res = sorted(res, key=lambda x: x[1], reverse=True)
        for i in range(5):
            print(i+1, res[i][0])
        print(6, "以上都不是")
        x = input("请输入你要问的问题序号：")
        if int(x) == 6:
            print("请咨询医生")
        elif 0 < int(x) < 6:
            print(Sim.a_list[Sim.q_list.index(res[int(x)-1][0])])
        else:
            print("无效输入，请重新提问")



'''
while True:
    target = input("问题：")
    for string in strings:
        print(string, vector_similarity(string, target))
'''

