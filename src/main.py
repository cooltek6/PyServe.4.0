# pyserve.4
# main.py

import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msg
from tkinter.messagebox import showerror
from tinydb import TinyDB, Query

# create an instance of the db globally
db = TinyDB("db.json")

# create a printable version of the db for testing
def print_db():
	print(db.all())
print_db()

# create a printable service order form and populate it with custy info
class ServiceOrderForm:
	def __init__(self, custy_info):
		self.custy_info = custy_info

	# create a method to print the form
	def print_form(self):
		form = f"""
		Crossroads Technical Services
		Service Order Form
		-------------------
		Customer Name: {self.custy_info['name']}
		Address: {self.custy_info['address']}
		City: {self.custy_info['city']}
		Zipcode: {self.custy_info['zipcode']}
		Phone: {self.custy_info['phone']}
		Email: {self.custy_info['email']}
		-------------------
		Description of Work:
		
		______________________
		
		Service Performed:
  
  
  
		
		______________________
		
		Parts Used:
  
  
  
  
		
		______________________
		
		Notes:
  
  
  
  
		______________________

		Technician Signature: _____________   Date: _____________
  
		Customer Signature: _____________   Date: _____________
		"""
		print(form)


# create the new service order window
class NewOrder(tk.Toplevel):
	def __init__(self, container):
		super().__init__(container)
		self.title("New Customer")
		self.geometry("419x350")
		self.resizable(False, False)

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
			sticky="e",
		)
		self.new_order_frame = NewOrderFrame(self)
  
# create the new order frame
class NewOrderFrame(ttk.Frame):
	def __init__(self, container: ttk.Frame):
		super().__init__(container)
  
  		# grid the frame inside the window
		self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
  
		# create labels and entries and submit button for order input and grid them
		self.lbl_order_custy = ttk.Label(self, text="Customer Name:")
		self.lbl_order_custy.grid(row=1, column=0, padx=5, pady=5, sticky='e')
		self.ent_order_custy = ttk.Entry(self)
		self.ent_order_custy.grid(row=1, column=1, padx=5, pady=5, sticky='e')
		self.btn_submit = tk.Button(
			self,
			width=10,
			text="Submit",
			bg="green",
			fg="white",
			command=self.submit_order)
		self.btn_submit.grid(row=1, column=2, padx=5, pady=5, sticky='e')
  
	# create the submit function
	def submit_order(self):
		custy_name = self.ent_order_custy.get()
		# create a query to check if the customer exists		
		Customer = Query()
		if db.search(Customer.name == custy_name):
			# if the customer exists, show a messagebox with their info
			custy_info = db.search(Customer.name == custy_name)[0]
			info_message = f"Customer Found!\n\nName: {custy_info['name']}\nAddress: {custy_info['address']}\nCity: {custy_info['city']}\nZipcode: {custy_info['zipcode']}\nPhone: {custy_info['phone']}\nEmail: {custy_info['email']}"
			tk.messagebox.showinfo("Customer Found", info_message)
		else:
			tk.messagebox.showerror("Error", "Customer not found")
    
		self.sevice_order_form = ServiceOrderForm(custy_info)
		self.sevice_order_form.print_form()
		self.master.destroy()
		     

# create the new customer window
class NewCustomer(tk.Toplevel):
	def __init__(self, container):
		super().__init__(container)
		self.title("New Customer")
		self.geometry("419x350")
		self.resizable(False, False)

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
		self.new_custy_frame = NewCustyFrame(self)


