from PyQt5.QtWidgets import QMainWindow, QSplashScreen,QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QProgressBar
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import pyqtSignal,Qt,pyqtSlot,QDate
import sqlite3,json
from datetime import datetime
from content import Main
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import PyQt5.sip

import os, sys,time,json


class App(QMainWindow):
	
	def __init__(self):
		
		super().__init__()		
		self.title = 'Login'
		self.left = 350
		self.top = 70
		self.width = 600
		self.height = 600

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		#self.showMaximized()
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)
		#self.setWindowModality(Qt.ApplicationModal)
				

		self.table_content = self.LoginContent()
		self.setCentralWidget(self.widget)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
	

	def LoginContent(self):	 
	
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.mainlayout.setSpacing(0)
		self.mainlayout.setContentsMargins(0, 0, 0, 0)

		scroll=QScrollArea()
		scroll.setWidgetResizable(True)
				
		minorlayout=QVBoxLayout()
		majorlayout=QVBoxLayout()

		scrollwidget=QWidget()
		scrollwidget.setLayout(majorlayout)
		scroll.setWidget(scrollwidget)

		self.mainlayout.addLayout(minorlayout,1)
		self.mainlayout.addWidget(scroll,8)
				
		titlelayout=QGridLayout()
		companylayout=QGridLayout()

		title=QLabel("SmartAccount")
		title.setObjectName('title')
		
		
		titlelayout.addWidget(title,0,0,)
		
		
		company=QLabel('v 2.0.1 © Sadel Technology')
		company.setObjectName('company')
		web=QLabel()
		web.setObjectName('web')
		web.setText("<a href='http://www.sadeltech.com.ng'>www.sadeltech.com.ng</a>")
		web.setOpenExternalLinks(True)
		
		
		companylayout.addWidget(company,0,0)
		companylayout.addWidget(web,0,1,1,8)
		
		
		minorlayout.addLayout(titlelayout,3)
		minorlayout.addLayout(companylayout,1)

		dashboard=QHBoxLayout()
		action=QHBoxLayout()
		action.setSpacing(20)

		majorlayout.addLayout(dashboard,1)
		majorlayout.addLayout(action,1)	

		labellayout=QVBoxLayout()

		dashboard.addWidget(QLabel(),1)
		dashboard.addLayout(labellayout,3)
		dashboard.addWidget(QLabel(),1.5)

		schoolimg=QLabel(self)
		pixmap=QPixmap('image/FCAA.JPG')
		schoolimg.setPixmap(pixmap)
		schoollabel=QLabel("FEDERAL COLLEGE OF AGRICULTURE, AKURE")

		schoolimg.setObjectName('schoolimg')
		schoollabel.setObjectName('schoollabel')

		labellayout.addWidget(schoollabel)
		labellayout.addWidget(schoolimg)
		

		logolayout=QVBoxLayout()
		actionlayout1=QVBoxLayout()
		#actionlayout1.setVerticalSpacing(10)
		#actionlayout1.setHorizontalSpacing(5)
		actionlayout2=QVBoxLayout()
		actionlayout2.setObjectName('actionlayout2')

		action.addLayout(logolayout,1)
		action.addLayout(actionlayout1,3)
		action.addLayout(actionlayout2,1.5)

		logolayout.addWidget(QLabel(''))
		self.LoginForm()
		actionlayout1.addLayout(self.formlayout)
		actionlayout2.addWidget(QLabel(''))

	def LoginForm(self):

		self.formlayout =QGridLayout()	
		self.formlayout.setVerticalSpacing(20)
		self.username=QLineEdit()
		self.Password=QLineEdit()
		self.submit=QPushButton("Sign In")
		self.Password.setEchoMode(QLineEdit.Password)
		self.username.setPlaceholderText('User Name, Email, Phone')
		self.Password.setPlaceholderText('********')

		self.signup=ClickableLabel()
		self.signup.setText("<a href='/none/'>Don't have account yet, click here to Sign Up</a>")
		self.signup.setObjectName('signup')

		self.forgotpass=ClickableLabel()
		self.forgotpass.setText("<a href='/none/'>Forgot Password?</a>")
		self.forgotpass.setObjectName('forgotpass')
		
		self.formlayout.addWidget(self.username,0,0,1,2)
		self.formlayout.addWidget(self.Password, 1,0,1,2)

		self.formlayout.addWidget(self.submit, 3,0,1,2)

		self.formlayout.addWidget(self.forgotpass, 4,0)
		self.formlayout.addWidget(self.signup, 4,1)

		self.formlayout.addWidget(QLabel(""),5,0)
		self.formlayout.addWidget(QLabel(""),6,0)
		self.formlayout.addWidget(QLabel(""),7,0)
		self.formlayout.addWidget(QLabel(""),8,0)

		self.username.setObjectName('signlineedit')
		self.Password.setObjectName('signlineedit')
		self.submit.setObjectName('signinbutton')
		self.signup.setObjectName('signuplabel')

		self.forgotpass.clicked.connect(self.ForgotPassword)
		self.signup.clicked.connect(self.SignUp)
		self.submit.clicked.connect(self.SignIn)

	def keyPressEvent(self, press):
		if press.key()==16777220:
			self.SignIn()

	def SignIn(self):
		try:
			usern=self.username.text()
			passw=self.Password.text()
			if usern=='' and passw=='':
				QMessageBox.about(self, 'Login', "   \nPlease enter your user name and password\n   ")
				return False
			if  passw=='':
				QMessageBox.about(self, 'Password ', "\nPlease enter your password\n   ")
				return False
			if usern=='':
				QMessageBox.about(self, 'User name ', "\nPlease enter your user name\n   ")
				return False
			
			self.conn = sqlite3.connect('db/admin.db')
			self.cursor=self.conn.cursor()
			self.cursor.execute('''SELECT count(*), firstname,lastname,email,usertype,loginid,phone FROM login WHERE\
			 password=? AND (username=? OR email=? OR phone=?)''',(passw,usern,usern,usern))
			self.current_admin=self.cursor.fetchone()
			
			if self.current_admin[0]>0:
				self.cursor.execute('''UPDATE login SET count=count+? WHERE loginid=? ''',(1,self.current_admin[5],))
				self.conn.commit()
							
				json.dump(self.current_admin[4], open("db/usertype.json", "w"))
				json.dump((self.current_admin[1]).upper() +' '+(self.current_admin[2]).upper(), open("db/user.json", "w"))
				json.dump([self.current_admin[1],self.current_admin[2],self.current_admin[3],self.current_admin[4],self.current_admin[5],self.current_admin[6]], open("db/userdata.json", "w"))
				
				
				self.content=Main((self.current_admin[3]),self.current_admin[4])
				self.content.show()
				self.username.setText('')
				self.Password.setText('')
				#self.close()

			
			else:
				QMessageBox.critical(self, 'Error Connection ', "	\nLogin error: incorrect login details\n   ")
		except Exception as e:
			QMessageBox.about(self, 'Connection', ' \n  Failed connection {}    \n'.format(e))


	def ForgotPassword(self):
		self.dialog=QDialog(self)
		layout=QVBoxLayout()
		groupbox = QGroupBox('Retrieve Password')
		layout.addWidget(groupbox)
		self.dialog.setLayout(layout)
		self.dialog.setWindowTitle("Password")
		self.retrievepass=QLineEdit()
		self.retrievepass.setPlaceholderText("Enter your email")
		layout1=QVBoxLayout()
		layout1.addWidget(self.retrievepass)
		groupbox.setLayout(layout1)

		grid=QGridLayout()
		self.passbtn=QPushButton('Send')
		self.cancelbutn=QPushButton('Cancel') 
		self.helpbutn=QPushButton('Help')

		grid.addWidget(self.passbtn,0,1)
		grid.addWidget(self.cancelbutn,0,2)
		grid.addWidget(self.helpbutn,0,3)
		layout.addLayout(grid)

		self.cancelbutn.clicked.connect(self.dialog.close)
		self.passbtn.clicked.connect(self.SendPassword)
		self.dialog.exec_()

	def SignUp(self):
		self.dialog=QDialog(self)
		layout=QVBoxLayout()
		groupbox = QGroupBox('Sign Up Form')
		layout.addWidget(groupbox)
		self.dialog.setLayout(layout)
		self.dialog.setWindowTitle("Sign Up")
		formlayout = QFormLayout()	
		formlayout.setHorizontalSpacing(50)
		groupbox.setLayout(formlayout)

		self.firstname=QLineEdit()
		self.firstname.setPlaceholderText('First Name')
		self.lastname=QLineEdit()
		self.lastname.setPlaceholderText('Last Name')
		self.usernam=QLineEdit('')
		self.usernam.setPlaceholderText('User Name')
		self.password=QLineEdit()
		self.password.setPlaceholderText('********')
		self.password.setEchoMode(QLineEdit.Password)
		self.confirm_password=QLineEdit()
		self.confirm_password.setPlaceholderText('********')
		self.confirm_password.setEchoMode(QLineEdit.Password)
		self.sexlayout=QGridLayout()
		self.sexlabel1=QRadioButton("Male")
		self.sexlabel2=QRadioButton("Female")
		self.sexlayout.addWidget(self.sexlabel1,0,0)
		self.sexlayout.addWidget(self.sexlabel2,0,1)

		self.usertype=QGridLayout()
		self.user=QRadioButton("User")
		self.admin=QRadioButton("Administrator")
		self.usertype.addWidget(self.user,0,0)
		self.usertype.addWidget(self.admin,0,1)
	
		self.phone=QLineEdit()
		self.phone.setPlaceholderText('+234704....')
		self.email=QLineEdit()
		self.email.setPlaceholderText('Email')
		self.email.setPlaceholderText('Email')
		
		buttongroup1=QButtonGroup()
		buttongroup1.addButton(self.user)
		buttongroup1.addButton(self.admin)

		buttongroup2=QButtonGroup()
		buttongroup2.addButton(self.sexlabel1)
		buttongroup2.addButton(self.sexlabel2)

		formlayout.setVerticalSpacing(15)
		formlayout.setHorizontalSpacing(100)
		formlayout.addRow(QLabel("First Name:"), self.firstname)
		formlayout.addRow(QLabel("Last Name:"), self.lastname)
		formlayout.addRow(QLabel("User Name:"), self.usernam)
		formlayout.addRow(QLabel("password:"), self.password)
		formlayout.addRow(QLabel("Confirm password:"), self.confirm_password)
		formlayout.addRow(QLabel("Gender:"), self.sexlayout)
		formlayout.addRow(QLabel("Administrator/User"), self.usertype)
		formlayout.addRow(QLabel("Email:"), self.email)
		formlayout.addRow(QLabel("Phone:"), self.phone)
		
		grid=QGridLayout()
		layout.addLayout(grid)
		self.signup=QPushButton('Sign Up')
		self.cancelbutn=QPushButton('Cancel') 
		self.helpbutn=QPushButton('Help')

		grid.addWidget(self.signup,0,1)
		grid.addWidget(self.cancelbutn,0,2)
		grid.addWidget(self.helpbutn,0,3)

		self.cancelbutn.clicked.connect(self.dialog.close)
		self.signup.clicked.connect(self.SubmitSignUp)
		self.dialog.exec_()
	
	def SubmitSignUp(self):
		try:
			firstn=self.firstname.text()
			lastn=self.lastname.text()
			usern=self.usernam.text()
			passw=self.password.text()
			confirm_passw=self.confirm_password.text()
			if (self.sexlabel1).isChecked()==True:
			 	sex=(self.sexlabel1).text() 
			if (self.sexlabel2).isChecked()==True:
			 	sex=(self.sexlabel2).text()
			if (self.user).isChecked()==True:
			 	usertype=(self.user).text() 
			if (self.admin).isChecked()==True:
			 	usertype=(self.admin).text() 	  	
			phone=self.phone.text()
			email=self.email.text()

			date = datetime(1,1,1).now()

			if len(str(passw))<6:
				QMessageBox.about(self, 'Password', "\nPassword too short 	 \n   ")	
				return False

			if firstn=='' or lastn=='' or phone=='' or email=='' or date=='' or usern=='' or passw=='':
				QMessageBox.about(self, 'Sign Up', "\nThe fields cannot be empty, Please enter all fields 	\n")
				return False
			
			if (self.sexlabel1).isChecked()==False and (self.sexlabel2).isChecked()==False:
				QMessageBox.about(self, 'Sign Up', "\nPlease select your gender 	 \n   ")
				return False
			
			if (self.user).isChecked()==False and (self.admin).isChecked()==False:
				QMessageBox.about(self, 'User Type', "\nPlease select user type 	 \n   ")	
				return False
			
			if passw!=confirm_passw:
				QMessageBox.about(self, 'Password', "\nPasswords not match 	 \n   ")	
				return False

			conn = sqlite3.connect('db/admin.db')
			cursor=conn.cursor()
			cursor.execute('''SELECT count(*), firstname,lastname,email FROM login WHERE\
		  			email=? OR username=? OR phone=? OR (firstname=? AND lastname=?)''',(email,usern,phone,firstn,lastn))
			current_admin=cursor.fetchone()
			conn.close()
			if current_admin[0]>0:	
				QMessageBox.about(self, 'Password', "\nUser already exists 	 \n")	
				return False	
				
			conn = sqlite3.connect('db/admin.db')
			cursor=conn.cursor()
			cursor.execute('''INSERT INTO login
								(firstname,
								lastname, 
								username,
								password,
								gender,
								usertype,
								phone,
								email,
								access,
								date_reg
								)\
							VALUES (?,?,?,?,?,?,?,?,?,?) ''',(firstn,lastn,usern,passw,sex,usertype,phone,email,1,date))
			conn.commit()
			conn.close()
			QMessageBox.about(self, 'Sign Up', '\nAcccount created for {} {} , you can now sign in\n'.format(firstn, lastn))
			#print(QMessageBox.Close,QMessageBox.Ok)
			
			if QMessageBox.Ok==1024:
				self.dialog.close()

		except Exception as e:
			QMessageBox.about(self, 'Connection', ' \nFailed connection {}    \n'.format(e))

	def SendPassword(self):
		Subject="Retrieve Password"
		fromaddr="sadeltechnology@gmail.com"
		email=self.retrievepass.text()
		conn = sqlite3.connect('db/admin.db')
		cursor=conn.cursor()
		cursor.execute('''SELECT count(*), firstname,lastname,email,password FROM login WHERE\
		  email=? ''',(email,))
		current_admin=cursor.fetchone()
		conn.close()
		if current_admin[0]>0:
			toaddr=current_admin[3]
			firstn=current_admin[1]
			lastn=current_admin[2]
			passw=current_admin[4]
			body="Dear {} {}, Please use the password given bellow to Sign In with SmartAccount\n\n {} \n Best regards! ".format(firstn,lastn,passw)

			try:
				server = smtplib.SMTP('smtp.gmail.com', 587)
				server.starttls()
				#print('Establish addressinfo')
			except Exception as e:
			    QMessageBox.critical(self, 'Email  ', "{}. No internet access	\n   ".format(e))
			    return False

			try:
			    server.login(fromaddr, "192111ade")
			    print('logged in..')
			    #self._popup.dismiss()
			    
			except Exception as e:
				QMessageBox.critical(self, 'Email  ', "{} \n   ".format(e))  
				print('logged not successful')  
				return False

			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['To'] = toaddr
			msg['Subject'] = Subject
			msg.attach(MIMEText(body, 'plain'))
			text = msg.as_string()
			try:        
			    server.sendmail(fromaddr, toaddr, text)
			    QMessageBox.critical(self, 'Email  ', "Your password has been sent to {}\nKindly check your email account to retrieve your password  ".format(toaddr))
			    
			    if QMessageBox.Ok==1024:
			    	self.dialog.close()
			    	server.quit()

			except Exception as e:
			    QMessageBox.critical(self, 'Email  ', "\n {} \n   ".format(e))
			    return False
		else:
			QMessageBox.critical(self, 'Email Error ', "\n You didn't register with this email address, try with different email  \n   ")
				    

