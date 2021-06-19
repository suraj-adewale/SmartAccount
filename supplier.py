from PyQt5.QtWidgets import QMainWindow,QTabWidget,QTextEdit,QCheckBox, QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency



class Suppliers(QMainWindow):
	def __init__(self, parent=None):
		super(Suppliers, self).__init__(parent)
		self.title = 'Supplier'
		self.left = (self.x()+400)
		self.top = (self.x()+150)
		self.width = 550
		self.height = 400
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		usertype_db=open("db/usertype.json", "r")
		usertype=json.load(usertype_db)
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			ipaddress=open("db/ipaddress.json", "r")
			self.ip=json.load(ipaddress)		
		
		self.AddSupplier()
		self.setCentralWidget(self.widget)

	def AddSupplier(self):
	
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.tabs = QTabWidget()
		self.mainlayout.addWidget(self.tabs)
		#self.tabs.currentChanged.connect(self.currentTab)

		self.supplier = QWidget()
		self.layout=QFormLayout()
		self.layout.setHorizontalSpacing(150)
		self.supplier.setLayout(self.layout)
		self.supplier.setStatusTip("Enter supplier information")
			
		self.tabs.addTab(self.supplier,"Supplier")

		self.supplierName=QLineEdit()
		self.supplierName.setPlaceholderText("Sadel Tec, Inc")
		self.contactperson=QLineEdit()
		self.contactperson.setPlaceholderText("Ade Temi")
		self.firstname=QLineEdit()
		self.firstname.setPlaceholderText("Ade")
		self.memo=QTextEdit()
		self.memo.setPlaceholderText("Enter address here.")
		self.memo.setMaximumHeight(50)

		grid1= QGridLayout()
		self.phone=QLineEdit()
		self.phone.setPlaceholderText("+2347 055 224 987")
		callphone=QPushButton("    Call    ")
		grid1.addWidget(self.phone,0,0)
		grid1.addWidget(callphone,0,1)

		grid2= QGridLayout()
		self.phone_alternative=QLineEdit()
		self.phone_alternative.setPlaceholderText("+2347 038 334 897")
		callphone=QPushButton("    Call    ")
		grid2.addWidget(self.phone_alternative,0,0)
		grid2.addWidget(callphone,0,1)

		grid3= QGridLayout()
		self.email=QLineEdit()
		self.email.setPlaceholderText("ade.temi@sadetec.com")
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

		self.tax = QCheckBox("Set tax exempt for this supplier")


		self.layout.addRow(QLabel("Supplier name:"),self.supplierName)
		self.layout.addRow(QLabel("Contact person:"),self.contactperson)
		self.layout.addRow(QLabel("Contact first name:"),self.firstname)
		self.layout.addRow(QLabel("Address:"),self.memo)
		self.layout.addRow(QLabel("Phone (primary):"),grid1)
		self.layout.addRow(QLabel("Phone (alternative):"),grid2)
		self.layout.addRow(QLabel("Email:"),grid3)
		self.layout.addRow(self.tax)
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

	def Cancel(self):
		self.close()	

	def Save(self):
		name=self.supplierName.text()
		contact=self.contactperson.text()
		first=self.firstname.text()
		address=self.memo.toPlainText()
		phone1=self.phone.text()
		phone2=self.phone_alternative.text()
		email=self.email.text()
		info=self.info.text()
		spinbox=self.spinbox.value()
		
		postList=[]

		if name=="" or contact=="" or first=="" or phone1=="":
			QMessageBox.critical(self, 'Empty', "\n    The fields cannot be empty 		\n")
			return False

		postList.append(name)
		postList.append(contact)
		postList.append(first)
		postList.append(address)
		postList.append(phone1)
		postList.append(phone2)
		postList.append(email)
		postList.append(info)
		postList.append('')
		postList.append(spinbox)

		postList=json.dumps(postList)
		data = QtCore.QByteArray()
		data.append("action=addsupplier")
		data.append("supplier={}".format(postList))
		url = "http://{}:5000/addsupplier".format(self.ip)
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
	        json_ar = json.loads(str(bytes_string, 'utf-8'))
	        if json_ar['2']=='supplieradded':
	        	QMessageBox.critical(self, 'Databese Connection  ', "\n 	Supplier added	 \n")
	        	return False

	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', " 	\n {}	 \n 	".format(reply.errorString()))
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Suppliers()
	ex.show()
	sys.exit(app.exec_())
