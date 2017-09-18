import numpy as np
from numpy.linalg import eig, inv
import math
from matplotlib import pyplot as plt
from numpy import double
from decimal import Decimal

def fitEllipse(x,y):
    x = x[:,np.newaxis]
    x = np.array(x, np.float)
    y = y[:,np.newaxis]
    y = np.array(y, np.float)
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

def ellipse_center(a):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])


def ellipse_angle_of_rotation( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))


def ellipse_axis_length( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    try:
        down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
        down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
        res1=np.sqrt(up/down1)
        res2=np.sqrt(up/down2)
    except ZeroDivisionError as detail:
        print 'Handling run-time error:', detail
    return np.array([res1, res2])

def ellipse_angle_of_rotation2( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    if b == 0:
        if a > c:
            return 0
        else:
            return np.pi/2
    else:
        if a > c:
            return np.arctan(2*b/(a-c))/2
        else:
            return np.pi/2 + np.arctan(2*b/(a-c))/2
    
def Ellipse(xx,yy,angle,fileForImage,maxAxis):
    #plt.plot(xx,yy, color = 'red')
    #plt.show()
    print len(angle)
    a = fitEllipse(xx,yy)
    print 'this is a',a
    print len(xx),len(yy)
    #s=xx.shape
    y0=''
    y1=0
    y2=0
    y3=0
    y4=0
    #XX=xx
    #YY=yy
    spanningX=maxAxis
    forceLinear=0
    
    try:
        lenght=len(a)
    except:
        lenght=0
    if (lenght!=0):
        print 'calculating ellipse properties'
        center = ellipse_center(a)
        phi = ellipse_angle_of_rotation(a)
        axes = ellipse_axis_length(a)
    
    #check if the elliptical fit succeeded 
    # and if the axis size is reasonable, it may not be due to some problem of the 
    exit=0
    while (~exit):
        print 'exit', exit
        if lenght==0 or  (math.isnan(axes[0]*axes[1])) or isinstance(axes[0]*axes[1], complex):
            print 'Inside force linear'
            forceLinear=1
            exit=1
            return y0, y1, y2, y3, y4,forceLinear
        elif  (axes[0]>spanningX):
            print 'too large axis, try again'
            print axes[0],spanningX
            #trying to reduce the point over which to do the calculation
            #print 'Im here'
            skip=2
            if (len(xx)-skip)>(skip-1):
                xx=xx[skip-1:(len(xx)-skip)]
                yy=yy[skip-1:(len(yy)-skip)]
                y0, y1, y2, y3, y4,forceLinear=Ellipse(angle,xx,yy,fileForImage,maxAxis)
                exit=1
                return y0, y1, y2, y3, y4,forceLinear
            else:
                forceLinear=1
                exit=1
                return y0, y1, y2, y3, y4,forceLinear
        else:
            print 'ellipse fit succeeded'
            print("centre = ",  center)
            print("angle of rotation = ",  phi)
            print("axes = ", axes)
            '''
            Rz= rotation about z (roll)
            Rx rotation about x (pitch
            '''
            y0=''
            y1=0
            y2=0
            y3=0
            y4=0
            a, b = axes
            xCoo=np.zeros(360)
            yCoo=np.zeros(360)
            for i in xrange(0,360):
                R=math.radians(i)
                xCoo[i] = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
                yCoo[i] = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)
            Rz=math.degrees(phi) 
            '''
            #define if the pitch angle, Rx is positive or negative
            #I take some point in the middle and if y is larger than the y of the centre then the points are above
            '''
            for i in range(len(angle)):
                counter=0
                avgY=0
                if angle[i]>0 and angle[i]<90:
                    counter=counter+1
                    avgY=avgY+yy[i]
            if counter>0:
                avgY=avgY/counter
                print 'counter', counter
                print 'avgY',avgY
            else:
                print 'no angle between 0 and 90 degrees'
            '''
            index_min: index of the minimum angle
            '''    
            index_min = np.argmin(np.absolute(angle))
            '''
            if the average is higher, assuming it is rotating anticlockwise, the angle is negative
            , otherwise, positive. 
            '''
            if avgY> yy[index_min]:
                Rx=-math.degrees(math.atan(axes[1]/axes[0]))
            else:
                Rx=math.degrees(math.atan(axes[1]/axes[0]))
            '''
            pippo=len(yy)
            pippo=int(pippo/2)
            print pippo,yy[pippo]
            if yy[pippo]>center[1]:
                Rx=math.degrees(math.atan(axes[1]/axes[0]))
            else:
                Rx=-math.degrees(math.atan(axes[1]/axes[0]))
            '''  
            y0='ellipse'
            y1=a
            y2=b
            y3=Rz
            y4=Rx
            print '@z', Rz, ' degrees'
            print '@x', Rx,' degrees'
            fig4 = plt.figure(1)
            title='@z= %.5f degrees, @x= %.5f degrees' %(Rz, Rx)
            fig4.suptitle(title)
            plt.gca().invert_yaxis()
            ax2 = fig4.add_subplot(111)
            ax2.scatter(xx, yy)
            plt.xlabel('pixel')
            plt.ylabel('pixel')
            plt.plot(xCoo,yCoo, color = 'red')
            for i in range(len(angle)):
                ax2.annotate('%s' %angle[i], xy=(xx[i],yy[i]))#, xytext=(30,0), textcoords='offset points')
                print angle[i],xx[i],yy[i]
                #    ax2.annotate('(%s,' %angle[k], xy=(i,j))
                #ax2.annotate('(%s,' %i, xy=(i,j))
            plt.grid()
            plt.show()
            exit=1
            return y0, y1, y2, y3, y4,forceLinear
        #return exit
            #For saving images comment the line above and uncomment the line below
            #plt.savefig(fileForImage)
            #plt.close('all')
    print y0, y1, y2, y3, y4,forceLinear
    return y0, y1, y2, y3, y4,forceLinear


if __name__ == "__main__":
    #fin = open('/home/xfz42935/Desktop/test.txt','r')
    #a = np.loadtxt('/home/xfz42935/Documents/Alignment/75477Corrected.txt')
    a = np.loadtxt('/home/xfz42935/Documents/Alignment/78037Corrected.txt')
    b = np.loadtxt('/home/xfz42935/Documents/Alignment/78037Angle.txt')
    print a 
    print b
    #a=[]
    #for line in fin.readlines():
    #    a.append( [ x for x in line.split(' ') ] )
    #print a[:,0]
    fileForImage='/home/xfz42935/Documents/Alignment/test2.png'
    maxAxis=1200
    Ellipse(b,a[:,0],a[:,1],fileForImage,maxAxis)