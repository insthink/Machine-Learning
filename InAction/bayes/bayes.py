# coding: UTF-8
import numpy as np

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabList(dataSet):
    vocab = set()
    for data in dataSet:
        vocab = vocab | set(data)
    return list(vocab)

def words2vec(vocabList, inputSet):
    wordVec = [0] * len(vocabList)
    common = list(set(vocabList) & set(inputSet))
    for w in common:
        i = vocabList.index(w)
        wordVec[i] = 1
    return wordVec


def trainNB(trainMat, trainCat):
    docNum = len(trainCat)
    wordNum = len(trainMat[0])
    pAbusive = sum(trainCat) / float(docNum)
    upper0, upper1 = np.ones(wordNum), np.ones(wordNum)
    down0, down1 = 2.0, 2.0
    for i in range(docNum):
        if trainCat[i] == 1:
            upper0 += trainMat[i]
            down0 += sum(trainMat[i])
        else:
            upper1 += trainMat[i]
            down1 += sum(trainMat[i])
    p0wi, p1wi = upper0 / down0, upper1 / down1
    return np.log(p0wi), np.log(p1wi), np.log(pAbusive)

def classifyNB(inputVec, p0Vec, p1Vec, pAb):
    p0 = sum(inputVec * p0Vec) + pAb
    p1 = sum(inputVec * p1Vec) + (1.0 - pAb)
    if p0 > p1: return 1
    else: return 0



# main function
def main():
    dataSet, classVec = loadDataSet()   # 获取原始数据集与手工分类结果
    vocablist = createVocabList(dataSet)    # 获得词汇表
    print vocablist
    trainMat = []
    for data in dataSet:
        trainMat.append(words2vec(vocablist, data)) # 得到训练用矩阵

    p0wi, p1wi, pAb = trainNB(trainMat, classVec)   # 每个单词的条件概率以及类别概率
    print pAb
    print p0wi
    print p1wi
    testArray1 = ["stupid", "garbage"]
    testArray2 = ["cute", "love"]
    inputArray1 = words2vec(vocablist, testArray1)
    inputArray2 = words2vec(vocablist, testArray2)
    print "array1: ", inputArray1
    print "array2: ", inputArray2
    print classifyNB(inputArray1, p0wi, p1wi, pAb)

if __name__ == '__main__':
    main()

