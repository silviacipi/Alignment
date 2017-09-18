import h5py
import cv2
import os
import ntpath
import struct
from array import array

#import __builtin__
from os import listdir
from os.path import isfile, join
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion
from scipy.signal.signaltools import wiener
import EllipseV12Angle
import math
import threading
import time
import barrellTest
from scipy import ndimage

threadLock = threading.Lock()
threads = []
#circlesProperties = np.zeros((1,2))
myIter=0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter,img,threshold,myIter,minSlice, maxSlice,angle):
        threading.Thread.__init__(self)
        self.angle=angle
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.img=img
        self.threshold=threshold
        self.minSlice=minSlice
        self.maxSlice=maxSlice
        #self.myIter=myIter
        #self.fileName=fileName
    def run(self):
        print "Starting " + self.name
#         # Get lock to synchronize threads
        p1,p2=imageAnalysis(self.img,self.threshold,myIter,self.minSlice,self.maxSlice)
        threadLock.acquire()
        writeToFile(p1,p2,self.angle)
         #print_time(self.name, self.counter, 3)
#         # Free lock to release next thread
        threadLock.release()

#this version is adapted for dark and flat field images and to have the right sign for the roll and pitch
def selectData(v, nxsfileName,dataFolder):
    if v==1:
        print 'you selected HDF5 file'
        findContour(v, nxsfileName,dataFolder)
    else:
        print 'you selected TIF file'
        findContour(v, nxsfileName,dataFolder)
        
