from pomegranate import *

def main():
	burglary = DiscreteDistribution({1:0.001,0:0.999})
	earthquake = DiscreteDistribution({1:0.002,0:0.998})

	alarm = ConditionalProbabilityTable(
		[[1,1,1,0.95],
		 [1,1,0,0.05],
		 [1,0,1,0.94],
		 [1,0,0,0.06],
		 [0,1,1,0.29],
		 [0,1,0,0.71],
		 [0,0,1,0.001],
		 [0,0,0,0.999]	
		],[burglary,earthquake])

	johnCalls = ConditionalProbabilityTable(
		[[1,1,0.90],
		 [1,0,0.10],
		 [0,1,0.05],
		 [0,0,0.95]
		],[alarm])

	maryCalls = ConditionalProbabilityTable(
		[[1,1,0.70],
		 [1,0,0.30],
		 [0,1,0.01],
		 [0,0,0.99]
		],[alarm])

	a1 = State(burglary,name='burglary')
	a2 = State(earthquake,name='earthquake')
	a3 = State(alarm,name='alarm')
	a4 = State(johnCalls,name='johnCalls')
	a5 = State(maryCalls,name='maryCalls')

	bayes_model = BayesianNetwork('Burglary Problem')
	bayes_model.add_states(a1,a2,a3,a4,a5)

	bayes_model.add_transition(a1,a3)
	bayes_model.add_transition(a2,a3)
	bayes_model.add_transition(a3,a4)
	bayes_model.add_transition(a3,a5)

	bayes_model.bake()

	
	p1 = 0
	for i in range(2):
		for j in range(2):
			for k in range(2):
				p1 += bayes_model.probability([i,j,k,1,1])

	p2 = bayes_model.probability([1,1,1,1,1])

	# p3 = 0
	# for i in range(2):
	# 	for j in range(2):
	# 		p3 += bayes_model.probability([i,j,1,1,1])
	# p3 = p3 / p1

	p3 = bayes_model.predict_proba({'johnCalls':1,'maryCalls':1})[2].probability(1)

	t1 = 0.999
	p4 = 0
	for i in range(2):
		for j in range(2):
			p4 += bayes_model.probability([0,i,j,1,0])
	p4 = p4 / t1
	
	print('P(J,M): ', p1)
	print('P(B,E,A,J,M): ',p2)
	print('P(A | J,~M): ',p3)
	print('P(J,~M | ~B): ',p4)

	output = open('burglary_out.txt','w',encoding='utf-8')
	p = [str(p1),'\n',str(p2),'\n',str(p3),'\n',str(p4)]
	output.writelines(p)


if __name__ == "__main__":
	main()