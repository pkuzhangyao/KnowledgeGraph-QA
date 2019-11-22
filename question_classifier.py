#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: zhangyao
# Date: 19-11-1

import os
import ahocorasick
diseases_dict = ''


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.check_path = os.path.join(cur_dir, 'dict/check.txt')
        self.check_item_path = os.path.join(cur_dir, 'dict/check_item.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptoms.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        self.behavior_path = os.path.join(cur_dir, 'dict/behaviors.txt')
        self.organ_path = os.path.join(cur_dir, 'dict/organ.txt')
        # 加载特征词，把txt文件加载成一个大list
        self.disease_wds = [i.strip() for i in open(self.disease_path, encoding="utf-8") if i.strip()]
        self.check_wds = [i.strip() for i in open(self.check_path, encoding="utf-8") if i.strip()]
        self.drug_wds = [i.strip() for i in open(self.drug_path, encoding="utf-8") if i.strip()]
        self.food_wds = [i.strip() for i in open(self.food_path, encoding="utf-8") if i.strip()]
        self.check_item_wds = [i.strip() for i in open(self.check_item_path, encoding="utf-8") if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path, encoding="utf-8") if i.strip()]
        self.behavior_wds = [i.strip() for i in open(self.behavior_path, encoding="utf-8") if i.strip()]
        self.organ_wds = [i.strip() for i in open(self.organ_path, encoding="utf-8") if i.strip()]
        # 把上面所有的放在一起构造一个领域字典
        self.region_words = set(self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.check_item_wds + self.symptom_wds+self.behavior_wds+self.organ_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path, encoding="utf-8") if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典 类似   {'骶骨裂': ['symptom'], '豆腐烧胡萝卜': ['food'], '喉角化症': ['disease']}
        self.wdtype_dict = self.build_wdtype_dict()
        # print("wdtype_dict", self.wdtype_dict)
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现', '会引起']
        self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成', '病因']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现', '引起', '引起']
        self.food_qwds = ['饮食', '饮用', '可以吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医', '治愈', '逆转']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室', '去哪看']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚'] # '需要', '要'
        self.check_item_high_qwds = ['阳性', '高怎么回事', '偏高', '高是怎么回事', '阳', '高']
        self.check_item_low_qwds = ['阴性', '低怎么回事', '偏低', '低是怎么回事', '阴', '低']
        self.notice_qwds = ['注意', '日常保养', '生活上', '日常护理', '吸收', '饭前', '饭后', '空腹']
        self.infectivity_qwds = ['传染', '传播']
        self.inheritance_qwds = ['遗传', '后代']
        self.tolerance_qwds = ['耐药', '耐药性']
        self.by_effect_qwds = ['副作用', '有伤害']
        self.can_eat_qwds = ['可以吃', '可以喝', '有用', '管用']
        self.related_qwds = ['有关系', '相关', '有关', '是不是因为']
        self.replace_qwds = ['可以换']
        self.miss_qwds = ['漏服', '忘吃', '补服']
        self.period_qwds = ['疗程', '月了', '星期了', '周了']
        self.advantage_qwds = ['优势', '优点']
        self.pregnant_qwds = ['怀孕', '要孩子', '备孕']
        self.infect_prevent_qwds = ['被传染', '病人接触']
        self.process_qwds = ['病程', '代偿期']
        self.examination_qwds = ['体检', '入职体检']
        self.organ_damage_qwds = ['受损', '受伤', '损伤']
        self.not_do_qwds = []


        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        data['question'] = question
        medical_dict = self.check_medical(question)
        # medical_dict: {'肝硬化': ['disease'], '乙肝': ['disease']}
        #print(medical_dict)
        '''
        if not medical_dict:   # 如果当前问题没有查到实体，就查看之前问题有没有保存实体
            if diseases_dict != '':
                medical_dict = diseases_dict
            else:
                return {}
        '''
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状 简单的判断问句中是否有字典里的词语
        # 检查项偏低问题
        if self.check_words(self.check_item_low_qwds, question) and ('check_item' in types):
            question_type = 'check_item_low'
            question_types.append(question_type)

        # 检查项偏高问题
        if self.check_words(self.check_item_high_qwds, question) and ('check_item' in types):
            question_type = 'check_item_high'
            question_types.append(question_type)

        # 检查注意事项问题
        if self.check_words(self.notice_qwds, question) and ('check_item' in types or 'check' in types):
            question_type = 'check_notice'
            question_types.append(question_type)

        # 传染问题
        if self.check_words(self.infectivity_qwds, question) and ('disease' in types):
            question_type = 'disease_infectivity'
            question_types.append(question_type)

        # 遗传问题
        if self.check_words(self.inheritance_qwds, question) and ('disease' in types):
            question_type = 'disease_inheritance'
            question_types.append(question_type)

        # 根据疾病问症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        # 根据症状问可能的疾病
        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 根据疾病问原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        # 可以吃/喝 xx吗？
        if self.check_words(self.can_eat_qwds, question) and 'disease' in types:
            question_type = 'can_eat'
            question_types.append(question_type)

        # 根据疾病推荐食品（分为宜吃和不宜吃）
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        # 已知食物找疾病 （什么病不能吃什么食物，食物对哪些病有好处）
        if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        # 推荐药品 什么病吃什么药
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 什么药治什么病
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds+self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        # 疾病的预防措施
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cure'
            question_types.append(question_type)

        # 疾病日常保养
        if self.check_words(self.notice_qwds, question) and 'disease' in types:
            question_type = 'disease_notice'
            question_types.append(question_type)

        # 药物的耐药性
        if self.check_words(self.tolerance_qwds, question) and 'drug' in types:
            question_type = 'drug_tolerance'
            question_types.append(question_type)

        # 药物注意事项
        if self.check_words(self.notice_qwds, question) and 'drug' in types:
            question_type = 'drug_notice'
            question_types.append(question_type)

        # 药物副作用
        if self.check_words(self.by_effect_qwds, question) and 'drug' in types:
            question_type = 'drug_byeffect'
            question_types.append(question_type)

        # 检查项查什么病
        if self.check_words(self.check_qwds, question) and 'check_item' in types:
            question_type = 'check_item_disease'
            question_types.append(question_type)

        # xx和xx疾病有关系吗
        if self.check_words(self.related_qwds, question) and 'disease' in types:
            question_type = 'related_disease'
            question_types.append(question_type)

        # 药物更换问题(知识库还没有)
        if self.check_words(self.replace_qwds, question) and 'drug' in types:
            question_type = 'drug_replace' 
            question_types.append(question_type)

        # 药物漏服问题
        if self.check_words(self.miss_qwds, question) and 'drug' in types:
            question_type = 'drug_missed'
            question_types.append(question_type)

        # 药物禁忌行为
        if self.check_words(self.not_do_qwds , question) and 'drug' in types:
            question_type = 'drug_not_do'
            question_types.append(question_type)

        # 药物疗程问题
        if self.check_words(self.period_qwds, question) and 'drug' in types:
            question_type = 'drug_period'
            question_types.append(question_type)

        # 药物优点
        if self.check_words(self.advantage_qwds, question) and 'drug' in types:
            question_type = 'drug_advantage'
            question_types.append(question_type)

        # 疾病备孕问题
        if self.check_words(self.pregnant_qwds, question) and 'disease' in types:
            question_type = 'disease_pregnant'
            question_types.append(question_type)

        # 疾病禁忌行为问题
        if self.check_words(self.not_do_qwds , question) and 'disease' in types:
            question_type = 'disease_not_do'
            question_types.append(question_type)

        # 疾病预防传染问题
        if self.check_words(self.infect_prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_infect_prevent'
            question_types.append(question_type)

        # 疾病发展过程问题
        if self.check_words(self.process_qwds, question) and 'disease' in types:
            question_type = 'disease_process'
            question_types.append(question_type)

        # 疾病入职体检问题
        if self.check_words(self.examination_qwds, question) and 'disease' in types:
            question_type = 'disease_entry_examination'
            question_types.append(question_type)

        # 器官禁忌行为问题
        if self.check_words(self.not_do_qwds , question) and 'organ' in types:
            question_type = 'organ_not_do'
            question_types.append(question_type)

        # 器官损伤表现问题
        if self.check_words(self.organ_damage_qwds, question) and 'organ' in types:
            question_type = 'organ_damage'
            question_types.append(question_type)

        # 检查项副作用问题
        if self.check_words(self.by_effect_qwds, question) and ('check_item' in types or 'check' in types):
            question_type = 'check_byeffect'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该药品的描述信息返回
        if question_types == [] and 'drug' in types:
            question_types = ['drug_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该检查项的描述信息返回
        if question_types == [] and 'check' in types:
            question_types = ['check_desc']

        # 若没有查到相关的外部查询信息，那么则将该检查项指标的描述信息返回
        if question_types == [] and 'check_item' in types:
            question_types = ['check_item_desc']


        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.check_item_wds:
                wd_dict[wd].append('check_item')
            if wd in self.behavior_wds:
                wd_dict[wd].append('behavior')
            if wd in self.organ_wds:
                wd_dict[wd].append('organ')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        # iter方法返回一个元组形如(1, (5822, '乙肝'))
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        # 这一步操作是用来去掉，例如["硬化", "肝硬化"]，我们想要的明显是长的那个词，我们要把属于子集的词给去掉。
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        global diseases_dict
        if final_dict:  # 如果当前的问题里有新的实体，则更新
            diseases_dict = final_dict
        # final_dict形如：{'乙肝': ['disease']}
        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                print(wd)
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)