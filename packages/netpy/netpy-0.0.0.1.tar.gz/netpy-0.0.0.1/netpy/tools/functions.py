from scipy import exp, clip
import math as m
import numpy as np
import logging
import datetime
from .errors import mse_Error

def Exp(x):
    return exp(clip(x, -500, 500))

def sigmoid(x):
    return 1. /(1. +(Exp(-x)))

def sigmoid_der(x):
    return sigmoid(x)*(1-sigmoid(x))

def tanh(x):
    return (Exp(x)-Exp(-x))/(Exp(x)+Exp(-x))

def tanh_der(x):
    return 1 - (tanh(x)**2)

def SoftSign(x):
    return x / (1. + np.absolute(x))

def SoftSign_der(x):
    return 1. / (1. + np.absolute(x))

def SoftPlus(x):
    return np.log(1.0 + (Exp(x)))

def SoftPlus_der(x):
    return 1. /(1. + (Exp(x)))

def ReLU(x):
    return x * (x > 0)

def ReLU_der(x):
    return 1. * (x > 0)

def NormVector(x):
    res = 0

    for i in range(len(x)):
        res += x[i]**2

    return m.sqrt(res)

def NormMatrix(x):
    res = 0

    for i in range(len(x)):
        for j in range(len(x[0])):
            res += x[i][j]**2

    return m.sqrt(res)

def ScalarMultMatrix(x, y):

    res = 0

    for i in range(len(x)):
        for j in range(len(x[0])):
            res += x[i][j]*y[i][j]

    return res

def iq_test(net, X, Y):

    logging.basicConfig(filename=net.name+'_data/'+net.name+'.log', 
                       level=logging.INFO)

    output = []
    error = np.array([])

    for i in range(0, len(X)):
        output.append(net.forward(X[i], training=True))

    for i in range(0, len(X)):
        error = np.hstack((error, mse_Error(output[i], Y[i])))

    err_ = sum(error)/len(error)

    sigma = m.sqrt((sum((error - err_)** 2)/len(error)))
    err_max = err_ + 3*sigma
    
    if err_max > 1:
        err_max = 1

    err_min = err_ - 3*sigma

    if err_max < 0:
        err_max = 0

    iq_min = (1 - err_max)*100
    iq_max = (1 - err_min)*100
    iq = (iq_min + iq_max)/2

    net.iq_min = iq_min
    net.iq_max = iq_max
    net.iq = iq
    net.num_of_tests = len(X)

    net.save()

    logging.info("%s | iq_test | iq: %s | iq_min: %s | iq_max: %s" %
                 (datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"),
                  iq, iq_min, iq_max))

    return iq, iq_min, iq_max
    
