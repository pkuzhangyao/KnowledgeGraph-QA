#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: zhangyao
# Date: 19.10.24

import os
import json
from py2neo import Graph, Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.check_item_path = os.path.join(cur_dir, 'data/check_item.json')
        self.disease_path = os.path.join(cur_dir, 'data/disease.json')
        self.drug_path = os.path.join(cur_dir, 'data/drug.json')
        self.check_path = os.path.join(cur_dir, 'data/check.json')
        self.organ_path = os.path.join(cur_dir, 'data/organ.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")


    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        drugs = []  # 药品
        foods = []  # 食物
        checks = []  # 检查
        check_items = []  # 检查项指标
        diseases = []  # 疾病
        symptoms = []  # 症状
        organs = []  # 器官
        behaviors = []  # 行为
        drugs_another_name = []  # 药物别名  这里主要用来导出词典
        check_items_another_name = []  # 检查项指标别名
        disease_another_name = []  # 疾病别名
        check_another_name = []  # 检查项别名
        drugs_infos = []  # 药物信息
        disease_infos = []  # 疾病信息
        check_item_infos = []  # 检查项指标信息
        checks_infos = []  # 检查项信息
        organ_infos = []  # 器官信息

        # 构建疾病节点实体关系
        rels_check = []  # 疾病－检查关系
        rels_return_check = []  # 疾病-复查检查关系
        rels_check_item = []  # 疾病-检查项关系
        rels_doeat = []  # 疾病－宜吃食物关系
        rels_noteat = []  # 疾病－忌吃食物关系
        rels_recommandeat = []  # 疾病-推荐食物关系
        rels_transfer = []  # 疾病-疾病转化关系
        rels_acompany = []  # 疾病并发关系
        rels_symptom = []  # 疾病症状关系
        rels_drug = []  # 疾病－通用药品关系
        rels_notdo = []  # 疾病-行为关系

        # 构建其他实体关系
        rels_has_item = []  # 检查项-检查项指标关系
        rels_check_item_drug = []  # 检查项指标-需要药物关系
        rels_drug_not_do = []  # 药品禁忌-行为关系
        rels_organ_not_do = []  # 器官受损-行为关系

        count = 0
        for data in open(self.disease_path, encoding="utf-8"):
            disease_dict = {}
            count += 1
            print("disease_node:", count)
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['another_name'] = ''
            disease_dict['desc'] = ''
            disease_dict['infectivity'] = ''
            disease_dict['inheritance'] = ''
            disease_dict['cure'] = ''
            disease_dict['treatment'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['get_prob'] = ''
            disease_dict['notice'] = ''
            disease_dict['infect_prevent'] = ''
            disease_dict['entry_examination'] = ''
            disease_dict['diagnostic_criteria'] = ''
            disease_dict['process'] = ''
            disease_dict['pregnant'] = ''

            if 'another_name' in data_json:
                disease_dict['another_name'] = data_json['another_name']
                for another_name in data_json['another_name']:
                    disease_another_name.append(another_name)

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'infectivity' in data_json:
                disease_dict['infectivity'] = data_json['infectivity']

            if 'inheritance' in data_json:
                disease_dict['inheritance'] = data_json['inheritance']

            if 'cure' in data_json:
                disease_dict['cure'] = data_json['cure']

            if 'treatment' in data_json:
                disease_dict['treatment'] = data_json['treatment']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'notice' in data_json:
                disease_dict['notice'] = data_json['notice']

            if 'infect_prevent' in data_json:
                disease_dict['infect_prevent'] = data_json['infect_prevent']

            if 'entry_examination' in data_json:
                disease_dict['entry_examination'] = data_json['entry_examination']

            if 'diagnostic_criteria' in data_json:
                disease_dict['diagnostic_criteria'] = data_json['diagnostic_criteria']

            if 'process' in data_json:
                disease_dict['process'] = data_json['process']

            if 'pregnant' in data_json:
                disease_dict['pregnant'] = data_json['pregnant']

            if 'check' in data_json:
                checks += data_json['check']
                for check in data_json['check']:
                    rels_check.append([disease, check])

            if 'return_visit' in data_json:
                checks += data_json['return_visit']
                for check in data_json['return_visit']:
                    rels_return_check.append([disease, check])

            if 'check_item' in data_json:
                check_items += data_json['check_item']
                for check_item in data_json['check_item']:
                    rels_check_item.append([disease, check_item])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])

                foods += not_eat
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do])

                foods += do_eat
                recommand_eat = data_json['recommand_eat']

                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if 'transfer' in data_json:
                diseases += data_json['transfer']
                for transfer_disease in data_json['transfer']:
                    rels_transfer.append([disease, transfer_disease])

            if 'acompany' in data_json:
                diseases += data_json['acompany']
                for acompany_disease in data_json['acompany']:
                    rels_acompany.append([disease, acompany_disease])

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'common_drug' in data_json:
                drugs += data_json['common_drug']
                for drug in data_json['common_drug']:
                    rels_drug.append([disease, drug])

            if 'not_do' in data_json:
                behaviors += data_json['not_do']
                for behavior in data_json['not_do']:
                    rels_notdo.append([disease, behavior])

            disease_infos.append(disease_dict)

        count = 0
        for data in open(self.drug_path, encoding="utf-8"):
            drug_dict = {}
            count += 1
            print("drug_node:", count)
            data_json = json.loads(data)
            drug = data_json['name']
            drug_dict['name'] = drug
            drugs.append(drug)
            drug_dict['another_name'] = ''
            drug_dict['drug_desc'] = ''
            drug_dict['tolerance'] = ''
            drug_dict['by_effect'] = ''
            drug_dict['drug_notice'] = ''
            drug_dict['treatment_period'] = ''
            drug_dict['missed'] = ''
            drug_dict['advantage'] = ''
            drug_dict['replace'] = ''

            if 'another_name' in data_json:
                drug_dict['another_name'] = data_json['another_name']
                for another_name in data_json['another_name']:
                    drugs_another_name.append(another_name)

            if 'drug_desc' in data_json:
                drug_dict['drug_desc'] = data_json['drug_desc']

            if 'tolerance' in data_json:
                drug_dict['tolerance'] = data_json['tolerance']

            if 'by_effect' in data_json:
                drug_dict['by_effect'] = data_json['by_effect']

            if 'drug_notice' in data_json:
                drug_dict['drug_notice'] = data_json['drug_notice']

            if 'treatment_period' in data_json:
                drug_dict['treatment_period'] = data_json['treatment_period']

            if 'missed' in data_json:
                drug_dict['missed'] = data_json['missed']

            if 'advantage' in data_json:
                drug_dict['advantage'] = data_json['advantage']

            if 'replace' in data_json:
                drug_dict['replace'] = data_json['replace']

            if 'not_do' in data_json:
                behaviors += data_json['not_do']
                for behavior in data_json['not_do']:
                    rels_drug_not_do.append([drug, behavior])

            drugs_infos.append(drug_dict)

        count = 0
        for data in open(self.check_item_path, encoding="utf-8"):
            check_item_dict = {}
            count += 1
            print("check_item_node:", count)
            data_json = json.loads(data)
            check_item = data_json['name']
            check_items.append(check_item)
            check_item_dict['name'] = check_item
            check_item_dict['another_name'] = ''
            check_item_dict['low/negative'] = ''
            check_item_dict['high/positive'] = ''
            check_item_dict['desc'] = ''
            check_item_dict['transfer'] = ''
            check_item_dict['threshold'] = ''

            if 'another_name' in data_json:
                check_item_dict['another_name'] = data_json['another_name']
                for another_name in data_json['another_name']:
                    check_items_another_name.append(another_name)

            if 'low/negative' in data_json:
                check_item_dict['low/negative'] = data_json['low/negative']

            if 'high/positive' in data_json:
                check_item_dict['high/positive'] = data_json['high/positive']

            if 'desc' in data_json:
                check_item_dict['desc'] = data_json['desc']

            if 'transfer' in data_json:
                check_item_dict['transfer'] = data_json['transfer']

            if 'threshold' in data_json:
                check_item_dict['threshold'] = data_json['threshold']

            if 'need_drug' in data_json:
                drugs += data_json['need_drug']
                for drug in data_json['need_drug']:
                    rels_check_item_drug.append([check_item, drug])

            check_item_infos.append(check_item_dict)

        count = 0
        for data in open(self.check_path, encoding="utf-8"):
            check_dict = {}
            count += 1
            print("check_node:", count)
            data_json = json.loads(data)
            check = data_json['name']
            checks.append(check)
            check_dict['name'] = check
            check_dict['another_name'] = ''
            check_dict['desc'] = ''
            check_dict['by_effect'] = ''
            check_dict['notice'] = ''

            if 'another_name' in data_json:
                check_dict['another_name'] = data_json['another_name']
                for another_name in data_json['another_name']:
                    check_another_name.append(another_name)

            if 'desc' in data_json:
                check_dict['desc'] = data_json['desc']

            if 'by_effect' in data_json:
                check_dict['by_effect'] = data_json['by_effect']

            if 'notice' in data_json:
                check_dict['notice'] = data_json['notice']

            if 'has_item' in data_json:
                check_items += data_json['has_item']
                for check_item in data_json['has_item']:
                    rels_has_item.append([check, check_item])

            checks_infos.append(check_dict)

        count = 0
        for data in open(self.organ_path, encoding="utf-8"):
            organ_dict = {}
            count += 1
            print("organ_node:", count)
            data_json = json.loads(data)
            organ = data_json['name']
            organs.append(organ)
            organ_dict['name'] = organ
            organ_dict['damage'] = ''

            if 'damage' in data_json:
                organ_dict['damage'] = data_json['damage']

            if 'not_do' in data_json:
                behaviors += data_json['not_do']
                for behavior in data_json['not_do']:
                    rels_organ_not_do.append([organ, behavior])

            organ_infos.append(organ_dict)



        #print("diseases:", set(diseases))
        #print("disease_info:", disease_infos)
        #print("drugs:", set(drugs))
        #print("rels_check_item:", rels_check_item)
        #print("drug_infos:", drugs_infos)
        #print("check_item_infos:", check_item_infos)
        print("rels_check_tiem:", rels_check_item)
        print("rels_has_item:", rels_has_item)
        print("rels_not_do:", rels_notdo)
        print("rels_drug_not_do:", rels_drug_not_do)
        return set(drugs), set(foods), set(checks), set(check_items), set(diseases), set(symptoms), set(organs), set(behaviors), drugs_infos, disease_infos, check_item_infos, \
                checks_infos, organ_infos, rels_check, rels_return_check, rels_check_item, rels_doeat, rels_noteat, rels_recommandeat, rels_transfer, rels_acompany, rels_symptom, \
                rels_drug, rels_notdo, rels_has_item, rels_check_item_drug, rels_drug_not_do, rels_organ_not_do, disease_another_name, drugs_another_name, check_another_name, check_items_another_name


    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            #print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'],another_name=disease_dict['another_name'], desc=disease_dict['desc'], infectivity=disease_dict['infectivity'],
                        inheritance=disease_dict['inheritance'], cure=disease_dict['cure'], treatment = disease_dict['treatment'],
                        prevent=disease_dict['prevent'], cause=disease_dict['cause'], get_prob=disease_dict['get_prob'],
                        notice=disease_dict['notice'], infect_prevent=disease_dict['infect_prevent'],
                        entry_examination=disease_dict['entry_examination'], diagnostic_criteria=disease_dict['diagnostic_criteria'],
                        process=disease_dict['process'], pregnant=disease_dict['pregnant'])
            self.g.create(node)
            count += 1
            print("疾病中心节点：",count)
        return

    '''创建药品节点'''
    def create_drug_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            node = Node("Drug", name=drug_dict['name'], desc=drug_dict['drug_desc'],
                        another_name=drug_dict['another_name'], tolerance=drug_dict['tolerance'],
                        by_effect=drug_dict['by_effect'], drug_notice=drug_dict['drug_notice'],
                        treatment_period=drug_dict['treatment_period'], missed=drug_dict['missed'],
                        advantage=drug_dict['advantage'], replace=drug_dict['replace']
                        )
            self.g.create(node)
            count += 1
            print("药物节点：",count)
        return

    '''创建检查项指标节点'''
    def create_check_item_nodes(self, check_item_infos):
        count = 0
        for check_item_dict in check_item_infos:
            node = Node("Check_item", name=check_item_dict['name'], another_name=check_item_dict['another_name'], desc=check_item_dict['desc'],
                        low_negative=check_item_dict['low/negative'], high_positive=check_item_dict['high/positive'],
                        transfer=check_item_dict['transfer'], threshold=check_item_dict['threshold'])
            self.g.create(node)
            count += 1
            print("检查项指标节点", count)
        return

    '''创建检查项节点'''
    def create_check_nodes(self, checks_infos):
        count = 0
        for check_dict in checks_infos:
            node = Node("Check", name=check_dict['name'], another_name=check_dict['another_name'], desc=check_dict['desc'],
                        by_effect=check_dict['by_effect'], notice=check_dict['notice'])
            self.g.create(node)
            count += 1
            print("检查项节点", count)

    '''创建器官节点'''
    def creat_organ_nodes(self, organ_infos):
        count = 0
        for organ_dict in organ_infos:
            node = Node("Organ", name=organ_dict['name'], damage=organ_dict['damage'])
            self.g.create(node)
            count += 1
            print("器官节点", count)

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Drugs, Foods, Checks, Check_items, Diseases, Symptoms, Organs, Behaviors, drugs_infos, disease_infos, check_item_infos, checks_infos, organ_infos,rels_check, rels_return_check, rels_check_item, rels_doeat, rels_noteat, rels_recommandeat, rels_transfer, rels_acompany, rels_symptom, \
                rels_drug, rels_notdo, rels_has_item, rels_check_item_drug, rels_drug_not_do, rels_organ_not_do, disease_another_name, drugs_another_name, check_another_name, check_items_another_name = self.read_nodes()
        self.create_diseases_nodes(disease_infos)  # 创建中心疾病节点
        self.create_drug_nodes(drugs_infos)  # 创建中心药物节点
        self.create_check_item_nodes(check_item_infos)  # 创建中心检查项指标节点
        self.create_check_nodes(checks_infos)  # 创建中心检查项节点
        self.creat_organ_nodes(organ_infos)  # 创建中心检查节点
        self.create_node('Food', Foods)
        print("食品节点共有：", len(Foods))
        self.create_node('Behavior', Behaviors)
        print("器官节点共有：", len(Behaviors))
        self.create_node('Symptom', Symptoms)
        print("症状节点共有：", len(Symptoms))
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Check_items, Diseases, Symptoms, Organs, Behaviors, drugs_infos, disease_infos, check_item_infos, checks_infos, organ_infos, rels_check, rels_return_check, rels_check_item, rels_doeat, rels_noteat, rels_recommandeat, rels_transfer, rels_acompany, rels_symptom, \
        rels_drug, rels_notdo, rels_has_item, rels_check_item_drug, rels_drug_not_do, rels_organ_not_do, disease_another_name, drugs_another_name, check_another_name, check_items_another_name = self.read_nodes()
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Check', rels_return_check, 'return_visit', '复查项目')
        self.create_relationship('Disease', 'Check_item', rels_check_item, 'need_check_item', '常用检查项')
        self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Disease', 'Disease', rels_transfer, 'transfer', '疾病转化')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany', '并发症')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '常见症状')
        self.create_relationship('Disease', 'Drug', rels_drug, 'common_drug', '常用药品')
        self.create_relationship('Disease', 'Behavior', rels_notdo, 'not_do', '禁忌行为')
        self.create_relationship('Check', 'Check_item', rels_has_item, 'has_item', '包含检查项')
        self.create_relationship('Check_item', 'Drug', rels_check_item_drug, 'check_item_drug', '检查项异常所需药物')
        self.create_relationship('Drug', 'Behavior', rels_drug_not_do, 'drug_not_do', '药物禁忌行为')
        self.create_relationship('Organ', 'Behavior', rels_organ_not_do, 'organ_not_do', '器官损伤禁忌行为')


    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            # 关系的属性
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Check_items, Diseases, Symptoms, Organs, Behaviors, drugs_infos, disease_infos, check_item_infos, checks_infos, organ_infos, rels_check, rels_return_check, rels_check_item, rels_doeat, rels_noteat, rels_recommandeat, rels_transfer, rels_acompany, rels_symptom, \
        rels_drug, rels_notdo, rels_has_item, rels_check_item_drug, rels_drug_not_do, rels_organ_not_do, disease_another_name, drugs_another_name, check_another_name, check_items_another_name = self.read_nodes()
        f_drug = open('./dict/drug.txt', 'w+', encoding="utf-8")
        f_food = open('./dict/food.txt', 'w+', encoding="utf-8")
        f_check = open('./dict/check.txt', 'w+', encoding="utf-8")
        f_symptom = open('./dict/symptoms.txt', 'w+', encoding="utf-8")
        f_disease = open('./dict/disease.txt', 'w+', encoding="utf-8")
        f_check_item = open('./dict/check_item.txt', 'w+', encoding="utf-8")
        f_organs = open('./dict/organ.txt', 'w+', encoding="utf-8")
        f_behaviors = open('./dict/behaviors.txt', 'w+', encoding="utf-8")
        print('\n'.join(list(Drugs)))
        print("--------分割线-------")
        print('\n'.join(list(drugs_another_name)))

        f_drug.write('\n'.join(list(Drugs)))
        f_drug.write('\n')
        f_drug.write('\n'.join(list(drugs_another_name)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_check.write('\n')
        f_check.write('\n'.join(list(check_another_name)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))
        f_disease.write('\n')
        f_disease.write('\n'.join(list(disease_another_name)))
        f_check_item.write('\n'.join(list(Check_items)))
        f_check_item.write('\n')
        f_check_item.write('\n'.join(list(check_items_another_name)))
        f_organs.write('\n'.join(list(Organs)))
        f_behaviors.write('\n'.join(list(Behaviors)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_symptom.close()
        f_disease.close()
        f_check_item.close()

        return



if __name__ == '__main__':
    handler = MedicalGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()