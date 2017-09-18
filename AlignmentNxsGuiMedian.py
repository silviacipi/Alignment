import Tkinter
import tkFileDialog
from Tkinter import *
import tkMessageBox
import FindCirclesCenterContourMedian
class myGui_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent=parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        
        #text entry
        self.entryVariable=Tkinter.StringVar()
        self.entry=Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        
        #browse button
        buttonBrowse=Tkinter.Button(self,text='Browse Nexus file',command=self.OnBrowseClick)
        buttonBrowse.grid(column=1,row=0)  
        
        #hdf5 tif option selection
        T = Tkinter.Text(height=2, width=40)
        T.insert(END,"Select the type of file")
        T.grid(column=0,row=1,sticky='w')
        
        self.v = Tkinter.IntVar()
        buttonOption=Tkinter.Radiobutton(self, text='HFD5', variable=self.v,value=1, command=lambda: self.HDF5Message()).grid(column=0,row=2,sticky='w')
        buttonOption=Tkinter.Radiobutton(self, text='Tif', variable=self.v,value=2, command=lambda: self.HDF5Message()).grid(column=0,row=3,sticky='w')
        
        '''slice selection option 
        '''
        #T = Tkinter.Text(height=2, width=40)
        #T.insert(END,"reduced window")
        #T.grid(column=3,row=1,sticky='w')
        
        #self.v2 = Tkinter.IntVar()
        #self.v2.set(0)
        #buttonOption2=Tkinter.Radiobutton(self, text='ROI', command=lambda: self.ROIMessage()).grid(column=3,row=2,sticky='w')
        self.labelVariableROI=Tkinter.StringVar()
        label=Tkinter.Label(self,textvariable=self.labelVariableROI,anchor='w',fg='black',bg='grey')
        label.grid(column=3, row=3, columnspan=2,rowspan=2, sticky='EW')
        self.labelVariableROI.set('ROI: enter min and max slice number (default full image)')
                
        #slice number entry
        self.entryVariableDataROIMin=Tkinter.IntVar()
        self.entryDataROIMin=Tkinter.Entry(self,textvariable=self.entryVariableDataROIMin)
        self.entryDataROIMin.grid(column=4,row=5,sticky='EW')
        
        self.labelVariableMin=Tkinter.StringVar()
        label=Tkinter.Label(self,textvariable=self.labelVariableMin,anchor='w',fg='black',bg='grey')
        label.grid(column=3, row=5, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableMin.set('Min slice')
        
        self.entryVariableDataROIMax=Tkinter.IntVar()
        self.entryDataROIMax=Tkinter.Entry(self,textvariable=self.entryVariableDataROIMax)
        self.entryDataROIMax.grid(column=4,row=6,sticky='EW')
        
        self.labelVariableMax=Tkinter.StringVar()
        label=Tkinter.Label(self,textvariable=self.labelVariableMax,anchor='w',fg='black',bg='grey')
        label.grid(column=3, row=6, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableMax.set('Max slice')
        
         #label
        self.labelVariable=Tkinter.StringVar()
        label=Tkinter.Label(self,textvariable=self.labelVariable,anchor='w',fg='black',bg='grey')
        label.grid(column=0, row=4, columnspan=2,rowspan=2, sticky='EW')
        self.labelVariable.set('')
        
        #text entry
        self.entryVariableData=Tkinter.StringVar()
        self.entryData=Tkinter.Entry(self,textvariable=self.entryVariableData)
        self.entryData.grid(column=0,row=6,sticky='EW')
             
        #label Dark Image
        self.labelVariableDarkImage=Tkinter.StringVar()
        labelDarkImage=Tkinter.Label(self,textvariable=self.labelVariableDarkImage,anchor='w',fg='black',bg='grey')
        labelDarkImage.grid(column=0, row=7, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableDarkImage.set('Nr Dark Images')
        
        #Dark Image entry
        self.entryVariableDarkImage=Tkinter.IntVar()
        self.entryDarkImage=Tkinter.Entry(self,textvariable=self.entryVariableDarkImage)
        self.entryDarkImage.grid(column=0,row=8,sticky='EW')
        
        #Label Flat Field
        self.labelVariableFlatFieldImage=Tkinter.StringVar()
        labelFlatFieldImage=Tkinter.Label(self,textvariable=self.labelVariableFlatFieldImage,anchor='w',fg='black',bg='grey')
        labelFlatFieldImage.grid(column=1, row=7, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableFlatFieldImage.set('Nr Flat Field Images')

        
        #Flat Field Image entry
        self.entryVariableFlatFieldImage=Tkinter.IntVar()
        self.entryFlatFieldImage=Tkinter.Entry(self,textvariable=self.entryVariableFlatFieldImage)
        self.entryFlatFieldImage.grid(column=1,row=8,sticky='EW')
        
        #Label Image Threshold
        self.labelVariableThreshold=Tkinter.StringVar()
        labelThreshold=Tkinter.Label(self,textvariable=self.labelVariableThreshold,anchor='w',fg='black',bg='grey')
        labelThreshold.grid(column=2, row=7, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableThreshold.set('Threshold for binary image (0-255)')
        
        #Image Threshold  entry
        self.entryVariableThreshold=Tkinter.IntVar()
        self.entryThreshold=Tkinter.Entry(self,textvariable=self.entryVariableThreshold)
        self.entryThreshold.grid(column=2,row=8,sticky='EW')
        
        #Label Barrel Distortion
        self.labelVariableBarrel=Tkinter.StringVar()
        labelBarrel=Tkinter.Label(self,textvariable=self.labelVariableBarrel,anchor='w',fg='black',bg='grey')
        labelBarrel.grid(column=0, row=9, columnspan=2,rowspan=1, sticky='EW')
        self.labelVariableBarrel.set('Enter values for Barrel distortion')
        
        #Label Barrel Distortion Centre
        self.labelVariableBarrelCentreX=Tkinter.StringVar()
        labelBarrelCentreX=Tkinter.Label(self,textvariable=self.labelVariableBarrelCentreX,anchor='w',fg='black',bg='grey')
        labelBarrelCentreX.grid(column=0, row=10, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableBarrelCentreX.set('Centre X')
        self.labelVariableBarrelCentreY=Tkinter.StringVar()
        labelBarrelCentreY=Tkinter.Label(self,textvariable=self.labelVariableBarrelCentreY,anchor='w',fg='black',bg='grey')
        labelBarrelCentreY.grid(column=1, row=10, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableBarrelCentreY.set('Centre Y')
        #Label Barrel Distortion Parameter
        self.labelVariableBarrelParameter=Tkinter.StringVar()
        labelBarrelParameter=Tkinter.Label(self,textvariable=self.labelVariableBarrelParameter,anchor='w',fg='black',bg='grey')
        labelBarrelParameter.grid(column=2, row=10, columnspan=1,rowspan=1, sticky='EW')
        self.labelVariableBarrelParameter.set('Distortion Parameter')
        
        #Barrel Distortion Centre  entry
        self.entryVariableTBarrelCentreX=Tkinter.DoubleVar()
        self.entryBarrelCentreX=Tkinter.Entry(self,textvariable=self.entryVariableTBarrelCentreX)
        self.entryBarrelCentreX.grid(column=0,row=11,sticky='EW')
        
        self.entryVariableTBarrelCentreY=Tkinter.DoubleVar()
        self.entryBarrelCentreY=Tkinter.Entry(self,textvariable=self.entryVariableTBarrelCentreY)
        self.entryBarrelCentreY.grid(column=1,row=11,sticky='EW')
        
        #Barrel Distortion Parameter  entry
        self.entryVariableTBarrelParameter=Tkinter.DoubleVar()
        self.entryBarrelParameter=Tkinter.Entry(self,textvariable=self.entryVariableTBarrelParameter)
        self.entryBarrelParameter.grid(column=2,row=11,sticky='EW')
        
        
        self.entryVariable.set(' ')
        self.entryVariableData.set('')
        self.entryVariableDarkImage.set(0)
        self.entryVariableFlatFieldImage.set(0)     
        self.entryVariableThreshold.set(100) 
        self.entryVariableTBarrelParameter.set('0')#('-3.128e-9') 
        self.entryVariableTBarrelCentreY.set('1374.0') 
        self.entryVariableTBarrelCentreX.set('1329.0') 
        
        #button
        button=Tkinter.Button(self,text='Run Alignment',command=self.OnButtonClick)
        button.grid(column=1,row=13)
        
               
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def HDF5Message(self):
        if self.v.get()==1:
            print 'HDF5'
            self.labelVariable.set('Enter below the name of the Nexus tree entry containing the data.')
            self.entryVariableData.set('data')
        else:
            print 'TIF'
            self.labelVariable.set('Enter below the name of the Nexus tree entry containing the path to the folder.')
            self.entryVariableData.set('file_name')
            
    def ROIMessage(self):
        if self.v2.get()==0:
            self.v2.set(1)
            print 'Select ROI'
            #label
            
            
    def btnCallBack(self):
        v=self.v.get()
        var=self.entryVariable.get()
        dataFolder=self.entryVariableData.get()
        darkImg=self.entryVariableDarkImage.get()
        flatImg=self.entryVariableFlatFieldImage.get()
        threshold=self.entryVariableThreshold.get()
        xc=self.entryVariableTBarrelCentreX.get()
        yc=self.entryVariableTBarrelCentreY.get()
        kBest=self.entryVariableTBarrelParameter.get()
        minSlice=self.entryVariableDataROIMin.get()
        maxSlice=self.entryVariableDataROIMax.get()
        FindCirclesCenterContourMedian.findContour(v,var,dataFolder,darkImg,flatImg,threshold,xc,yc,kBest, minSlice, maxSlice)
    
    def OnBrowseClick(self):
        filename = tkFileDialog.askopenfilename(filetypes=(("NEXUS files", "*.nxs"),
                                           ("All files", "*.*") ))
        if len(filename ) > 0:
            print "You chose %s" % filename 
            self.entry.focus_set()
            self.entry.selection_range(0, Tkinter.END)
            self.entryVariable.set(filename)

    def OnButtonClick(self):
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        self.entryData.focus_set()
        self.entryData.selection_range(0, Tkinter.END)
        self.btnCallBack()
    '''    
    def hide_me(self):
        self.widget.pack_forget()
     '''   
if __name__ == "__main__":
    app=myGui_tk(None)
    app.title('my window')
    app.mainloop()
