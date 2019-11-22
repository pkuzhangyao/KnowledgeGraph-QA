#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: zhangyao
# Date: 19-11-1

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        # dict.items返回的是可遍历的(键-值)元组数组
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    # res_classifer: {'args': {'乙肝': ['disease']}, 'question_types': ['disease_cureway'], 'question' : []}
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        # entity_dict: {'food': ['鸡蛋']}
        #print("entity_dict:", entity_dict)
        question_types = res_classify['question_types']
        res_sql = {}
        res_sql['question'] = res_classify['question']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cure':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_infectivity':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_inheritance':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_notice':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_tolerance':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_notice':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_byeffect':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'check_item_low':
                sql = self.sql_transfer(question_type, entity_dict.get('check_item'))

            elif question_type == 'check_item_high':
                sql = self.sql_transfer(question_type, entity_dict.get('check_item'))

            elif question_type == 'can_eat':
                sql = self.sql_transfer('disease_not_food', entity_dict.get('disease'))

            elif question_type == 'related_disease':
                sql = self.sql_transfer('disease_symptom', entity_dict.get('disease'))

            elif question_type == 'check_item_disease':
                sql = self.sql_transfer('check_item_disease', entity_dict.get('check_item'))

            elif question_type == 'check_notice':
                if 'check' in entity_dict:
                    entity = entity_dict.get('check')
                else:
                    entity = entity_dict.get('check_item')
                sql = self.sql_transfer('check_notice', entity)

            elif question_type == 'check_desc':
                sql = self.sql_transfer('check_desc', entity_dict.get('check'))

            elif question_type == 'check_item_desc':
                sql = self.sql_transfer('check_item_desc', entity_dict.get('check_item'))

            elif question_type == 'drug_replace':
                sql = self.sql_transfer('drug_replace', entity_dict.get('drug'))

            elif question_type == 'drug_missed':
                sql = self.sql_transfer('drug_missed', entity_dict.get('drug'))

            elif question_type == 'drug_not_do':
                sql = self.sql_transfer('drug_not_do', entity_dict.get('drug'))

            elif question_type == 'drug_period':
                sql = self.sql_transfer('drug_period', entity_dict.get('drug'))

            elif question_type == 'drug_advantage':
                sql = self.sql_transfer('drug_advantage', entity_dict.get('drug'))

            elif question_type == 'disease_pregnant':
                sql = self.sql_transfer('disease_pregnant', entity_dict.get('disease'))

            elif question_type == 'disease_not_do':
                sql = self.sql_transfer('disease_not_do', entity_dict.get('disease'))

            elif question_type == 'disease_infect_prevent':
                sql = self.sql_transfer('disease_infect_prevent', entity_dict.get('disease'))

            elif question_type == 'disease_process':
                sql = self.sql_transfer('disease_process', entity_dict.get('disease'))

            elif question_type == 'disease_entry_examination':
                sql = self.sql_transfer('disease_entry_examination', entity_dict.get('disease'))

            elif question_type == 'organ_not_do':
                sql = self.sql_transfer('organ_not_do', entity_dict.get('organ'))

            elif question_type == 'organ_damage':
                sql = self.sql_transfer('organ_damage', entity_dict.get('organ'))

            elif question_type == 'check_byeffect':
                if 'check' in entity_dict:
                    entity = entity_dict.get('check')
                else:
                    entity = entity_dict.get('check_item')
                sql = self.sql_transfer('check_byeffect', entity)

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        res_sql['sqls'] = sqls

        return res_sql

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的治愈情况
        elif question_type == 'disease_cure':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.cure".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' or '{0}' in n.another_name return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}'return m.name, r.name, n.name".format(i) for i in entities]

        # 疾病传染性
        elif question_type == 'disease_infectivity':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.infectivity".format(i) for i in entities]

        # 疾病遗传性
        elif question_type == 'disease_inheritance':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.inheritance".format(i) for i in entities]

        # 疾病保养问题
        elif question_type == 'disease_notice':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name return m.name, m.notice".format(i) for i in entities]

        # 药品耐药性问题
        elif question_type == 'drug_tolerance':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.tolerance".format(i) for i in entities]

        # 药品注意事项问题
        elif question_type == 'drug_notice':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.drug_notice".format(i) for i in entities]

        # 药品副作用
        elif question_type == 'drug_byeffect':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.by_effect".format(i) for i in entities]

        # 药品介绍
        elif question_type == 'drug_desc':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.desc".format(i) for i in entities]

        # 检查指标偏低
        elif question_type == 'check_item_low':
            sql = ["MATCH (m:Check_item) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.low_negative".format(i) for i in entities]

        # 检查指标偏高
        elif question_type == 'check_item_high':
            sql = ["MATCH (m:Check_item) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.high_positive".format(i) for i in entities]

        # 检查项查什么病
        elif question_type == 'check_item_disease':
            sql = ["MATCH (m:Disease)-[r:need_check_item]->(n:Check_item) where n.name = '{0}' or '{0}' in n.another_name return m.name, n.name".format(i) for i in entities]

        elif question_type == 'check_notice':
            sql = ["MATCH (m:Check)-[r:has_item]->(n:Check_item) where n.name = '{0}' or '{0}' in n.another_name or m.name='{0}' or '{0}'in m.another_name return m.name,n.name, m.notice".format(i) for i in entities]

        elif question_type == 'check_desc':
            sql = ["MATCH (m:Check) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.desc".format(i) for i in entities]

        elif question_type == 'check_item_desc':
            sql = ["MATCH (m:Check_item) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.desc".format(i) for i in entities]

        elif question_type == 'drug_replace':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.replace".format(i) for i in entities]

        elif question_type == 'drug_missed':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.missed".format(i) for i in entities]

        elif question_type == 'drug_not_do':
            sql = ["MATCH (m:Drug)-[r:drug_not_do]->(n:Behavior) where m.name='{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'drug_period':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.treatment_period".format(i) for i in entities]

        elif question_type == 'drug_advantage':
            sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.advantage".format(i) for i in entities]

        elif question_type == 'disease_pregnant':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.pregnant".format(i) for i in entities]

        elif question_type == 'disease_not_do':
            sql = ["MATCH (m:Disease)-[r:not_do]->(n:Behavior) where m.name='{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_infect_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.infect_prevent".format(i) for i in entities]

        elif question_type == 'disease_process':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.process".format(i) for i in entities]

        elif question_type == 'disease_entry_examination':
            sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.entry_examination".format(i) for i in entities]

        elif question_type == 'organ_not_do':
            sql = ["MATCH (m:Organ)-[r:organ_not_do]->(n:Behavior) where m.name='{0}' or '{0}' in m.another_name return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'organ_damage':
            sql = ["MATCH (m:Organ) where m.name = '{0}' return m.name, m.damage".format(i) for i in entities]

        elif question_type == 'check_byeffect':
            sql = ["MATCH (m:Check)-[r:has_item]->(n:Check_item) where n.name = '{0}' or '{0}' in n.another_name or m.name='{0}' or '{0}'in m.another_name return m.name,n.name, m.by_effect".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
