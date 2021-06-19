from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QGroupBox,QFormLayout, QPushButton,QLabel, QVBoxLayout, QGridLayout,QLineEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json, sqlite3


class Settings(QDialog):
	def __init__(self, parent=None):
		super(Settings, self).__init__(parent)
		self.title = 'Settings'
		self.left = (self.x()+500)
		self.top = (self.x()+200)
		self.width =400
		self.height = 100
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		layout=QVBoxLayout()
		groupbox1 = QGroupBox('Set IP Address')	
		layout.addWidget(groupbox1)
		self.setLayout(layout)
		formlayout1 = QFormLayout()	
		formlayout1.setHorizontalSpacing(5)
		groupbox1.setLayout(formlayout1)

		self.ip=QLineEdit()
		self.port=QLineEdit("Port: 5000")
		self.port.setDisabled(True)

		ipgrid=QGridLayout()
		ipgrid.setHorizontalSpacing(5)
		self.saveip=QPushButton('Save')
		ipgrid.addWidget(self.port,0,0,0,2)
		ipgrid.addWidget(self.saveip,0,2)

		self.saveip.clicked.connect(self.SaveIp)

		self.ip.setPlaceholderText("Set IP Address e.g 192.168.173.1 ")
		self.port.setMaximumWidth(100)
		self.ip.setMinimumWidth(200)
		formlayout1.addRow(self.ip,ipgrid)

		groupbox2 = QGroupBox('Change Password')	
		layout.addWidget(groupbox2)
		self.setLayout(layout)
		passwordgrid=QGridLayout()
		passwordgrid.setHorizontalSpacing(5)
		groupbox2.setLayout(passwordgrid)

		self.currentpass=QLineEdit()
		self.newpass=QLineEdit()

		self.currentpass.setPlaceholderText("Enter current Password")
		self.newpass.setPlaceholderText("Enter new Password")

		self.savepass=QPushButton('Save')
		passwordgrid.addWidget(self.currentpass,0,1)
		passwordgrid.addWidget(self.newpass,0,2)
		passwordgrid.addWidget(self.savepass,0,3)

		self.savepass.clicked.connect(self.SavePass)
		
		self.currentpass.setMaximumWidth(200)
		self.newpass.setMaximumWidth(200)
		
	def SaveIp(self):
		ip=self.ip.text()
		if ip=="":
			return False
		json.dump(ip, open("db/ipaddress.json", "w"))
		QMessageBox.about(self, 'Ip Address ', "\n  IP Address Changed to {}	\n\n  ".format(ip))
		print(ip)
	def SavePass(self):
		password=self.currentpass.text()
		if password=="":
			return False		
		conn = sqlite3.connect('db/admin.db')
		cursor=conn.cursor()
		cursor.execute('''SELECT count(*), loginid FROM login WHERE password=? ''',(password,))
		current_admin=cursor.fetchone()

		if current_admin[0]>0:	
			newpassword=self.newpass.text()
			if len(str(newpassword))<6:
				QMessageBox.about(self, 'Password', "\n 	Passwords too short 	\n   ")	
				return False
			cursor.execute('''UPDATE login SET password=? WHERE loginid=?''',(newpassword,current_admin[1]))
			conn.commit()
			QMessageBox.about(self, 'Change Password ', "\n 	Your password has been updated 	\n")

			if QMessageBox.Ok==1024:
			    	self.close()
		else:
			QMessageBox.about(self, 'Password', "\n 	Password did not match 	\n")	
			return False



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Settings()
	ex.show()
	sys.exit(app.exec_())
