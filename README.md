# KnowledgeGraph-QA
基于知识图谱和相似度匹配的肝病智能问答系统

本项目参考了中科院刘焕勇老师的刘焕勇老师在github上的开源项目，基于知识图谱的医药领域问答项目QABasedOnMedicaKnowledgeGraph。
该项目立足医药领域，以垂直型医药网站为数据来源，以疾病为核心，构建起一个包含7类规模为4.4万的知识实体，11类规模约30万实体关系的知识图谱。
原始数据包含8000多种病，和肝病相关的有200多种病。

原项目地址：[https://github.com/liuhuanyong/QASystemOnMedicalKG](https://github.com/liuhuanyong/QASystemOnMedicalKG)

在此基础上，我修改了知识图谱结构，针对常见的三种肝病为中心，重新建立了知识图谱，并增加了当知识图谱不能解决问题时通过相似度匹配的方法查询问答库选择相似问题并返回答案的方法。
## 整体流程
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191126113826220.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzkxNDY5Mg==,size_16,color_FFFFFF,t_70)
## 知识图谱结构
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019112611462170.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzkxNDY5Mg==,size_16,color_FFFFFF,t_70)
