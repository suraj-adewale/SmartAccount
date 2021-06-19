from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from addinvoice import Invoice
from babel.numbers import format_currency


class InvoicePayable(QMainWindow):
	def __init__(self, parent=None):
		super(InvoicePayable, self).__init__(parent)
		self.title = 'Invoice'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		usertype_db=open("db/usertype.json", "r")
		usertype=json.load(usertype_db)
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			ipaddress=open("db/ipaddress.json", "r")
			self.ip=json.load(ipaddress)

		self.initmenu()

		self.InvoicePayableList()
		self.setCentralWidget(self.widget)

	def initmenu(self):
		#self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		Journal = mainMenu.addMenu('Invoice')
		homeMenu = mainMenu.addMenu('Report')
		homeMenu = mainMenu.addMenu('Help')
		 
		NewEntryButton = QAction(QIcon('exit24.png'), 'New Entry                    ', self)
		NewEntryButton.setShortcut('Ctrl+N')
		NewEntryButton.setStatusTip('New Journal')
		#NewEntryButton.triggered.connect(self.CreateNewAccount)

		Editbutton = QAction(QIcon('exit24.png'), 'Edit Entry', self)
		Editbutton.setDisabled(True)
		Editbutton.setShortcut('Enter')

		Deletebutton = QAction(QIcon('exit24.png'), 'Delete Entry', self)
		Deletebutton.setDisabled(True)
		Deletebutton.setShortcut('Cltl+Delete')

		Findbutton = QAction(QIcon('exit24.png'), 'Find Entry', self)
		Findbutton.setDisabled(True)
		Findbutton.setShortcut('Cltl+F')

		Findnextbutton = QAction(QIcon('exit24.png'), 'Find Next Entry', self)
		Findnextbutton.setDisabled(True)
		Findnextbutton.setShortcut('Cltl+N')
		
		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)

		self.statusBar()
		
		Journal.addAction(NewEntryButton)
		Journal.addAction(Editbutton)
		Journal.addAction(Deletebutton)
		Journal.addSeparator()
		Journal.addAction(Findbutton)
		Journal.addAction(Findnextbutton)
		Journal.addSeparator()
		Journal.addAction(exitButton)

		toolbar = self.addToolBar('tool bar')
		toolbar.setObjectName('toolbar')

		self.addinvoice= QAction(QIcon('image/icon/add.ico'), 'Add Invoice', self)
		self.edit= QAction(QIcon('image/icon/edit.ico'), 'Edit ', self)
		self.delete= QAction(QIcon('image/icon/delete.ico'), 'Delete ', self)
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail', self)
		self.payment= QAction(QIcon('image/icon/coins.png'), 'Payment', self)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		self.preview.setDisabled(True)
		self.print.setDisabled(True)
		self.save.setDisabled(True)
		self.mail.setDisabled(True)
		self.payment.setDisabled(True)
		
		toolbar.addAction(self.addinvoice)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()

		toolbar.addAction(self.preview)
		toolbar.addAction(self.print)
		toolbar.addAction(self.save)
		toolbar.addAction(self.payment)
		
		self.addinvoice.triggered.connect(self.CreateNewInvoice)
		self.edit.triggered.connect(self.Edit)
		self.delete.triggered.connect(self.Delete)
		self.preview.triggered.connect(self.Preview)
		self.print.triggered.connect(self.Print)
		self.save.triggered.connect(self.Save)
		self.mail.triggered.connect(self.Mail)
		self.payment.triggered.connect(self.Payment)	


	def CreateNewInvoice(self):
		self.addinvoice=Invoice({})
		self.addinvoice.show()	

	def Edit(self):
		self.delref=self.deljournal[self.delkey]
		self.EditInvoice(self.delref)

	def Delete(self):
		pass
	def Preview(self):
		pass	

	def Print(self):
		pass
	def Save(self):
		pass
	def Mail(self):
		pass
	def Payment(self):
		pass					
	def InvoicePayableList(self):
	
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.table =QTableWidget()
		self.mainlayout.addWidget(self.table)

		requireddata=open("db/invoicedata.json", "r")
		self.requireddata=json.load(requireddata)

		self.SupplierTable()
		self.AccountData()

	def SupplierTable(self):
		
		InvoicePayableHeader=["  Date","         Due Date        ","         Reference           ","          Invoice   ","          Customer   ","          Amount   ","          Due   ","          Status   "]
		self.table.setColumnCount(len(InvoicePayableHeader))     #Set three expense
		
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		header = self.table.horizontalHeader()
		for row in InvoicePayableHeader:
			header.setSectionResizeMode(InvoicePayableHeader.index(row), QtWidgets.QHeaderView.Stretch)
				
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(InvoicePayableHeader)	
		self.table.clicked.connect(self.TableAction)

	def AccountData(self):
		self.tabledata={}
		self.tabledata=self.requireddata
		rows=len(self.tabledata)
		self.table.setRowCount(rows)
		self.table.resizeRowsToContents()
		for row in sorted(self.tabledata):
			self.table.setItem(int(row),0, QTableWidgetItem(self.tabledata[row][0]))
			self.table.setItem(int(row),1, QTableWidgetItem(self.tabledata[row][1]))
			self.table.setItem(int(row),2, QTableWidgetItem(self.tabledata[row][2]))
			self.table.setItem(int(row),3, QTableWidgetItem(self.tabledata[row][3]))
			self.table.setItem(int(row),4, QTableWidgetItem(self.tabledata[row][4]))
			self.table.setItem(int(row),5, QTableWidgetItem(format_currency(self.tabledata[row][5],'NGN', locale='en_US')))
			if self.tabledata[row][6]==0.0:
				self.table.setItem(int(row),6, QTableWidgetItem(''))
			else:
				self.table.setItem(int(row),6, QTableWidgetItem(format_currency(self.tabledata[row][6],'NGN', locale='en_US')))
			self.table.setItem(int(row),7, QTableWidgetItem(self.tabledata[row][7]))
	
	def TableAction(self,item):
		if self.tabledata=={}:
			return False
		row=item.row()
		self.deljournal={}
		self.delkey= row
		
		#for row in self.table.selectionModel().selectedRows():
		if self.tabledata.get(str(row), '') is not '':
			self.deljournal[row]=self.tabledata[str(row)][2]
		#print(self.deljournal,self.delkey)
		self.edit.setEnabled(True)
		self.delete.setEnabled(True)
		self.preview.setEnabled(True)
		self.print.setEnabled(True)
		self.save.setEnabled(True)
		self.mail.setEnabled(True)
		self.payment.setEnabled(True)
	
	def EditInvoice(self,ref):
	
		data = QtCore.QByteArray()
		data.append("action=edit_invoices&")
		data.append("ref={}".format(ref))
		url = "http://{}:5000/invoices".format(self.ip)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse)
		
		#return False
		self.nam.post(req, data)

	def handleResponse(self, reply):
	    er = reply.error()
	    if er == QtNetwork.QNetworkReply.NoError:
	        bytes_string = reply.readAll()     
	        data = json.loads(str(bytes_string, 'utf-8'))
	        self.addinvoice=Invoice(data)
	        self.addinvoice.show()
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "\n {}	 \n".format(reply.errorString()))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = InvoicePayable()
	ex.show()
	sys.exit(app.exec_())
