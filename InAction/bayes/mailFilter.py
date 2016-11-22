import numpy as np

def textParse(bigString):
    import re
    wordsOfText = re.split('\W+', bigString)
    return [w.lower() for w in wordsOfText if len(w) > 2]

def createVocabList(docList):
    vocab = set()
    for doc in docList:
        vocab |= set(doc)
    return list(vocab)

def words2vec(vocab, doc):
    docVec = [0] * len(vocab)
    for word in doc:
        if word in vocab:
            docVec[vocab.index(word)] += 1
    return docVec

def trainNB(trainSet, trainClass):
    docNum = len(trainClass)
    wordNum = len(trainSet[0])
    pSpam = sum(trainClass) / float(docNum)
    wiOfC1 = np.ones(wordNum); wiOfC2 = np.ones(wordNum)
    wnOfC1 = 2.0; wnOfC2 = 2.0
    for i in xrange(docNum):
        if trainClass[i] == 1:
            wiOfC1 += trainSet[i]
            wnOfC1 += sum(trainSet[i])
        else:
            wiOfC2 += trainSet[i]
            wnOfC2 += sum(trainSet[i])
    p1 = wiOfC1 / wnOfC1; p2 = wiOfC2 / wnOfC2
    return p1, p2, pSpam

def classfyNB(inputVec, p1, p2, pSpam):
    pC1 = sum(np.log(p1) * inputVec) + np.log(pSpam)
    pC2 = sum(np.log(p2) * inputVec) + np.log(1 - pSpam)
    return pC1 > pC2 and 1 or 0


def main():
    import random
    # file2vocab
    docList = []; classList = []
    for i in xrange(1, 26):
        wordList = textParse(open('bayes/spam/%d.txt' % i, 'r').read())
        docList.append(wordList)
        classList.append(1)

        wordList = textParse(open('bayes/ham/%d.txt' % i, 'r').read())
        docList.append(wordList)
        classList.append(0)
    vocab = createVocabList(docList)
    # 10 randint for test
    # make a index copy for origin docList
    totalCount = 0
    for k in xrange(100):
        docMat = range(50); testMat = []; randList = []
        for i in xrange(10):
            randIndex = int(random.uniform(0, len(docMat)))
            randList.append(randIndex)
            testMat.append(words2vec(vocab, docList[randIndex]))
            del(docMat[randIndex])
        trainMat = []; trainClass = []
        for i in docMat:
            trainMat.append(words2vec(vocab, docList[i]))
            trainClass.append(classList[i])
        # go for classify
        # cal the error rate
        p1, p2, pSpam = trainNB(trainMat, trainClass)
        errorCount = 0
        for i, test in enumerate(testMat):
            out = classfyNB(test, p1, p2, pSpam)
            if out != classList[randList[i]]:
                errorCount += 1
        totalCount += errorCount
    print "average err: %.2f" % (float(totalCount) / (100 * 10))

if __name__ == '__main__':
    main()

