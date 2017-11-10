from tkinter import *
from tkinter import ttk
from utils import initInstrument,openVisaResource
		
class InitFrame(ttk.Frame):

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
        self.gpib_add=StringVar(self)
        self.reset=IntVar(self)
        self.inst_name=StringVar(self)
        self.gpib_add.set(str(17))
        
        main_frame= ttk.Frame(self, borderwidth=2, relief=GROOVE, padding=5)
        main_frame.grid()
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
		
        self.add_name=ttk.Label(main_frame,text='GPIB Address:',padding=1)
        self.add_name.grid(row=0, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
  
        self.add_number=Entry(main_frame, textvariable=self.gpib_add, bg='white')
        self.add_number.grid(row=0, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
       
        self.reset_option = ttk.Checkbutton(main_frame, text="Reset?",variable=self.reset)
        self.reset_option.grid(row=1, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
		
        self.inst_nameL=ttk.Label(main_frame,text='Instrument:')
        self.inst_nameL.grid(row=2, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.inst_nameV=ttk.Label(main_frame,text=self.inst_name.get(),borderwidth=1,relief=SUNKEN,
                                  font=("Helvetica", 8))
        self.inst_nameV.grid(row=2, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
					   
        self.init_Button=ttk.Button(main_frame,text='Initialize',command=self.init_instrument)
        self.init_Button.grid(row=3, column=1, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
		
    def get_handle(self):
        return self.inst_handle
		
    def init_instrument(self):
        print ("Initializing Instrument.................")
        self.inst_handle=(openVisaResource(self.gpib_add.get()))
        self.inst_name.set(initInstrument(self.inst_handle,self.reset.get()))
        self.inst_nameV.config(text=self.inst_name.get().replace(',','\n'))
        self.parent.updateInstHandle(self.inst_handle)
        print ("Done")
     
		
		
