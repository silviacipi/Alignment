import numpy as np
from numpy.linalg import eig, inv
import math
from matplotlib import pyplot as plt
from numpy import double, size
from decimal import Decimal
from math import sqrt, tan, atan, sin
import scipy
from matplotlib.pyplot import ion
from scipy import stats


def barrell(xd,yd,xc,yc,k1):
    YY=(yd-yc)*(yd-yc)
    XX=(xd-xc)*(xd-xc)
    rd = [0 for x in range(len(XX))]
    ru = [0 for x in range(len(XX))]
    xu = [0 for x in range(len(XX))]
    yu = [0 for x in range(len(XX))]
    alpha = [0 for x in range(len(XX))]

    for i in range(len(XX)):

        rd[i]=sqrt(XX[i]+YY[i])
        alpha[i]=atan((yd[i]-yc)/(xd[i]-xc))
        signX=(xd[i]-xc)/abs((xd[i]-xc))
        signY=(yd[i]-yc)/abs((yd[i]-yc))
        ru[i]=rd[i]*(1+k1*rd[i]*rd[i])
        xu[i]=signX*ru[i]*abs(math.cos(alpha[i]))+xc
        yu[i]=signY*ru[i]*abs(math.sin(alpha[i]))+yc

    return xu, yu



if __name__ == "__main__":
    #fin = open('/home/xfz42935/Desktop/test.txt','r')
    #a = np.loadtxt('/home/xfz42935/Documents/Alignment/129.txt')
    a = np.loadtxt('/home/xfz42935/Documents/Alignment/75695.txt')
    print 'loaded ', a
    print len(a)
    #a=[]
    #for line in fin.readlines():
    #    a.append( [ x for x in line.split(' ') ] )
    #print a[:,0]
    #fileForImage='/home/xfz42935/Documents/Alignment/test2.png'
    xc=2000
    yc=1520
    k1Start=1e-9
    k1End=5e-9
    reg=0
    kBest=0
    steps=500
    k1=k1Start
#     stepSize=(k1End-k1Start)/steps
#     for i in range (steps):
#         k1=k1+stepSize*i
#         xx,yy=barrell(a[:,0], a[:,1], xc, yc, k1)
#         slope, intercept, r_value, p_value, std_err = stats.linregress(xx,yy)
#         print 'r_value', r_value
#         if (abs(r_value))>reg:
#             reg=abs(r_value)
#             kBest=k1
#     # kBest=-8e-9
#     print 'kBest', kBest
#     #print 'regBest', reg
    kBest=-4e-9
    xx,yy=barrell(a[:,0], a[:,1], xc, yc, kBest)
    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)
    ax1.scatter(a[:,0], a[:,1],color = 'red')
    ax1.scatter(xx, yy)
    plt.show()
    newCoo=np.vstack((xx, yy)).T
    print 'size',size(newCoo)
    nameTemp='/home/xfz42935/Documents/Alignment/'+str(75693)+'Corrected.txt'
    #with file(nameTemp, 'w') as outfile:
        #outfile.write('# Array shape: {0}\n'.format(newCoo.shape))
    #    np.savetxt(outfile, newCoo, fmt='%-7.4f')
    #print 'written'
    #Ellipse(a[:,0],a[:,1],fileForImage,maxAxis)