from tkinter import *
from utils import setSignalLevelAndFrequency,setImpedance,setIntegrationTime,runCVLoop
import numpy as np
		
class RunCVFrame(Frame):

    def __init__(self, master,inst_handle,app):
        ttk.Frame.__init__(self, master)
        self.relief = GROOVE
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.Widgets()
        self.inst_handle=inst_handle
        self.parent=app
        
    def Widgets(self):
        self.freq=DoubleVar(self)
        self.ac_volt=DoubleVar(self)
        self.dc_start=DoubleVar(self)
        self.dc_end=DoubleVar(self)
        self.dc_pts=DoubleVar(self)
        self.imp_rng=DoubleVar(self)
        self.int_pts=IntVar(self)
        self.aut_rng=IntVar(self)
        self.int_pts.set(8)
        self.filename=''
        
        
        main_frame= ttk.Frame(self, borderwidth=2, relief=GROOVE, padding=5)
        main_frame.grid()
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
		
        self.signal_freqL=ttk.Label(main_frame,text='Freq(Hz)',padding=1)
        self.signal_freqL.grid(row=0, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.signal_freqV=Entry(main_frame, textvariable=self.freq, bg='white')
        self.signal_freqV.grid(row=0, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.ac_voltageL=ttk.Label(main_frame,text='AC(V)',padding=1)
        self.ac_voltageL.grid(row=1, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.ac_voltageV=Entry(main_frame, textvariable=self.ac_volt, bg='white')
        self.ac_voltageV.grid(row=1, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)

        self.dc_startL=ttk.Label(main_frame,text='Start(V):',padding=1)
        self.dc_startL.grid(row=2, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.dc_startV=Entry(main_frame, textvariable=self.dc_start, bg='white')
        self.dc_startV.grid(row=2, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.dc_endL=ttk.Label(main_frame,text='End(V):',padding=1)
        self.dc_endL.grid(row=3, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.dc_endV=Entry(main_frame, textvariable=self.dc_end, bg='white')
        self.dc_endV.grid(row=3, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.ptsL=ttk.Label(main_frame,text='Pts(V)',padding=1)
        self.ptsL.grid(row=4, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.ptsV=Entry(main_frame, textvariable=self.dc_pts, bg='white')
        self.ptsV.grid(row=4, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.imp_rangeL=ttk.Label(main_frame,text='Imp Rng:',padding=1)
        self.imp_rangeL.grid(row=5, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.imp_rangeV=Entry(main_frame, textvariable=self.imp_rng, bg='white')
        self.imp_rangeV.grid(row=5, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.auto_range = ttk.Checkbutton(main_frame, text="Imp Auto Rng?",
        variable=self.aut_rng)
        self.auto_range.grid(row=6, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)	 		  
        
        self.load_typeL=ttk.Label(main_frame,text='Imp Type:',padding=1)
        self.load_typeL.grid(row=7, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        
        self.load_typeV= ttk.Combobox(main_frame, 
		values=["CPD","CPQ","CPG","CPRP","CSD","CSQ",
		"CSRS","LPQ","LPD","LPG","LPRP","LSD","LSQ","LSRS","RX",
		"ZTD","ZTR","GB","YTD","YTR"])
        self.load_typeV.grid(row=7, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.integ_timeL=ttk.Label(main_frame,text='Integ:',padding=1)
        self.integ_timeL.grid(row=8, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        
        self.integ_timeV= ttk.Combobox(main_frame, 
		values=["SHOR","MED","LONG"])
        self.integ_timeV.grid(row=8, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S) 

        self.integ_ptsL=ttk.Label(main_frame,text='Int pts:',padding=1)
        self.integ_ptsL.grid(row=9, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.integ_ptsV=Entry(main_frame, textvariable=self.int_pts, bg='white')
        self.integ_ptsV.grid(row=9, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)        
   
        self.run_Button=ttk.Button(main_frame,text='Run',command=self.runCVMeasurements)
        self.run_Button.grid(row=10, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
    def cb(self, event):
        print ("variable is", self.c.get())
        
    def updateInstHandle(self,handle):
        self.inst_handle=handle	
        
    def updateFileName(self,filename):
        self.filename=filename
        
    def runCVMeasurements(self):
        print ("setSignalLevelAndFrequency....")
        setSignalLevelAndFrequency(self.inst_handle,
                                self.freq.get(),
                                self.ac_volt.get(),
                                True,
                                False)
        print ("setImpedance....")
        setImpedance(self.inst_handle,
                    self.imp_rng.get(),
                    self.aut_rng.get(),
                    self.load_typeV.get())#Cp - G Mode
        print ("setIntegrationTime....")
        setIntegrationTime(self.inst_handle,
                            self.integ_timeV.get(),
                            self.int_pts.get())#Medium Integration Time - 8 Point Average
        print ("Run CV....")
        vBias = VBias = np.linspace(self.dc_start.get(),self.dc_end.get(),self.dc_pts.get()) #V
        runCVLoop(self.inst_handle,self.freq.get(),VBias,self.filename,self.parent)
        print('Done')