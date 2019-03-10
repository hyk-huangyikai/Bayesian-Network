import time

class Bayes():

    def build_node(self):
        #创建变量结点
        self.B = Node('B', ['B'])
        self.E = Node('E', ['E'])
        self.A = Node('A', ['A', 'B', 'E'])
        self.J = Node('J', ['J', 'A'])
        self.M = Node('M', ['M', 'A'])

        #生成各个变量结点的条件概率
        self.B.set_proba({'0': 0.999, '1': 0.001})
        self.E.set_proba({'0': 0.998, '1': 0.002})
        self.A.set_proba({'111': 0.95, '011': 0.05, '110': 0.94, '010': 0.06,
                '101':0.29, '001': 0.71, '100': 0.001, '000': 0.999})
        self.J.set_proba({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
        self.M.set_proba({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})
        #已知变量的取值
        self.var_list = [['B',0],
                         ['E',0],
                         ['A',0],
                         ['J',0],
                         ['M',0]] 
        #变量的数目
        self.variable_num = 5
    
    #对变量进行取特定值
    def take_specific_value(self,node,variable,value):
        #定位变量列表中取特定值变量的位置
        index = node.variable_list.index(variable)
        #新的取值集合
        new_proba = {}
        #遍历原变量取值的key值
        for key in node.proba:
            #如果符合取值，则放入新集合
            if key[index] == str(value):
                new_proba[key] = node.proba[key]
        #生成新的变量结点
        new_node = Node(node.name,node.variable_list)
        new_node.set_proba(new_proba)
        return new_node

    #计算全概率的具体实现
    def calculate_pro(self,node_list,variable_list):
        res = 1
        #利用链式法则，按照变量顺序依次相乘
        for i in range(len(node_list)):
            #对于每一个变量结点，检查包含哪些变量
            for j in range(0,i+1):
                #检查当前变量是否在变量结点的变量列表中
                if variable_list[j][0] in node_list[i].variable_list:
                    #取特定值的概率
                    node_list[i] = self.take_specific_value(node_list[i],variable_list[j][0],variable_list[j][1])
            #将特定值的概率进行累乘
            res = res * list(node_list[i].proba.values())[0]
        return res

    #计算前进行变量集合初始化
    def probability(self,value_list):
        #声明变量结点顺序集合
        node_list = [self.B,self.E,self.A,self.J,self.M]
        #给已知变量赋予特定值
        for i in range(len(self.var_list)):
            self.var_list[i][1] = value_list[i]
        #计算全概率
        res = self.calculate_pro(node_list,self.var_list)
        return res

    #计算条件概率
    def condition_probability(self,query,condition):
        #将条件概率利用链式法则扩展
        #首先计算分母的全概率
        t2 = self.joint_probability(condition)
        #下面更新分子的变量集合以及各个变量的特定取值
        new_query = {}
        for q in query:
            new_query[q] = query[q]
        for c in condition:
            new_query[c] = condition[c]
        t1 = self.joint_probability(new_query)
        #将分子与分母相除得出条件概率
        return t1 / t2

    #计算联合概率
    def joint_probability(self,query):
        domain = [] 
        #给每个变量赋予取值的范围，用二维列表表示
        for i in range(self.variable_num):
            #对于已知变量，取特定值
            if self.var_list[i][0] in query:
                tmp = [query[self.var_list[i][0]]]
                domain.append(tmp)
                continue
            #未知变量则有所有取值可能
            else:
                domain.append([0,1])
        p = 0
        #循环遍历，求出在指定变量值的所有情况全概率相加
        for i in domain[0]:
            for j in domain[1]:
                for k in domain[2]:
                    for x in domain[3]:
                        for y in domain[4]:
                            p += self.probability([i,j,k,x,y])
        #p为所求的联合概率
        return p

#存储变量的结点
class Node():
    #存储变量名字、与该变量相关的变量名字集合
    def __init__(self,name,variable_list):
        self.name = name
        self.variable_list = variable_list
    #变量各种取值的概率
    def set_proba(self,proba):
        self.proba = proba


if __name__ == "__main__":
    bayes = Bayes()
    bayes.build_node()

    #第一个
    p1 = bayes.joint_probability({'J':1,'M':1})
    print('P(J,M): ', p1)

    #第二个
    p2 = bayes.joint_probability({'B':1,'E':1,'A':1,'J':1,'M':1})
    print('P(B,E,A,J,M): ',p2)

    #第三个
    p3 = bayes.condition_probability({'A':1},{'J':1,'M':1})
    print('P(A | J,~M): ',p3)

    #第四个
    p4 = bayes.condition_probability({'J':1,'M':0},{'B':0})
    print('P(J,~M | ~B): ',p4)

    # output = open('burglary_out.txt','w',encoding='utf-8')
    # p = [str(p1),'\n',str(p2),'\n',str(p3),'\n',str(p4)]
    # output.writelines(p)