#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: zhangyao
# Date: 19-11-1

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls['sqls']:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                # .data返回的是一个字典组成的列表[{"n.name":"xx", "m.name":"xx", "r.name":"xx(关系名称，如"宜吃")"
                #print("ress:", ress)
                answers += ress
            final_answer = self.answer_prettify(question_type, answers, sqls['question'])
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers, question):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            #final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            final_answer = '；'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_cure':
            desc = [i['m.cure'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '；'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            #final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))
            final_answer = '您问的问题暂时还不能回答，先帮你介绍一下{0}吧：\n{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_infectivity':
            desc = [i['m.infectivity'] for i in answers]
            #subject = answers[0]['m.name']
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_inheritance':
            desc = [i['m.inheritance'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_notice':
            desc = [i['m.notice'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_tolerance':
            desc = [i['m.tolerance'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_byeffect':
            desc = [i['m.by_effect'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_notice':
            desc = [i['m.drug_notice'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            # final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))
            final_answer = '您问的问题暂时还不能回答，先帮你介绍一下{0}吧：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_item_low':
            desc = [i['m.low_negative'] for i in answers]
            final_answer = '；'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'check_item_high':
            desc = [i['m.high_positive'] for i in answers]
            final_answer = '；'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'can_eat':
            desc = [i['n.name'] for i in answers]
            for item in desc:
                if item in question:
                    final_answer = '不可以哦。'
                    return final_answer
            final_answer = '可以，适量即可。'

        elif question_type == 'related_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            for item in desc:
                if item in question:
                    final_answer = '{0}是{1}的常见症状。'.format(item, subject)
                    return  final_answer
            final_answer = '一般没有关系。'

        elif question_type == 'check_item_disease':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'check_notice':
            desc = answers[0]['m.notice']
            subject = answers[0]['m.name']
            final_answer = '做{0}检查的注意事项如下：\n{1}'.format(subject, desc)

        elif question_type == 'check_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '您问的问题暂时还不能回答，先帮你介绍一下{0}吧：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_item_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '您问的问题暂时还不能回答，先帮你介绍一下{0}吧：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_replace':
            desc = [i['m.replace'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_missed':
            desc = [i['m.missed'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_not_do':
            #sql = ["MATCH (m:Drug)-[r:drug_not_do]->(n:Behavior) where m.name='{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            for item in desc:
                if item in question:
                    final_answer = '服用{0}期间是要杜绝{1}的。'.format(item, subject)
                    return final_answer
            final_answer = '可以的，但要杜绝{0}。'.format(';'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_period':
            #sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.treatment_period".format(i) for i in entities]
            desc = [i['m.treatment_period'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'drug_advantage':
            #sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.advantage".format(i) for i in entities]
            desc = [i['m.advantage'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_pregnant':
            #sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.pregnant".format(i) for i in entities]
            desc = [i['m.pregnant'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_not_do':
            #sql = ["MATCH (m:Disease)-[r:not_do]->(n:Behavior) where m.name='{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            for item in desc:
                if item in question:
                    final_answer = '{1}患者是要杜绝{0}de。'.format(item, subject)
                    return final_answer
            final_answer = '可以的，但要杜绝{0}。'.format(';'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_infect_prevent':
            #sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.infect_prevent".format(i) for i in entities]
            desc = [i['m.infect_prevent'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_process':
            #sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.process".format(i) for i in entities]
            desc = [i['m.process'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'disease_entry_examination':
            #sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.entry_examination".format(i) for i in entities]
            desc = [i['m.entry_examination'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'organ_not_do':
            #sql = ["MATCH (m:Organ)-[r:organ_not_do]->(n:Behavior) where m.name='{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            for item in desc:
                if item in question:
                    final_answer = '{1}损伤的患者是要杜绝{0}de。'.format(item, subject)
                    return final_answer
            final_answer = '可以的，但要杜绝{0}。'.format(';'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'organ_damage':
            #sql = ["MATCH (m:Organ) where m.name = '{0}' return m.name, m.damage".format(i) for i in entities]
            desc = [i['m.damage'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        elif question_type == 'check_byeffect':
            #sql = ["MATCH (m:Check)-[r:has_item]->(n:Check_item) where n.name = '{0}' or '{0}' in n.another_name or m.name='{0}' or '{0}'in m.another_name return m.name,n.name, m.by_effect".format(i) for i in entities]
            desc = [i['m.by_effect'] for i in answers]
            final_answer = ';'.join(list(set(desc))[:self.num_limit])

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    res_sql = [{'question_type': 'disease_do_food', 'sql': ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '脑膜炎' return m.name, r.name, n.name", "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '脑膜炎' return m.name, r.name, n.name"]}]
    print(searcher.search_main(res_sql))