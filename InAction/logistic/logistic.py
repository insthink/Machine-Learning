# -*- coding: UTF-8 -*-
import numpy as np
from matplotlib import pyplot as plt

def drawSigmod():
    plt.figure()
    plt.subplot(111)

    X = np.linspace(-60, 60, 256, endpoint=True)
    Y = 1 / (1 + np.exp(-X))

    plt.plot(X, Y)

    plt.ylim(Y.min() - 0.1, Y.max() * 1.1)

    plt.show()

def sigmod(inX):
    return 1.0 / (1 + np.exp(-inX))

def loadDataSet(path):
    # Set: X0 = 1.0
    dataSet = []; labelSet = []
    with open(path, 'r') as f:
        for line in f.xreadlines():
            lineArr = line.strip().split()
            dataSet.append([1.0, float(lineArr[0]), float(lineArr[1])])
            labelSet.append(float(lineArr[2]))
    return dataSet, labelSet

def gradDescend(trainMatIn, trainLabelIn):
    trainMat = np.mat(trainMatIn)
    trainLabel = np.mat(trainLabelIn).transpose()

    alpha = 0.001 # alpha为步长
    m, n = np.shape(trainMat) # m为样本数量,n为特征个数
    loopCount = 500 # 迭代次数
    theta = np.ones((n, 1)) # 初始化回归系数

    for i in xrange(loopCount):
        h = sigmod(trainMat * theta)
        error = h - trainLabel
        theta  -= alpha * trainMat.transpose() * error
    return theta

def randGradDescend(trainMatIn, trainLabelIn):
    import random

    trainMat = np.array(trainMatIn) # list转换为numpy.array
    trainLabel = np.array(trainLabelIn)

    alpha = 0.01 # 初始化步长
    m, n = np.shape(trainMat) # m个样本,n个特征
    theta = np.ones(n) # 初始化回归系数
    loopCount = 40 # 迭代次数

    for j in xrange(loopCount):
        for i in xrange(m):
            alpha += 4 / (1 + i + j)
            randIndex = int(random.uniform(0, m))
            h = sigmod(sum(theta * trainMat[randIndex]))
            error = h - trainLabel[randIndex]
            theta -= alpha * error * trainMat[randIndex]
    return theta


def main():
    data, label = loadDataSet("testSet.txt")
    theta = gradDescend(data, label)
    thetaRand = randGradDescend(data, label)
    dataArr = np.array(data)
    m, n = np.shape(dataArr)
    print m, n
    print len(label)
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in xrange(m):
        if label[i] == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=50, c='red')
    ax.scatter(xcord2, ycord2, s=50, c='blue')
    x = np.arange(-3.0, 3.0, 0.1)
    y1 = (- theta[0] - theta[1] * x) / theta[2]
    y2 = (- thetaRand[0] - thetaRand[1] * x) / thetaRand[2]
    ax.plot(x, y1, c='green')
    ax.plot(x, y2, c= 'green')
    plt.xlabel('x1'); plt.ylabel('x2')
    plt.show()



if __name__ == "__main__":
    main()
