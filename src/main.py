# pyserve.4
# main.py

import tkinter as tk
#from tkinter import *
from tkinter import ttk
#import tkinter.messagebox as msg
#from tkinter.messagebox import showerror
#from tinydb import TinyDB, Query

class NewCustomer(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("New Customer")
        self.geometry("433x400")
        self.resizable(False, False)


class StartFrame(ttk.Frame):
    def __init__(self, container: ttk.Frame):
        super().__init__(container)
        # create the banner and grid it
        self.lbl_banner = ttk.Label(
            self,
            text="PyServe.4.0",
            background="dodgerblue",
            foreground="white",
            anchor="center",
        )
        self.lbl_banner.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=15,
            ipady=10,
            sticky="ew",
        )
        
        # create three buttons and grid them
        self.btn_custy = ttk.Button(self, width=15, text="New Customer", command=self.click_newcustomer)
        self.btn_custy.grid(row=1, column=0, padx=5, pady=5)
        self.btn_order = ttk.Button(self, width=15, text="New Order", command=self.click_neworder)
        self.btn_order.grid(row=1, column=1, padx=5, pady=5)
        self.btn_cancel = ttk.Button(self, width=15, text="Cancel", command=self.click_cancel)
        self.btn_cancel.grid(row=1, column=2, padx=5, pady=5)
        # grid the frame inside the window
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def click_newcustomer(self):
        new_customer_window = NewCustomer(self)
        new_customer_window.grab_set()

    def click_neworder(self):
        pass

    def click_cancel(self):
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyServe.4")
        self.geometry("433x200")
        self.resizable(False, False)

if __name__ == "__main__":
    main_window = App()
    StartFrame(main_window)
    main_window.mainloop()
