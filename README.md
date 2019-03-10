# Bayesian-Network


    手动实现贝叶斯网络构建推理，尝试使用pomegranate库进行贝叶斯网络构建推理。

    - 手动实现构建贝叶斯网络并进行推理求出联合概率和条件概率。
    - 调用pomegranate库构建贝叶斯网络并进行推理。
      - 推理时，使用几种方式求出条件概率。
      - 根据D分离判断条件独立性，从而省略求部分变量联合概率的步骤。
      - 利用链式法则将联合概率转化为求条件概率。


    调库实现文件：
      Three_gate.py  task1
      Burglary.py  task2
      Diagnosing.py  task3

      手动构建贝叶斯网络推理文件：
      My_Bayes.py   由于手动实现的代码函数结构对于三个task都一样，只是构建网络输入的参数不一样，因此不再重复。
