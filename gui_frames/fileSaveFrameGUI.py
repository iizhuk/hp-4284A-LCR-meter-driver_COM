from tkinter import *
from tkinter import ttk
		
class FileSaveFrame(Frame):
     
    def __init__(self, master,filename,app):
        ttk.Frame.__init__(self, master)
        self.relief = GROOVE
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.parent=app
        self.filename=filename
        self.Widgets()
        
		
    def Widgets(self):
        self.file_name=StringVar(self)
        update_filename = self.register(self.update_filename)
            
        main_frame= ttk.Frame(self, borderwidth=0, relief=GROOVE)
        main_frame.grid()
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
		
        self.file_nameL=ttk.Label(main_frame,text='FileName/location')
        self.file_nameL.grid(row=0, column=0, rowspan=1, columnspan=1,
                       sticky=W + E + N + S)
        self.file_nameV=ttk.Entry(main_frame, textvariable=self.file_name, 
                                width=82, 
                                validate='focusout',
                                validatecommand=update_filename)
        self.file_nameV.grid(row=0, column=1, rowspan=1, columnspan=6,
                       sticky=W + E + N + S)
       
    def update_filename(self):
        self.filename=self.file_name.get()
        self.parent.updateFileName(self.filename)
        
    def get_fileName(self):
        return self.filename