class ClickableLabel(QLabel):
	clicked=pyqtSignal()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton: self.clicked.emit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	pixmap=QPixmap("image/accountsplash.jpg")
	splashscreen=QSplashScreen(pixmap,Qt.WindowStaysOnTopHint)
	splashscreen.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
	
	try:
		user=json.load(open("db/user.json", "r"))
	except Exception as e:
		user="Guest"
	splashscreen.showMessage("<h1><font color='green'>Welcome {}!</font></h1>".format(user), Qt.AlignTop | Qt.AlignCenter, Qt.black)
	#progresbar=QProgressBar(splashscreen)
	splashscreen.setMask(pixmap.mask())
	
	splashscreen.show()
	app.processEvents()
	
	'''for i in (0,100):
		progresbar.setValue(i)
		t=time.time()
		print(t)
		while time.time() < t+0.1:
			app.processEvents()
			time.sleep(2)'''

	time.sleep(2)

	date = QDate()
	currentdate=date.currentDate()
	year=currentdate.year()
	month=currentdate.month()
	day=currentdate.day()

	try:
		open("db/activedate.json")
		#json.dump('14-04-2019',open("db/activedate.json", "w"))
	except Exception as e:
		#print(e)
		active=(str(day)+'-'+str(month)+'-'+str(year))
		json.dump(active,open("db/activedate.json", "w"))	
	
	'''		
	import base64
	encode=base64.encodestring(b'122906229657')
	decode=base64.decodestring(encode).decode("utf-8")
	'''
	
	ex = App()
	ex.show()
	splashscreen.finish(ex)
	sys.exit(app.exec_())
