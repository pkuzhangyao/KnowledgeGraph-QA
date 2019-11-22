#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: zhangyao
# Date: 19-11-1

from question_classifier import *
from question_parser import *
from answer_search import *
from word2vec_sim import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        #self.sim = Word2vecSim()

    def chat_main(self, sent):
        answer = '您好，我是爱医生智能助理，希望可以帮到您。如果没答上来，可联系我们xxxx@aidoctor.com。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        print("res_classifer:", res_classify)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        print("res_sql:", res_sql)
        final_answers = self.searcher.search_main(res_sql)

        #print("final_answers:", final_answers)
        if not final_answers:
            return "这个问题知识库中暂时没有，请查看用户问答库中有没有您要问的问题。", 0
        else:
            return '\n'.join(final_answers), 1

if __name__ == '__main__':
    handler = ChatBotGraph()
    sim = Word2vecSim()
    while 1:
        question = input('用户:')
        answer, flag = handler.chat_main(question)
        print(answer, flag)
        if flag == 0:
            final_answer = sim.sim_main(question)
            print('爱医生智能助理:', final_answer)
        elif flag == 1:
            print('爱医生智能助理:', answer)
            print("可以解决你的问题吗？")
            x = input("请输入1表示可以，2表示不可以：")
            if x == '1':
                print("感谢您的提问。")
            elif x == '2':
                print("很抱歉知识库中的知识不能回答您的问题，请查看用户问答库中有没有您要问的问题。")
                final_answer = sim.sim_main(question)
                print(final_answer)
            else:
                print("输入出错请重新提问。")


