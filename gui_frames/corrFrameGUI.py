from tkinter import *
from utils import setCorrectionParameters
		
class CorrFrame(Frame):

    def __init__(self, master,inst_handle):
        ttk.Frame.__init__(self, master)
        self.relief = GROOVE
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.Widgets()
        self.inst_handle=inst_handle
		
    def Widgets(self):
    
        self.clb_len=IntVar(self)
        self.open_corr=IntVar(self)
        self.load_corr=IntVar(self)
        self.short_corr=IntVar(self)
        self.channel=IntVar(self)
        self.corr_Length=IntVar(self)
        
        self.open_corr.set(0)
        self.load_corr.set(0)
        self.short_corr.set(0)
        
        self.reset=StringVar(self)
        self.inst_name=StringVar(self)
        
        main_frame= ttk.Frame(self, borderwidth=2, relief=GROOVE, padding=5)
        main_frame.grid()
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
		
		
        self.corr_methodL=ttk.Label(main_frame,text='Corr Typ:',padding=1)
        self.corr_methodL.grid(row=0, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.corr_methodV= ttk.Combobox(main_frame, 
		values=["SING", "MULT"])
        self.corr_methodV.grid(row=0, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.corr_LengthL=ttk.Label(main_frame,text='Cbl Len:',padding=1)
        self.corr_LengthL.grid(row=1, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.corr_LengthV=Entry(main_frame, textvariable=self.corr_Length, bg='white')
        self.corr_LengthV.grid(row=1, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
		
        reset_frame= ttk.Frame(main_frame)
        reset_frame.grid(row=2, column=0, rowspan=1, columnspan=2,
                       sticky=W + E + N + S)
        reset_frame.grid_columnconfigure(0, weight=1)
        reset_frame.grid_rowconfigure(0, weight=1)
		
        self.open_option = ttk.Checkbutton(reset_frame, text="Open?",
        variable=self.open_corr)
        self.open_option.grid(row=0, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.short_option = ttk.Checkbutton(reset_frame, text="Short?",
        variable=self.short_corr)
        self.short_option.grid(row=0, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.load_option = ttk.Checkbutton(reset_frame, text="Load?",
        variable=self.load_corr)
        self.load_option.grid(row=0, column=2, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.corr_channelL=ttk.Label(main_frame,text='Channel:',padding=1)
        self.corr_channelL.grid(row=3, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.corr_channelV=Entry(main_frame, textvariable=self.channel, bg='white')
        self.corr_channelV.grid(row=3, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.load_typeL=ttk.Label(main_frame,text='Load Typ:',padding=1)
        self.load_typeL.grid(row=4, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.load_typeV= ttk.Combobox(main_frame, 
		values=["CPD","CPQ","CPG","CPRP","CSD","CSQ",
		"CSRS","LPQ","LPD","LPG","LPRP","LSD","LSQ","LSRS","RX",
		"ZTD","ZTR","GB","YTD","YTR"])
        self.load_typeV.grid(row=4, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)		
		
        			   
        self.corr_Button=ttk.Button(main_frame,text='Correct', command=self.runCorrections)
        self.corr_Button.grid(row=5, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
    
    def updateInstHandle(self,handle):
        self.inst_handle=handle
		
    def runCorrections(self):
        print ("Correction.........")
        setCorrectionParameters(self.inst_handle,
        self.corr_LengthV.get(),
        self.corr_methodV.get(),
        self.open_corr.get(),
        self.short_corr.get(),
        self.load_corr.get(),
        self.load_typeV.get(),
        self.channel.get()) 
        print ("Done")
		
       