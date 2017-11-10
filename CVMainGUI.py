#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk

from gui_frames.initFrameGUI import InitFrame
from gui_frames.runCVFrameGUI import RunCVFrame
from gui_frames.fileSaveFrameGUI import FileSaveFrame
from gui_frames.pltDataFrameGUI import PltDataFrame
from gui_frames.corrFrameGUI import CorrFrame

root = Tk()

# Create and grid the outer content frame

mainFrame = ttk.Frame(root, padding=(10, 10, 10, 10))
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
mainFrame.master.title('HP 4284A - CV measurement')


class Application(ttk.Frame):

    def __init__(self, master=None,inst_handle=None,file_name=None):
        ttk.Frame.__init__(self, master)
        self.inst_handle=inst_handle
        self.file_name=file_name
        self.grid()
        self.mainWidgets()
        for r in range(14):
            self.master.rowconfigure(r, weight=1)
        for c in range(8):
            self.master.columnconfigure(c, weight=1)
        
		
    def mainWidgets(self):

        self.initFrame = InitFrame(master=mainFrame,inst_handle=self.inst_handle, app=self)
        self.initFrame.grid(row=0, column=0, rowspan=2, columnspan=2,
                       sticky=W + E + N + S)
        self.corrFrame = CorrFrame(master=mainFrame,inst_handle=self.inst_handle)
        self.corrFrame.grid(row=2, column=0, rowspan=3, columnspan=2,
                       sticky=W + E + N + S)
        self.runCVFrame = RunCVFrame(master=mainFrame,inst_handle=self.inst_handle,app=self)
        self.runCVFrame.grid(row=5, column=0, rowspan=9, columnspan=2,
                       sticky=W + E + N + S)
        self.fileSaveFrame = FileSaveFrame(master=mainFrame,filename=self.file_name, app=self)
        self.fileSaveFrame.grid(row=0, column=2, rowspan=1, columnspan=6,
                       sticky=W+N)
                     
        self.pltDataFrame = PltDataFrame(master=mainFrame)
        self.pltDataFrame.grid(row=1, column=2, rowspan=14, columnspan=6,
                      sticky= N)
                      
    def updateInstHandle(self,handle):
        self.inst_handle=handle
        self.corrFrame.updateInstHandle(handle)
        self.runCVFrame.updateInstHandle(handle)
        
    def updateFileName(self,filename):
        self.file_name=filename
        self.runCVFrame.updateFileName(filename)
    
    def updatePlot(self,V_data,Cp_data,Gp_data):
        self.pltDataFrame.updatePlot(V_data,Cp_data,Gp_data)
        
    
app = Application(master=mainFrame)
app.mainloop()