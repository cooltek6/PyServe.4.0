# pyserve.4
# main.py

import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msg
from tkinter.messagebox import showerror
from tinydb import TinyDB, Query
import os
import subprocess
from datetime import datetime
import json
try:
	from reportlab.lib.pagesizes import letter
	from reportlab.pdfgen import canvas
except Exception:
	letter = None
	canvas = None

# create an instance of the db globally
db = TinyDB("db.json")

# create a printable version of the db for testing
def print_db():
	print(db.all())
print_db()

# create a printable service order form and populate it with custy info


# load app settings (optional)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_config_path = os.path.join(BASE_DIR, "config", "app_settings.json")
APP_SETTINGS = {}
if os.path.exists(_config_path):
    try:
        with open(_config_path, "r", encoding="utf-8") as _f:
            APP_SETTINGS = json.load(_f)
    except Exception:
        APP_SETTINGS = {}


class ServiceOrderForm:
	def __init__(self, custy_info, work_description, pdf_font_name: str | None = None, pdf_font_size: int | None = None, pdf_font_path: str | None = None):
		# use defaults from APP_SETTINGS when not provided
		if pdf_font_name is None:
			pdf_font_name = APP_SETTINGS.get("default_pdf_font_name", "Helvetica")
		if pdf_font_size is None:
			pdf_font_size = APP_SETTINGS.get("default_pdf_font_size", 10)
		"""Initialize the form.

		pdf_font_name/pdf_font_size/pdf_font_path control the font used when
		rendering the PDF. pdf_font_path may point to a .ttf file — if provided
		this will attempt to register it under pdf_font_name.
		"""
		self.custy_info = custy_info
		self.work_description = work_description
		# PDF font configuration — name should be a ReportLab-registered font name
		# or a base name like 'Courier', 'Helvetica', etc. If font_path is provided
		# and points to a TTF file, it will be registered under font_name.
		self.pdf_font_name = pdf_font_name
		self.pdf_font_size = pdf_font_size
		self.pdf_font_path = pdf_font_path

	# replaced print_form with PDF generation + print
	def _render_form_text(self) -> str:
		"""Return the plain-text representation of the service order."""
		return f"""
		Crossroads Technical Services
		Service Order Form
  
		-----------------------------------------------------
  
		Customer Name: 	{self.custy_info.get('name','')}
		Address: 		{self.custy_info.get('address','')}
		City: 			{self.custy_info.get('city','')}
		Zipcode: 		{self.custy_info.get('zipcode','')}
		Phone: 			{self.custy_info.get('phone','')}
		Email: 			{self.custy_info.get('email','')}
          
		-----------------------------------------------------
  
		Work Description: {self.work_description}


		_____________________________________________________

		Service Performed:



		_____________________________________________________

		Parts Used:
  



		______________________________________________________

		Notes:
  



		______________________________________________________
  

		Technician Signature: __________________   Date: _____________
  

		  Customer Signature: __________________   Date: _____________
		"""

	def save_as_pdf_and_print(self, printer_name: str | None = None, completed_dir: str | None = None) -> str:
		"""Render the service order to a PDF, save it into `completed_dir` (created if needed), and send to printer via lpr.

		Returns the path to the PDF file on success. Raises RuntimeError on failure.
		"""
		# lazy-check for reportlab
		if canvas is None or letter is None:
			raise RuntimeError("reportlab is required for PDF output — install with: pip install reportlab")

		# ensure completed directory
		if completed_dir is None:
			base_dir = os.path.dirname(os.path.abspath(__file__))
			completed_dir = os.path.join(base_dir, "completed")
		os.makedirs(completed_dir, exist_ok=True)

		# create a timestamped filename
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		name = (self.custy_info.get('name') or 'unknown').strip().replace(' ', '_')[:40]
		filename = f"service_order_{name}_{timestamp}.pdf"
		pdf_path = os.path.join(completed_dir, filename)

		# render PDF
		cnvs = canvas.Canvas(pdf_path, pagesize=letter)
		# If a TrueType font path is provided, register it under the desired name
		try:
			from reportlab.pdfbase import ttfonts
			from reportlab.pdfbase import pdfmetrics
		except Exception:
			ttfonts = None
			pdfmetrics = None

		if self.pdf_font_path and ttfonts and pdfmetrics:
			# register TTF under the requested font name
			try:
				font_obj = ttfonts.TTFont(self.pdf_font_name, self.pdf_font_path)
				pdfmetrics.registerFont(font_obj)
			except Exception:
				# fallback: ignore registration and rely on built-ins
				pass

		text = cnvs.beginText(40, 750)
		text.setFont(self.pdf_font_name, self.pdf_font_size)
		for line in self._render_form_text().splitlines():
			for chunk in [line[i:i+90] for i in range(0, len(line), 90)]:
				text.textLine(chunk)
		cnvs.drawText(text)
		cnvs.showPage()
		cnvs.save()

		# attempt to print using lpr
		cmd = ["lpr"]
		if printer_name:
			cmd += ["-P", printer_name]
		try:
			subprocess.run(cmd + [pdf_path], check=True)
		except FileNotFoundError:
			raise RuntimeError(f"lpr not found. PDF saved to: {pdf_path}")
		except subprocess.CalledProcessError as exc:
			raise RuntimeError(f"Printing failed: {exc}. PDF saved to: {pdf_path}") from exc

		return pdf_path


