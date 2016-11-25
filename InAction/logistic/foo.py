
def fGrad(x):
    return -2 * x  + 3

def calMax():
    x = 0.0
    step = 0.01
    loopCount = 1000
    for i in xrange(loopCount):
        x += step * fGrad(x)
    print x

def main():
    calMax()

if __name__ == '__main__':
    main()

