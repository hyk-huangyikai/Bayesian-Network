from pomegranate import *


def main():
	#构建离散分布，对于只涉及一个变量的单节点，只需要输入该变量的各个取值范围即可
	P = DiscreteDistribution({0:0.10,1:0.30,2:0.60})
	C = DiscreteDistribution({0:0.7,1:0.3})
	Mr = DiscreteDistribution({0:0.7,1:0.3})
	A = DiscreteDistribution({0:0.5,1:0.5})
	#对于变量S，是基于变量C和变量Mr得出的条件概率，因此需要建立条件概率表，将数据输入
	S = ConditionalProbabilityTable(
		[[0,0,0,0.8],
		 [0,1,0,0.5],
		 [1,0,0,0.5],
		 [1,1,0,0],

		 [0,0,1,0],
		 [0,1,1,0.4],
		 [1,0,1,0.4],
		 [1,1,1,0.9],

		 [0,0,2,0.2],
		 [0,1,2,0.1],
		 [1,0,2,0.1],
		 [1,1,2,0.1]
		],[C,Mr])

	Mo = ConditionalProbabilityTable(
		[[0,0,0,0.28],
		 [1,0,0,0.99],
		 [2,0,0,0.1],
		 [0,1,0,0.56],
		 [1,1,0,0.58],
		 [2,1,0,0.05],

		 [0,0,1,0.72],
		 [1,0,1,0.01],
		 [2,0,1,0.9],
		 [0,1,1,0.44],
		 [1,1,1,0.42],
		 [2,1,1,0.95]
		],[S,A])

	D = ConditionalProbabilityTable(
		[[0,0,0,0.80],
		 [1,0,0,0.70],
		 [2,0,0,0.9],
		 [0,1,0,0.60],
		 [1,1,0,0.50],
		 [2,1,0,0.4],
		 [0,2,0,0.30],
		 [1,2,0,0.20],
		 [2,2,0,0.1],

		 [0,0,1,0.1],
		 [1,0,1,0.2],
		 [2,0,1,0.05],
		 [0,1,1,0.3],
		 [1,1,1,0.4],
		 [2,1,1,0.3],
		 [0,2,1,0.4],
		 [1,2,1,0.2],
		 [2,2,1,0.1],

		 [0,0,2,0.1],
		 [1,0,2,0.1],
		 [2,0,2,0.05],
		 [0,1,2,0.1],
		 [1,1,2,0.1],
		 [2,1,2,0.3],
		 [0,2,2,0.3],
		 [1,2,2,0.6],
		 [2,2,2,0.8]
		],[S,P])

	#声明各个变量的结点，将其取值分布和变量名字作为参数传入
	a1 = State(P,name='P')
	a2 = State(C,name='C')
	a3 = State(Mr,name='Mr')
	a4 = State(S,name='S')
	a5 = State(A,name='A')
	a6 = State(Mo,name='Mo')
	a7 = State(D,name='D')

	#调用BayesianNetwork函数构建贝叶斯网络
	bayes_model = BayesianNetwork("Diagnosing Problem")
	#添加结点到贝叶斯网络中
	bayes_model.add_states(a1,a2,a3,a4,a5,a6,a7)

	#根据条件概率表，将各个变量的连接关系依次建立
	bayes_model.add_transition(a2,a4)
	bayes_model.add_transition(a3,a4)
	bayes_model.add_transition(a5,a6)
	bayes_model.add_transition(a4,a6)
	bayes_model.add_transition(a4,a7)
	bayes_model.add_transition(a1,a7)

	#运行贝叶斯网络
	bayes_model.bake()

	#两种方法求条件概率，一是扩展循环对联合概率求和的方式求出，
	#二是通过predict_proba求出基于已知变量值的剩余变量的取值概率即条件概率求出

	#将条件概率展开为分子/分母形式，分别求分子和分母的联合概率
	t1 = 0
	t2 = 0
	#求P、C、M的联合概率，将其进行扩展，进行循环遍历，将所有符合条件的全概率相加
	for i1 in range(2):
		for i2 in range(3):
			for i3 in range(2):
				for i4 in range(3):
					t1 += bayes_model.probability([0,0,i1,i2,i3,1,i4])
	#求变量P和C的联合概率，由于两者是条件独立的，因此可以直接相乘，避免展开求联合概率
	t2 = 0.10 * 0.70
	p1 = t1 / t2

	#下面方法同理
	t1 = 0
	t2 = 0
	for i1 in range(2):
		for i2 in range(3):
			for i3 in range(2):
				for i4 in range(2):
					t1 += bayes_model.probability([2,i1,0,i2,i3,i4,2])
	t2 = 0.6 * 0.7
	p2 = t1 / t2

	t1 = 0
	t2 = 0
	for i1 in range(2):
		for i2 in range(2):
			for i3 in range(3):
				t1 += bayes_model.probability([2,1,0,2,i1,i2,i3])
	t2 = 0.6 * 0.7 * 0.3
	p3 = t1 / t2

	t1 = 0
	t2 = 0
	for i1 in range(2):
		for i2 in range(2):
			for i3 in range(3):
				t1 += bayes_model.probability([0,i1,i2,2,0,0,i3])

	for i1 in range(2):
		for i2 in range(2):
			for i3 in range(2):
				for i4 in range(3):
					t2 += bayes_model.probability([0,i1,i2,2,0,i3,i4])
	p4 = t1 / t2

	p5 = bayes_model.probability([0,0,1,2,0,0,2])

	# print(p1)
	# print(p2)
	# print(p3)
	# print(p4)
	# print(p5)

	# print()

	#利用predict_proba可以得出已知变量条件下其他变量的各个取值概率，
	#其返回是一个列表，列表中的元素是离散分布，定位到指定的变量，
	#同时对其进行probability求解特定的值，即可得到对应的概率。
	pr1 = bayes_model.predict_proba({'P':0,'C':0})[5].probability(1)
	pr2 = bayes_model.predict_proba({'P':2,'Mr':0})[6].probability(2)
	pr3 = bayes_model.predict_proba({'P':2,'C':1,'Mr':0})[3].probability(2)
	pr4 = bayes_model.predict_proba({'P':0,'A':0,'S':2})[5].probability(0)
	pr5 = bayes_model.probability([0,0,1,2,0,0,2])

	print('Pr1: ',pr1)
	print('Pr2: ',pr2)
	print('Pr3: ',pr3)
	print('Pr4: ',pr4)
	print('Pr5: ',pr5)

	#将概率输出到指定的文件
	output = open('diagnosing_out.txt','w',encoding='utf-8')
	p = [str(pr1),'\n',str(pr2),'\n',str(pr3),'\n',str(pr4),'\n',str(pr5)]
	output.writelines(p)

if __name__ == "__main__":
	main()