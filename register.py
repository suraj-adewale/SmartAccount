from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox, QPushButton,QLabel, QVBoxLayout, QGridLayout,QLineEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot,QDate,QDateTime
from cryptography.fernet import Fernet
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
import sys,json, sqlite3, uuid,base64,time


class ClickableLabel(QLabel):
	clicked=pyqtSignal()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton: self.clicked.emit()

class Register(QDialog):
	def __init__(self, parent=None):
		super(Register, self).__init__(parent)
		self.title = 'Register Smart Account'
		self.left = (self.x()+400)
		self.top = (self.x()+200)
		self.width =300
		self.height = 250
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.setWindowFlags(Qt.WindowMaximizeButtonHint)
		#self.setWindowModality(Qt.ApplicationModal)

		layout=QVBoxLayout()
		self.setLayout(layout)
		label1=QLabel("After you have activated your serial number online(Database renewal pluging), kindly enter the Registration Code that\nwas emailed to you into the box below.")
		layout.addWidget(label1)

		gridlayout=QGridLayout()
		gridlayout.setHorizontalSpacing(10)
		layout.addLayout(gridlayout)
		self.regcode=QLineEdit()
		self.regcode.textChanged.connect(self.TextChange)
		self.regcode.setPlaceholderText("e.g., 213921-XyhjjaAKLkazPoy ")
		gridlayout.addWidget(QLabel("Smart Accounts Registration Code (Database renewal pluging):"),0,0)
		gridlayout.addWidget(self.regcode,0,1)

		label1=QLabel("You can only use a Registration Code on one computer, unless you have purchased a site license.\n Attempting to use the same Registration Code on multiple computers might result\n in your code being blocked ")
		layout.addWidget(label1)

		label2=QLabel("<b>If you have not purchased yet</b>")
		layout.addWidget(label2)

		label3= ClickableLabel("To use all the features of this app, please use this link to buy with <br>online discount offers: <a href='http://www.sadeltech.com.ng/smartaccount/purchase'>Purchase Serial Number Online</a>")
		#label3.setOpenExternalLinks(True)
		label3.clicked.connect(self.OpenWeb)
		layout.addWidget(label3)

		buttngrid=QGridLayout()
		layout.addLayout(buttngrid)
		self.register=QPushButton("Register")
		self.cancel=QPushButton("Cancel")
		self.help=QPushButton("Help")

		buttngrid.addWidget(QLabel(""),0,1,1,3)
		buttngrid.addWidget(self.register,0,3)
		buttngrid.addWidget(self.cancel,0,4)
		buttngrid.addWidget(self.help,0,5)

		self.register.clicked.connect(self.Register)
		self.cancel.clicked.connect(self.close)
		self.cancel.setDisabled(True)
		self.register.setDisabled(True)

		

		'''
		mac=uuid.getnode()
		serialnumber=(str(year)[2:]+str(day)+str(mac)+str(month)).encode()
		key = Fernet.generate_key()
		json.dump(key.decode("utf-8"), open("db/key.json", "w"))
		f = Fernet(key)	
		encrypted = f.encrypt(serialnumber)
		json.dump(encrypted.decode("utf-8"), open("db/serialnumber.json", "w"))

		key=json.load(open("db/key.json", "r"))
		f = Fernet(key.encode())
		serialnumber=json.load(open("db/serialnumber.json", "r"))
		decrypted = f.decrypt(serialnumber.encode())	
		print(decrypted.decode("utf-8"))
		'''

	def TextChange(self,obj):
		if len(obj)>15:
			self.register.setEnabled(True)
		else:
			self.register.setDisabled(True)

	def OpenWeb(self):
		userdata=json.load(open("db/userdata.json", "r"))
		firstname=userdata[0]
		lastname=userdata[1]
		email=userdata[2]
		phone=userdata[5]

		mac=uuid.getnode()
		data={'id':str(mac),'email':email,'firstname':firstname,'lastname':lastname,'display_name': "Mobile Number",'variable_name': "mobile_number",
                'value': phone}

		#print(data)       
		data=json.dumps(data) 
		self.browser= QWebEngineView()
		self.browser.setWindowTitle('Loading payment...')
		self.channel=QWebChannel()
		self.channel.registerObject('backend', self)
		self.browser.page().setWebChannel(self.channel)
		#self.browser.setHtml('<p style="color:red;">ghcshhscgyu</p>')
		self.browser.load(QtCore.QUrl('http://www.sadeltech.com.ng/smartaccount?dat={}'.format(data)))
		self.browser.loadFinished.connect(self.onLoadFinished)
		self.browser.show()
	
	@pyqtSlot(str)
	def BackendFunction(self,data):
		self.data=eval(data)
		regcode=self.data[0]+self.data[1]+self.data[2]+self.data[3]
		regcode=(base64.encodestring(regcode.encode())).decode("utf-8")
		self.regcode.setText(str(regcode))
		self.Register()

	def onLoadFinished(self):
		self.browser.setWindowTitle('Payment')

	def Register(self):
		regcode=self.regcode.text()		
		date = QDate()
		currentdate=date.currentDate()
		year=currentdate.year()
		month=currentdate.month()
		day=currentdate.day()

		mac=uuid.getnode()
		serialnumber=str(self.data[0])+str(self.data[1])+str(self.data[2])+str(mac)
		encode=base64.encodestring(serialnumber.encode()).decode("utf-8")
		#print(encode)
		time.sleep(2)
		if regcode==encode:
			active=(str(self.data[2])+'-'+str(self.data[1])+'-'+str(self.data[0]))
			json.dump(active,open("db/activedate.json", "w"))
			QMessageBox.critical(self, 'Success', "\n  Transaction Successful. Best regards!  \n")
			self.browser.close()
			self.close()
		else:
			QMessageBox.critical(self, 'Key Error ', "\nThis serial number is not correct. Please try with different one\n\nBest regards!")	


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Register()
	ex.show()
	sys.exit(app.exec_())
