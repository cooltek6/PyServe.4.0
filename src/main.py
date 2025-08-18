# pyserve.4
# main.py

#import tkinter as tk

from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msg
from tkinter.messagebox import showerror 
from tinydb import TinyDB, Query


class StartFrame(Frame):
  def __init__(self, container):
    super().__init__(container)
    

    # text vars for the buttons
    # self.var_custy = tk.StringVar()
    # self.var_custy.set("PyServe.4.0")
    
    # create the banner and grid it    
    self.lbl_banner = ttk.Label(self,
      text="PyServe.4.0",
      #bg='dodgerblue',
      foreground='white',
      pady=15)
    self.lbl_banner.grid(
      row=0,
      column=0,
      columnspan=3,
      sticky=(E,W))    


class App(Tk):
  def __init__(self):
    super().__init__()
    self.title('PyServe.4')
    self.geometry('350x200')
    self.resizable(False, False)
    
if __name__ == "__main__":
  app = App()
  StartFrame(app)
  app.mainloop()