# create the new service order window
class NewOrder(tk.Toplevel):
	def __init__(self, container):
		super().__init__(container)
		self.title("PyServe.4.0")
		self.geometry("419x350")
		self.resizable(False, False)

		# create the banner and grid it
		self.lbl_banner = ttk.Label(
			self,
			text="New Work Order",
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
		self.new_order_frame = NewOrderFrame(self)
  
# create the new order frame
class NewOrderFrame(ttk.Frame):
	def __init__(self, container: ttk.Frame):
		super().__init__(container)

		# grid the frame inside the window
		self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
  
		# create labels, entries, labelframe, and submit button for order input and grid them
		self.lbl_order_custy = ttk.Label(self, text="Customer Name:")
		self.lbl_order_custy.grid(row=1, column=0, padx=5, pady=5, sticky='e')
		self.ent_order_custy = ttk.Entry(self)
		self.ent_order_custy.grid(row=1, column=1, padx=5, pady=5, sticky='e')
		self.lbf_order_description = ttk.LabelFrame(self, text="Work to be done:")
		self.lbf_order_description.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
		self.ent_order_description = tk.Entry(self.lbf_order_description, width=48)
		self.ent_order_description.grid(row=1, column=0, padx=5, pady=5, sticky='ewns')

		# using a tk button instead of a ttk because it is easier without using Style()
		self.btn_submit = tk.Button(
			self,
			width=10,
			text="Submit",
			bg="green",
			fg="white",
			command=self.submit_order)
		self.btn_submit.grid(row=3, column=1, padx=5, pady=5, sticky='e')
  
		self.btn_cancel = tk.Button(
			self,
			width=10,
			text="Cancel",
			bg="red",
			fg="white",
			command=self.master.destroy)
		self.btn_cancel.grid(row=3, column=2, padx=5, pady=5, sticky='e')
  
	# create the submit function
	def submit_order(self) -> None:
		custy_name = self.ent_order_custy.get()
		# create a query to check if the customer exists		
		customer = Query()
		if db.search(customer.name == custy_name):
			# if the customer exists, show a messagebox with their info
			custy_info = db.search(customer.name == custy_name)[0]
			info_message = f"Customer Found!\n\nName: {custy_info['name']}\nAddress: {custy_info['address']}\nCity: {custy_info['city']}\nZipcode: {custy_info['zipcode']}\nPhone: {custy_info['phone']}\nEmail: {custy_info['email']}"
			tk.messagebox.showinfo("Customer Found", info_message)
		else:
			# if the customer does not exist, show an error messagebox
			tk.messagebox.showerror("Error", "Customer not found")

		# determine font choice using APP_SETTINGS
		ubuntu_sans_candidates = APP_SETTINGS.get("ubuntu_font_candidates", [
			"/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf",
			"/usr/share/fonts/truetype/ubuntu/Ubuntu-Medium.ttf",
			"/usr/share/fonts/truetype/Ubuntu/Ubuntu-M.ttf",
			"/usr/share/fonts/truetype/Ubuntu/Ubuntu-Medium.ttf",
		])

		# prefer bundled font when configured
		bundled_font_path = None
		if APP_SETTINGS.get("prefer_bundled_fonts"):
			candidate = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", APP_SETTINGS.get("bundled_font_filename", "Ubuntu-M.ttf"))
			if os.path.exists(candidate):
				bundled_font_path = candidate

		ubuntu_font_path = None
		if not bundled_font_path:
			for p in ubuntu_sans_candidates:
				if os.path.exists(p):
					ubuntu_font_path = p
					break

		if bundled_font_path:
			self.sevice_order_form = ServiceOrderForm(custy_info, self.ent_order_description.get(), pdf_font_name="Ubuntu-M", pdf_font_size=APP_SETTINGS.get("default_pdf_font_size", 16), pdf_font_path=bundled_font_path)
		elif ubuntu_font_path:
			self.sevice_order_form = ServiceOrderForm(custy_info, self.ent_order_description.get(), pdf_font_name="Ubuntu-M", pdf_font_size=APP_SETTINGS.get("default_pdf_font_size", 16), pdf_font_path=ubuntu_font_path)
		else:
			# fallback to default from APP_SETTINGS
			self.sevice_order_form = ServiceOrderForm(custy_info, self.ent_order_description.get())
		try:
			pdf_path = self.sevice_order_form.save_as_pdf_and_print()
			tk.messagebox.showinfo("Printed", f"Service order saved and sent to printer:\n{pdf_path}")
		except Exception as exc:
			tk.messagebox.showerror("Print Error", str(exc))
		finally:
			self.master.destroy()
		     

# create the new customer window
class NewCustomer(tk.Toplevel):
	def __init__(self, container):
		super().__init__(container)
		self.title("PySeve.4.0")
		self.geometry("419x350")
		self.resizable(False, False)

		# create the banner and grid it
		self.lbl_banner = ttk.Label(
			self,
			text="New Customer",
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
		# using a tk button. easier without using Style() at this time  
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
		self.btn_custy = ttk.Button(	
            self, 
            width=15, 
            text="New Customer", 
            command=self.click_newcustomer)
		self.btn_custy.grid(row=1, column=0, padx=5, pady=5)
  
		self.btn_order = ttk.Button(
      		self, 
        	width=15, 
         	text="New Order", 
          	command=self.click_neworder)
		self.btn_order.grid(row=1, column=1, padx=5, pady=5)
  
		self.btn_cancel = tk.Button(
      		self, 
            width=15, 
            text="Cancel",
            bg="red",
            fg="white", 
            command=self.click_cancel)
		self.btn_cancel.grid(row=1, column=2, padx=5, pady=5)
  
		# grid the frame inside the main window
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
		self.title("PyServe.4.0")
		self.geometry("448x200")
		self.resizable(False, False)

		# create the banner and grid it
		self.lbl_banner = ttk.Label(
			self,
			text="Welcome to PyServe.4.0",
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