def imageAnalysis(img,threshold,myIter,minSlice, maxSlice):
#### filtering
    print 'doing analysis'
    img=ndimage.median_filter(img, size=10)
    #img=wiener(img,mysize=9, noise=0.9)        
    height,width=img.shape
    blank_image = np.zeros((height,width,1), np.uint8)
    minVal, maxVal, minLoc, maxLoc= cv2.minMaxLoc(img)
    temp=img/maxVal*255
    blank_image=temp.astype(np.uint8)
    
    ret, thresh=cv2.threshold(blank_image,threshold,255,cv2.THRESH_BINARY)                     
    pippo=thresh.copy()
    #changed here
    if (minSlice>0 or maxSlice>0):
        pippo2=pippo[minSlice:maxSlice,:]
    else:
        pippo2=pippo
    #end of Change
    contours,hierarchy = cv2.findContours(pippo2, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    p1=-1
    p2=-1
    for ii in range(len(contours)):
        moments = cv2.moments(contours[ii])
           
        if not (moments['m00']==0):
            if ii==1:
                p1=moments['m10']/moments['m00']
                p2=moments['m01']/moments['m00']
                newrow = [[p1, p2]]
                print 'circle found ', p1,p2
                return p1,p2
                #break
                #return p1,p2
    return p1,p2
            
        
def writeToFile(p1,p2,angle):
    global myIter
    global circlesProperties
    try:
        if (p1==-1) or (p2==-1):
            print 'circle not found'
        else:
            newrow = [[p1, p2,angle]]
           # print 'myIter',myIter
            if myIter==0:
                circlesProperties=newrow
                myIter=1
            else:
                circlesProperties=np.vstack((circlesProperties,newrow))
    except:
        print 'unable to save the circles properties'
    return
            
def findContour(v, nxsfileName,dataFolder, nrDarkImg=0,nrFlatImg=0,threshold=100, xc=1280, yc=1080, kBest=0,minSlice=0, maxSlice=0):
    global circlesProperties
    global myIter
    tStart=time.time()
    circlesProperties=[]
    circlesProperties= np.arange(3)
    circlesProperties= circlesProperties.reshape(1,3)
    circlesProperties=np.zeros((1,3))
    print nxsfileName
    #print 'myIter', myIter
    temp=ntpath.basename(nxsfileName)
    fileForImage, file_extension = os.path.splitext(temp)
    print fileForImage, 'this is my name for the image'
    mypath=h5py.File(nxsfileName,'r') 
    pathTot2=''
    contLoop=True
    rotAngle='rotation_angle'
    print 'looking for "',rotAngle, '" in the tree...'
    contLoop, pathToData, pathTot2,temp3=myRec(mypath,contLoop,pathTot2,rotAngle)
    print 'this is the length', temp3[0]
    print temp3
    rangeLoop=temp3[0]-1-2*(nrDarkImg+nrFlatImg)
    dataAngle=[0]*(rangeLoop)
    ii=0
    for i in range(0,rangeLoop):
        print 'angle ',i
        dataAngle[i]= mypath[str(pathTot2)][i+nrDarkImg+nrFlatImg]
        print dataAngle[i]
    '''
    nameTemp=fileForImage+'Angle.txt'
    with file(nameTemp, 'w') as outfile:
        np.savetxt(outfile, dataAngle, fmt='%-7.4f')
    '''
    print 'this is the content',dataAngle
    print 'looking for "',dataFolder, '" in the tree...'
    pathTot=''
    contLoop=True
    contLoop, pathToData, pathTot,temp4=myRec(mypath,contLoop,pathTot,dataFolder)
    if len(temp4)==3:
        a=temp4[0]
        b=temp4[1]
        c=temp4[2]
        print 'shape ', a,b,c
        print a, ' images to analyse'
        
    #myIter=0;  
    #fileName='/home/xfz42935/Desktop/test3.txt'
    if not contLoop:
        print 'database "',dataFolder,'" found in  ', pathTot
        #data=mypath[str(pathTot)]
        #npdata=np.array(data)
        #if v==1:
        #    a,b,c=mypath[str(pathTot)].shape
        #else:
        #    a,b=mypath[str(pathTot)].shape
        print a, ' file images to analyse' 
       #circlesProperties = np.zeros((1,2))

        
        for i in range(a-1):
            print 'image ',i
            
            #temporary if statement to skip dark and flat field images
            #imgToSkip=nrDarkImg+nrFlatImg
            #print 'images to skip', imgToSkip
            if nrDarkImg>0 and nrFlatImg>0:
                if v==1:
                    data=mypath[str(pathTot)][i][:b][:c]
                    npdata=np.array(data)
                    # for HDF file
                    ###inizialising...
                    if i==0:
                        imgDark=np.zeros(shape=(b,c))
                        imgFlat=np.zeros(shape=(b,c))
                    ###DARK IMAGE---temporary comment
                    if i<(nrDarkImg):
                        print 'dark field...averaging'
                        imgDark=imgDark+npdata
                        
                        continue
                        ###FLAT FIELD IMAGE 
                    elif i>(nrDarkImg-1) and i<(nrFlatImg+nrDarkImg):
                        print 'flat field images...averaging'
                        imgFlat=imgFlat+npdata
                        continue
                    elif i<a-1-nrFlatImg-nrDarkImg:  
                        if i==nrDarkImg+nrFlatImg:
                            #print 'im here'
                            imgDark=imgDark/nrDarkImg
                            imgFlat=imgFlat/nrFlatImg    
                        img=npdata
                    else:
                        print 'skipping last images'
                        continue
                        #blank_image = np.zeros((b,c,1), np.uint8)
                else:
                    #For tif file
                    data=data=mypath[str(pathTot)][i][0]
                    npdata=np.array(data)
                    filename, file_extension = os.path.splitext(npdata)
                    ###added 220616
                    print 'here I am'
                    print os.path.dirname(npdata)
                    #end added 220616
                    if file_extension=='.tif':
                        try:
                            
                            if i==0:
                                imgDark=cv2.imread(npdata,cv2.IMREAD_UNCHANGED )
                            if i>0 and i<(nrDarkImg):
                                print 'dark image...averaging'
                                imgDark=imgDark+cv2.imread(npdata,cv2.IMREAD_UNCHANGED )
                                continue
                            if i==nrDarkImg:   
                                imgDark=imgDark/nrDarkImg
                                imgFlat=cv2.imread(npdata,cv2.IMREAD_UNCHANGED )
                                continue
                            if i>nrDarkImg and i<nrDarkImg+nrFlatImg:
                                print 'flat field...averaging'
                                imgFlat=imgFlat+cv2.imread(npdata,cv2.IMREAD_UNCHANGED )
                                if i==nrDarkImg+nrFlatImg-1:
                                    imgFlat=imgFlat/nrFlatImg-imgDark
                                continue
                            if i>nrDarkImg+nrFlatImg-1 and i< a-imgFlat-imgDark:
                               # print 'Im here inside'
                                img=cv2.imread(npdata,cv2.IMREAD_UNCHANGED )
                            if i>(a-1-nrDarkImg-nrFlatImg):
                                print 'skipping last images'
                                continue
                        except:
                            print 'image ',npdata
                            print 'image not found: check the path'
                            continue
                    else:
                        print 'tif image not found...looking for the next'
                        continue             
                img=(img-imgDark)/imgFlat
            else:
                if v==1:
                # for HDF file
                    data=mypath[str(pathTot)][i][:b][:c]
                    npdata=np.array(data)
                    img=npdata
                    blank_image = np.zeros((b,c,1), np.uint8)
                else:
                    #For tif file
                    data=data=mypath[str(pathTot)][i][0]
                    npdata=np.array(data)
                    filename, file_extension = os.path.splitext(npdata)
                    ###added 220616z
                    #print 'here I am'
                    #print os.path.dirname(npdata[i][0])
                    #print os.path.split(npdata[i][0])
                    #oldDir,oldFile=os.path.split(npdata[i][0])
                    #newDir='/home/xfz42935/Documents/Alignment/align_i12/56338/projections/'
                    #end added/home/xfz42935/Documents/Alignment/align_i12/56338/projections 220616
                    #newName=newDir+oldFile
                    #print newName
                    if file_extension=='.tif':
                        try:
                            #change
                            img=cv2.imread(npdata,cv2.IMREAD_UNCHANGED )
                            #img=cv2.imread(newName,cv2.IMREAD_UNCHANGED )
                            #end of change
                            height=np.size(img, 0)
                            width=np.size(img, 1)
                            blank_image = np.zeros((height,width,1), np.uint8)
                        except:
                            print 'image ',npdata
                            print 'image not found: check the path'
                            continue
                    else:
                        print 'tif image not found...looking for the next'
                        continue
                    
            ###to function
            thread = myThread(i, "Thread-1", i,img,threshold,myIter,minSlice,maxSlice,dataAngle[i-nrDarkImg-nrFlatImg])
            thread.start()
            threads.append(thread)
   
        for t in threads:
            t.join()
        print "Exiting Main Thread"
        print 'circle properties', circlesProperties
        #circlesProperties = np.loadtxt(fileName)a
        tEnd=time.time()
        if len(circlesProperties)>1:
            #correcting for barrel distortion
            #xc=1280.0
            #yc=1340
            #kBest=-3.464e-09
            xx,yy=barrellTest.barrell(circlesProperties[:,0], circlesProperties[:,1], xc, yc, kBest)
	    newCoo=np.vstack((xx, yy,circlesProperties[:,2])).T	    
	    '''
            nameTemp='/home/xfz42935/Documents/Alignment/'+fileForImage+'Corrected.txt'
            
            with file(nameTemp, 'w') as outfile:
                np.savetxt(outfile, newCoo, fmt='%-7.4f')
            nameTemp='/home/xfz42935/Documents/Alignment/'+fileForImage+'.txt'
            with file(nameTemp, 'w') as outfile:
                np.savetxt(outfile, circlesProperties, fmt='%-7.4f')
	    '''
            minX=min(newCoo[:,0])
            maxX=max(newCoo[:,0])
            maxAxis=3*(maxX-minX)/2
            y0, y1, y2, y3,y4,forceLinear=EllipseV12Angle.Ellipse(newCoo[:,0], newCoo[:,1],newCoo[:,2],fileForImage,maxAxis)
            
            ### adding here the linear bit:
            if forceLinear:
                xx=newCoo[:,0]
                yy=newCoo[:,1]
                m,b = np.polyfit(xx, yy, 1) 
                xCoo=xx
                yCoo=m*xx+b
                print 'ellipse fit failed. Linear fit'
                y0='line'
                y1=m
                y2=b
                y3=0
                y4=0
                Rz=math.degrees(math.atan(m))
                print 'rotation @z= ',Rz ,' degrees'
                fig4 = plt.figure(1)
                title='rotation @z= %.5f degrees' %(Rz)
                fig4.suptitle(title)
                plt.gca().invert_yaxis()
                ax2 = fig4.add_subplot(111)
                ax2.scatter(xx, yy)
                plt.xlabel('pixel')
                plt.ylabel('pixel')
                plt.plot(xCoo,yCoo, color = 'red')
                plt.show()
            ###ending here the linear bit
        else:
            print 'No circles found in images: check loaded nxs'
        print 'END'
        myIter=0
        #circlesProperties = []
    else:
        print 'database "', dataFolder,'" not found!'
    print 'time to calculate centres in s', tEnd-tStart
    return
      
def myRec(obj,continueLoop,pathTot,dataFolder):  
    ### recursive function to look for the data database
    temp=None
    temp2=None
    temp5=None
    a=0
    b=0
    c=0
    i=1
    tempPath=''
    for name, value in obj.items():
        if continueLoop:
            #check if the object is a group
            if isinstance(obj[name], h5py.Group):
                tempPath='/'+name
                print tempPath
                if len(obj[name])>0:
                    continueLoop,temp,tempPath,temp2= myRec(obj[name],continueLoop,tempPath,dataFolder)
                else:
                    continue
            else:
                test=obj[name]
                print test
                temp1='/'+dataFolder
                print test.name
                if temp1 in test.name:
                    continueLoop=False
                    tempPath=pathTot+'/'+name
                    temp2=obj[name].shape
                    print obj[name].shape, len(temp2)
                    '''for item in obj[name].attrs.keys():
                        print item + ":", obj[name].attrs[item]
                        a,b,c=obj[name].shape 
                        print 'shape ', a,b,c
                        print a, ' images to analyse' '''
                    #print 'dimensions', obj[name].attrs['size']
                    return continueLoop,test.name,tempPath ,temp2
            i=i+1
        if (i-1)>len(obj.items()):
            tempPath=''
    pathTot=pathTot+tempPath
    return continueLoop,temp, pathTot, temp2
    
   
#########For testing function
#pathToNexus='C:\\Users\\xfz42935\\Documents\\Alignement\\64764.nxs'
#name='C:\\Users\\xfz42935\\Documents\\Alignement\\pco1-63429.hdf'
#findContour(pathToNexus,'data')
