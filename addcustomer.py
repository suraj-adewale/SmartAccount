from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QTabWidget,QTextEdit,QCheckBox, QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency


class AddCustomer(QWidget):
	
	def __init__(self,custm, parent=None):
		super(AddCustomer, self).__init__(parent)
		self.title = 'Add Customer'
		self.left = (self.x()+400)
		self.top = (self.x()+150)
		self.width = 550
		self.height = 400
		self.custm=custm
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		usertype_db=open("db/usertype.json", "r")
		usertype=json.load(usertype_db)
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			ipaddress=open("db/ipaddress.json", "r")
			self.ip=json.load(ipaddress)

		self.supplier_action='addcustomer'	
		self.customerid=''

		self.mainlayout=QVBoxLayout()
		self.setLayout(self.mainlayout)
		self.tabs = QTabWidget()
		self.mainlayout.addWidget(self.tabs)
		#self.tabs.currentChanged.connect(self.currentTab)

		self.Customer = QWidget()
		self.layout=QFormLayout()
		self.layout.setHorizontalSpacing(150)
		self.Customer.setLayout(self.layout)
		self.Customer.setStatusTip("Enter Customer information")
			
		self.tabs.addTab(self.Customer,"Customer")

		self.customerName=QLineEdit()
		self.customerName.setPlaceholderText("Sadel Tec, Inc")
		self.contactperson=QLineEdit()
		self.contactperson.setPlaceholderText("Ade Temi")
		self.firstname=QLineEdit()
		self.firstname.setPlaceholderText("Ade")
		self.address=QTextEdit()
		self.address.setPlaceholderText("Enter address here.")
		self.address.setMaximumHeight(50)

		grid1= QGridLayout()
		self.phone1=QLineEdit()
		self.phone1.setPlaceholderText("+2347 055 224 987")
		callphone1=QPushButton("    Call    ")
		grid1.addWidget(self.phone1,0,0)
		grid1.addWidget(callphone1,0,1)

		grid2= QGridLayout()
		self.phone2=QLineEdit()
		self.phone2.setPlaceholderText("+2347 038 334 897")
		callphone2=QPushButton("    Call    ")
		grid2.addWidget(self.phone2,0,0)
		grid2.addWidget(callphone2,0,1)

		grid3= QGridLayout()
		self.email=QLineEdit()
		self.email.setPlaceholderText("ade.temi@sadeltec.com")
		mail=QPushButton("    Email    ")
		grid3.addWidget(self.email,0,0)
		grid3.addWidget(mail,0,1)

		self.info=QLineEdit()
		grid4= QGridLayout()
		self.term=QComboBox()
		self.term.addItems(["Pay in days","COD"])
		self.spinbox = QSpinBox()
		self.spinbox.setValue(30)

		grid4.addWidget(self.term,0,0)
		grid4.addWidget(self.spinbox,0,1)

		#self.tax = QCheckBox("Set tax exempt for this supplier")


		self.layout.addRow(QLabel("Customers name:"),self.customerName)
		self.layout.addRow(QLabel("Contact person:"),self.contactperson)
		self.layout.addRow(QLabel("Contact first name:"),self.firstname)
		self.layout.addRow(QLabel("Address:"),self.address)
		self.layout.addRow(QLabel("Phone (primary):"),grid1)
		self.layout.addRow(QLabel("Phone (alternative):"),grid2)
		self.layout.addRow(QLabel("Email:"),grid3)
		#self.layout.addRow(self.tax)
		self.layout.addRow(QLabel("Additional info:"),self.info)
		self.layout.addRow(QLabel("Payment terms: (if available)"),grid4)


		gridbutton=QGridLayout()
		self.ok=QPushButton('Ok')
		self.ok.clicked.connect(self.Save)
		self.cancel=QPushButton('Cancel')
		self.cancel.clicked.connect(self.Cancel)
		self.help=QPushButton('Help')
		gridbutton.addWidget(self.ok,0,0)
		gridbutton.addWidget(self.cancel,0,1)
		gridbutton.addWidget(self.help,0,2)

		buttonlayout=QFormLayout()
		buttonlayout.setHorizontalSpacing(200)
		buttonlayout.addRow(QLabel(),gridbutton)

		self.mainlayout.addLayout(buttonlayout)

		if self.custm.get('data',''):
			data=(self.custm.get('data',''))
			customerName=data[0]
			phone1=data[6]
			address=data[7]
			self.customerid=data[8]
			self.customerName.setText(str(customerName))
			self.phone1.setText(str(phone1))
			self.address.setText(str(address))
			self.supplier_action='editcustomer'

	def Cancel(self):
		self.close()
		if self.custm!='':
			self.custm=(self.custm.get('widget',''))
			requireddata=json.load(open("db/addinvoice.json", "r"))
			data=requireddata['customerdata']
			rows=len(data)
			self.custm.table.setRowCount(rows)
			self.custm.table.resizeRowsToContents()
			rw=0
			for row in sorted(data):
				key=row
				row=int(row)
				self.custm.table.setItem(rw,0, QTableWidgetItem(data[key][0]))
				self.custm.table.setItem(rw,1, QTableWidgetItem(format_currency(data[key][1],'NGN', locale='en_US')))
				self.custm.table.setItem(rw,2, QTableWidgetItem(data[key][2]))
				self.custm.table.setItem(rw,3, QTableWidgetItem(data[key][3]))
				self.custm.table.setItem(rw,4, QTableWidgetItem(data[key][4]))
				self.custm.table.setItem(rw,5, QTableWidgetItem(data[key][5]))
				self.custm.table.setItem(rw,6, QTableWidgetItem(data[key][6]))
				self.custm.keys[rw]=row
				rw+=1

	def Save(self):
		name=self.customerName.text()
		contact=self.contactperson.text()
		first=self.firstname.text()
		address=self.address.toPlainText()
		phone1=self.phone1.text()
		phone2=self.phone2.text()
		email=self.email.text()
		info=self.info.text()
		term=self.spinbox.value()

		if name=="":# or contact=="" or first=="" or phone1=="":
			QMessageBox.critical(self, 'Empty', "\n    The fields cannot be empty 		\n")
			return False
		
		postList=[]
		postList.append(name)
		postList.append(contact)
		postList.append(first)
		postList.append(address)
		postList.append(phone1)
		postList.append(phone2)
		postList.append(email)
		postList.append(info)
		postList.append(term)
		postList.append(self.customerid)
		postList=json.dumps(postList)
		data = QtCore.QByteArray()
		data.append("action={}&".format(self.supplier_action))
		data.append("customer={}".format(postList))
		url = "http://{}:5000/addcustomer".format(self.ip)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse)
		self.nam.post(req, data)

	def handleResponse(self, reply):
	    er = reply.error()
	    if er == QtNetwork.QNetworkReply.NoError:
	        bytes_string = reply.readAll()
	        customerdata= json.loads(str(bytes_string, 'utf-8'))
	       	requireddata=json.load(open("db/addinvoice.json", "r"))
        	requireddata['customerdata']=customerdata
        	json.dump(requireddata, open("db/addinvoice.json", "w"))
        	QMessageBox.critical(self, 'Databese Connection  ', "\nCustomer {} successfully    \n".format('edit' if self.supplier_action=='editcustomer' else 'added'))
        	return False
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "\n{}	 \n 	".format(reply.errorString()))	


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AddCustomer({})
	ex.show()
	sys.exit(app.exec_())