# create the new customer frame
class NewCustyFrame(ttk.Frame):
	def __init__(self, container: ttk.Frame):
		super().__init__(container)
  
		# create six labels for input and grid them
		self.lbl_custy_name = ttk.Label(self, text="Customer Name:")
		self.lbl_custy_name.grid(row=1, column=0, padx=5, pady=5, sticky='e')
		self.lbl_custy_address = ttk.Label(self, text="Street Address:")
		self.lbl_custy_address.grid(row=2, column=0, padx=5, pady=5, sticky='e')
		self.lbl_custy_city = ttk.Label(self, text="City:")
		self.lbl_custy_city.grid(row=3, column=0, padx=5, pady=5, sticky='e')
		self.lbl_custy_zipcode = ttk.Label(self, text="Zip Code:")
		self.lbl_custy_zipcode.grid(row=4, column=0, padx=5, pady=5, sticky='e')
		self.lbl_custy_phone = ttk.Label(self, text="Phone Number:")
		self.lbl_custy_phone.grid(row=5, column=0, padx=5, pady=5, sticky='e')
		self.lbl_custy_email = ttk.Label(self, text="Email Address:")
		self.lbl_custy_email.grid(row=6, column=0, padx=5, pady=5, sticky='e')
  
		# create six entry widgets to go with each label and grid them
		self.ent_custy_name = ttk.Entry(self)
		self.ent_custy_name.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
		self.ent_custy_address = ttk.Entry(self)
		self.ent_custy_address.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
		self.ent_custy_city = ttk.Entry(self)
		self.ent_custy_city.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
		self.ent_custy_zipcode = ttk.Entry(self)
		self.ent_custy_zipcode.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
		self.ent_custy_phone = ttk.Entry(self)
		self.ent_custy_phone.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
		self.ent_custy_email = ttk.Entry(self)
		self.ent_custy_email.grid(row=6, column=1, padx=5, pady=5, sticky='ew')
  
		# create two buttons: cancel and submit and grid them
		# using a tk button instead of a ttk because it is easier without using Style()  
		self.btn_submit = tk.Button(
      		self, 
        	width=10, 
         	text="Submit", 
          	bg="green", 
           	fg="white", 
            command=self.submit)
		self.btn_submit.grid(row=2, column=2, padx=5, pady=5, sticky='ew')
  
		self.btn_cancel = tk.Button(
      		self, 
        	width=10, 
         	text="Cancel", 
          	bg="red", 
           	fg="white", 
            command=lambda: self.master.destroy())
		self.btn_cancel.grid(row=4, column=2, padx=5, pady=5, sticky='ew')

		# grid the frame inside the window
		self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

		# create a query to check if the customer already exists
	def submit(self):
		custy_name = self.ent_custy_name.get()
		custy_address = self.ent_custy_address.get()
		custy_city = self.ent_custy_city.get()
		custy_zipcode = self.ent_custy_zipcode.get()
		custy_phone = self.ent_custy_phone.get()
		custy_email = self.ent_custy_email.get()
		Customer = Query()
		if db.search(Customer.name == custy_name):
			tk.messagebox.showerror("Error", "Customer already exists!")
		else:
			db.insert({
				"name": custy_name,
				"address": custy_address,
				"city": custy_city,
				"zipcode": custy_zipcode,
				"phone": custy_phone,
				"email": custy_email
			})
			tk.messagebox.showinfo("Success", "Customer added successfully!")
			self.master.destroy()


class StartFrame(ttk.Frame):
	def __init__(self, container: ttk.Frame):
		super().__init__(container)

		# create three buttons and grid them
		self.btn_custy = ttk.Button(self, width=15, text="New Customer", command=self.click_newcustomer)
		self.btn_custy.grid(row=1, column=0, padx=5, pady=5)
		self.btn_order = ttk.Button(self, width=15, text="New Order", command=self.click_neworder)
		self.btn_order.grid(row=1, column=1, padx=5, pady=5)
		self.btn_cancel = ttk.Button(self, width=15, text="Cancel", command=self.click_cancel)
		self.btn_cancel.grid(row=1, column=2, padx=5, pady=5)
		# grid the frame inside the window
		self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

	def click_newcustomer(self):
		new_customer_window = NewCustomer(self)
		new_customer_window.grab_set()

	def click_neworder(self):
		new_order_window = NewOrder(self)
		new_order_window.grab_set()

	@staticmethod
	def click_cancel():
		main_window.destroy()


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("PyServe.4")
		self.geometry("433x200")
		self.resizable(False, False)

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


if __name__ == "__main__":
	main_window = App()
	StartFrame(main_window)
	main_window.mainloop()
