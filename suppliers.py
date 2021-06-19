from PyQt5.QtWidgets import QMainWindow,QAction,QTableWidget,QDialogButtonBox,QDialog,QAbstractItemView, QApplication,QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from addsupplier import AddSupplier
from babel.numbers import format_currency
from functools import partial

class Suppliers(QMainWindow):
	def __init__(self,paywidget, parent=None):
		super(Suppliers, self).__init__(parent)
		self.title = 'Suppliers'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.paywidget=paywidget
		self.keys={}

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.SupplierList()
		self.setCentralWidget(self.widget)

		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		Journal = mainMenu.addMenu('Journal')
		homeMenu = mainMenu.addMenu('Report')
		homeMenu = mainMenu.addMenu('Help')
		 
		NewEntryButton = QAction(QIcon('exit24.png'), 'New Entry                    ', self)
		NewEntryButton.setShortcut('Ctrl+N')
		NewEntryButton.setStatusTip('New Journal')
		NewEntryButton.triggered.connect(self. AddNewSupplier)

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

		toolbar = self.addToolBar('Exit')
		toolbar.setObjectName('toolbar')

		self.addaccount= QAction(QIcon('image/icon/add.ico'), 'Add Account', self)
		self.edit= QAction(QIcon('image/icon/edit.ico'), 'Edit Account', self)
		self.delete= QAction(QIcon('image/icon/delete.ico'), 'Delete Account', self)

		toolbar.addAction(self.addaccount)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()
		
		self.addaccount.triggered.connect(self.AddNewSupplier)
		self.edit.triggered.connect(self.Edit)
		self.delete.triggered.connect(self.Delete)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)

	
	def Edit(self):

		self.suppl=AddSupplier({'widget':self,'data':self.del_editDic[self.delkey]})
		self.suppl.show()
		
	
	def Delete(self):
		self.dialog=QDialog(self)
		self.dialog.setWindowTitle("New Template")
		layout=QVBoxLayout()
		self.dialog.setLayout(layout)
		label=QLabel("\n Are you sure you want to delete selected Supplier {} at row {}\n\n".\
			format(self.del_editDic[self.delkey][0],self.delkey+1))
		
		layout.addWidget(label)
		buttonbox = QDialogButtonBox(QDialogButtonBox.Yes|QDialogButtonBox.No)
		layout.addWidget(buttonbox)

		buttonbox.accepted.connect(partial(self.DeleteNow,self.del_editDic[self.delkey][5]))
		buttonbox.rejected.connect(self.dialog.close)
		self.dialog.exec_()

	def DeleteNow(self,supplierid):
		self.ServerAction(supplierid)

	def AddNewSupplier(self):
		self.suppl=AddSupplier({'widget':self})
		self.suppl.show()	

	def SupplierList(self):
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.table =QTableWidget()
		self.mainlayout.addWidget(self.table)

		self.requireddata=json.load(open("db/suppliersdata.json", "r"))
		self.SupplierTable()
		self.SupplierData()

	def SupplierTable(self):
		JournalHeader=["  Supplier","         Account Payable        ","         Due date           ","          Phone   "]
		self.table.setColumnCount(4)     #Set three expense
		
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		header = self.table.horizontalHeader()
		
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(JournalHeader)	
		self.table.doubleClicked.connect(self.TableAction)

	def SupplierData(self):
		data=self.requireddata
		#print(data)
		rows=len(data)
		self.table.setRowCount(rows)
		self.table.resizeRowsToContents()
		rw=0
		for row in sorted(data):
			self.table.setItem(int(rw),0, QTableWidgetItem(data[row][0]))
			self.table.setItem(int(rw),1, QTableWidgetItem(format_currency(data[row][1],'NGN', locale='en_US')))
			self.table.setItem(int(rw),2, QTableWidgetItem(data[row][2]))
			self.table.setItem(int(rw),3, QTableWidgetItem(data[row][3]))
			self.keys[rw]=row
			rw+=1
	
	def TableAction(self,item):

		if self.requireddata=={}:
			return False
		row=item.row()
		self.delkey=row
		self.del_editDic={}
		
		if self.requireddata.get(str(self.keys[row]), '') is not '':
			self.del_editDic[row]=self.requireddata[self.keys[row]]		
		self.edit.setEnabled(True)
		self.delete.setEnabled(True)
		#print(self.requireddata[str(row)])	
		
	def ServerAction(self,supplierid):
		
		data = QtCore.QByteArray()
		data.append("action=deletesupplier&")
		data.append("supplierid={}".format(supplierid))
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
	        
	        if json_ar['delete']=='yes':
	        	self.table.clear()
	        	del self.requireddata[str(self.keys[self.delkey])]
	        	self.table.setRowCount(len(self.requireddata))
	        	json.dump(self.requireddata,open("db/suppliersdata.json", "w"))
	        	self.table.setHorizontalHeaderLabels(["  Supplier","         Account Payable        ","         Due date           ","          Phone   "])
	        	self.SupplierData()
	        	self.dialog.close()
	        	self.edit.setDisabled(True)
	        	self.delete.setDisabled(True)
	        	QMessageBox.critical(self, 'Databese Connection  ', "Supplier deleted successfully    \n")
        	return False
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "{} \n 	".format(reply.errorString()))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Suppliers('')
	ex.show()
	sys.exit(app.exec_())
