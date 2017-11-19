import os
import numpy as np
from mnist import MNIST
import random

np.random.seed(7642)
mndata = MNIST('data')
images, labels = mndata.load_training()
index = random.randrange(0, len(images))
# print(MNIST.display(images[2]))
# print images[1]

weights1 = 2*np.random.random((784, 256)) -1
bias1 = 2*np.random.random(256) - 1
weights2 = 2*np.random.random((256, 256)) -1
bias2 = 2*np.random.random(256) -1
weights3 = 2*np.random.random((256, 10)) -1
bias3 = 2 *np.random.random(10) -1
h1=None
h2=None
d1=None
d2=None
d3=None
# print weights1

def oneHot(label):
    labelVector = [0]*10
    labelVector[label] = 1
    return labelVector

def getValidationData(value = 5000):
    imageList = []
    randomNo = np.random.choice(len(images), value, False)
    for random in randomNo:
        temp = images[random]
        for i in range(len(temp)):
            temp[i] = float(temp[i])/255
        imageList.append( (temp, oneHot(labels[random])) )
    return imageList

def getTrainingData(value = 30000):
    imageList = []
    randomNo = np.random.choice(len(images), value, False)
    for random in randomNo:
        temp = images[random]
        for i in range(len(temp)):
            temp[i] = float(temp[i])/255
        imageList.append( (temp, oneHot(labels[random])) )
    return imageList

def getTestData(value = 5000):
    imageList = []
    randomNo = np.random.choice(len(images), value, False)
    for random in randomNo:
        temp = images[random]
        for i in range(len(temp)):
            temp[i] = float(temp[i])/255
        imageList.append( (temp, oneHot(labels[random])) )
    return imageList

# print (getValidationData(1)[0][1])

def predictedOutput(input):
    z1 = np.dot(weights1.T, input) + bias1
    global h1
    h1 = 1/(1 + np.exp(-z1))    #sigmoid

    z2 = np.dot(weights2.T, h1) + bias2
    global h2
    h2 = 1/(1 + np.exp(-z2))   #sigmoid

    z3 = np.dot(weights3.T, h2) + bias3
    output = np.exp(z3) / np.sum(np.exp(z3))
    return output
    # print output

    # weight = weights1.T
    # lists = []
    # for row in weight[:1]:
    #     print len(row)
    #     sum = 0
    #     for i in range(len(row)):
    #         sum += row[i]*input[i]
    #     # print input
    #     h = np.dot(row,input)
    #     print h
    #     print sum
    #     lists.append(h)
    # # print (lists[0])

def getLoss(output, label):
    loss = -np.sum(label * np.log(output))
    return loss

def train (trainData):
    global i,weights1,weights2,weights3,eta,bias1,bias2,bias3,etadecay
    for data in trainData:
        i += 1
        label = data[1]
        image = data[0]
        output = predictedOutput(image)
        d1 = output - label
        dW3 = np.dot(h2.reshape((256,1)),d1.reshape((1,10)))
        dB3 = d1

        derv2 = h2 * (1-h2)
        #print derv2

        d2 = np.dot(d1.reshape((1,10)),weights3.T) * derv2

        dW2 = np.dot(h1.reshape((256,1)),d2)
        dB2 = d2.reshape(256)


        derv1 = h1 * (1-h1)
        d3 = np.dot(d2, weights2.T) * derv1

        x = np.asarray(image)

        dW1 = np.dot(x.reshape((784,1)),d3)
        dB1 = d3.reshape(256)
        #print dB1

        if i%5000 ==0:print ('Training sample %s , eta: %s and Loss : %s' %(i,eta,getLoss(output, label)))
        #print bias2
        if i%5000 == 0:
            if eta <= 0.005: etadecay = 0.0001
            eta -= etadecay
            if eta <=0.0001: eta = 0.0001

        weights3 -= eta * dW3
        weights2 -= eta * dW2
        weights1 -= eta * dW1
        bias3 -= eta * dB3
        bias2 -= eta * dB2
        bias1 -= eta * dB1

        #print bias2
    total=0
    correct=0
    global validData
    for testdata in validData:
        out = predictedOutput(testdata[0])
        predictMax = np.argmax(out)
        realMax = np.argmax(testdata[1])
        if predictMax == realMax:
            correct += 1
        total += 1
    accuracy = (float(correct)/total) * 100
    print 'accuracy: ', accuracy

def save(filename='model1.npz'):
    np.savez_compressed(
        file=os.path.join(os.curdir, 'models', filename),
        weights1=weights1,
        weights2=weights2,
        weights3=weights3,
        bias1=bias1,
        bias2=bias2,
        bias3=bias3,
        eta = eta,
        etadecay = etadecay
    )

def load():
    global weights1, weights2, weights3, eta, bias1, bias2, bias3,etadecay
    npz_members = np.load(os.path.join(os.curdir, 'models', 'model1.npz'))
    weights1 = np.asarray(npz_members['weights1'])
    weights2 = np.asarray(npz_members['weights2'])
    weights3 = np.asarray(npz_members['weights3'])
    bias1 = np.asarray(npz_members['bias1'])
    bias2 = np.asarray(npz_members['bias2'])
    bias3 = np.asarray(npz_members['bias3'])
    eta = float(npz_members['eta'])
    etadecay = float(npz_members['etadecay'])

trainData = getTrainingData()
validData = getValidationData()
testSet = getTestData()
i =0
eta = 0.1
etadecay = 0.005


# Set it to true to train or false to test
if True:
    # Uncomment the following line to load from previously trained weights
    #load()
    total = 0
    correct = 0
    # accuracy before training
    for testdata in validData:
        out = predictedOutput(testdata[0])
        predictMax = np.argmax(out)
        realMax = np.argmax(testdata[1])
        if predictMax == realMax:
            correct += 1
        total += 1
    accuracy = (float(correct) / total) * 100
    print 'accuracy before training: ', accuracy

    for j in range(10):
        np.random.shuffle(trainData)
        train(trainData)

    # Saving the trained weights and bias to models folder. Need to create it
    save()
else:
    load()
    total = 0
    correct = 0
    for testdata in testSet:
        out = predictedOutput(testdata[0])
        predictMax = np.argmax(out)
        realMax = np.argmax(testdata[1])
        if predictMax == realMax:
            correct += 1
        total += 1
    accuracy = (float(correct) / total) * 100
    print 'accuracy of test: ', accuracy



