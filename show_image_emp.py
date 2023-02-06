


from tkinter import *
from PIL import Image , ImageTk
import sqlite3
import io , os  
import threading

class Widgets(object):
	""" This is The Class Desgin For Application """

	def __init__(self,master):
		self.master = master
		self.user_name = StringVar()

		self.master.geometry("800x400+500+100")
		self.master.resizable(width=False,height=False)
		self.master.title('أستخراج صورة من قاعدة البيانات')
		self.master.option_add("*Font", 40)



		self.title_frame = Frame(self.master, width=740 , 
										height=270 ,background='#CFF0F5',
										padx=10,pady=3,
										relief=SUNKEN , bd=1).place(x=30,y=50)


		self.title_label = Label(self.title_frame,text='إدخل إسم المستخدم',
			font=("Libre Baskerville, serif;",20),background='#CFF0F5').place(x=580,y=70)


	
class MainApplication(threading.Thread,Widgets):
	""" This is The Class For Main Application """

	def __init__(self,root):
		threading.Thread.__init__(self)
		self.root = root
		self.class_widgets = Widgets(self.root)


		self.entry_user = Entry(self.root,
			width=27 ,font=('Bold Oblique',16) , relief=RAISED , bd=1,textvariable=self.class_widgets.user_name).place(x=240,y=75)



		self.button = Button(self.root,
			background='#E0DAF5' , width=9 , height=1 ,text='عرض الصورة',
			font=("Libre Baskerville, serif;",16),command=self.ConnectDataBase).place(x=350,y=120)



	def ConnectDataBase(self):
		try :
			self.main_path  = os.path.dirname(os.path.abspath(__file__))
			self.path_database = os.path.join(self.main_path, "DataBaseEmployees.db")

			if not os.path.exists(self.path_database):
				raise FileNotFoundError('File Nor Found Error')

			with sqlite3.connect(self.path_database) as self.connection :
				self.curosr = self.connection.cursor()
				self.curosr.execute('SELECT Image FROM Employees WHERE Name=?',(self.class_widgets.user_name.get(),))

				self.result = self.curosr.fetchone()
				if (self.result) == None:
					return("Not Found")
				self.show_image() 

		except Exception as error :
			print(error) 


	def show_image(self):
		with Image.open(io.BytesIO(self.result[0])) as self.image :
			self.image = self.image.resize((120,120))

			self.insert_image = ImageTk.PhotoImage(self.image)
			self.label_img = Label(self.root,image=self.insert_image,width=100,height=100)
			self.label_img.place(x=40,y=60)


if __name__=='__main__':
	app = Tk()
	class_widgets = MainApplication(app).start()
	app.mainloop()