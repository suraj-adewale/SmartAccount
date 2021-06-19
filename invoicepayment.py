from PyQt5.QtWidgets import QPushButton,QAbstractItemView,QTableWidget,QTextEdit,QCompleter,QTableWidgetItem,QLabel,QFormLayout,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime,pyqtSignal
import sys, json,base64
from babel.numbers import format_currency,parse_decimal,parse_number 
from suppliers import Suppliers
from addsupplier import AddSupplier
from addaccount import AddAccount
from addcustomer import AddCustomer
from customers import Customers

#from server.routing import StartServer
class ImageWidget(QWidget):

    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)
        
class ClickableLineEdit(QLineEdit):
	clicked=pyqtSignal()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton: self.clicked.emit()

class InvoivePayment(QMainWindow):
	def __init__(self, parent=None):
		super(InvoivePayment, self).__init__(parent)
		self.title = 'Customer Payment'
		self.left = (self.x()+430)
		self.top = (self.x()+150)
		self.width = 600
		self.height = 500
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		usertype_db=open("db/usertype.json", "r")
		usertype=json.load(usertype_db)
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			ipaddress=open("db/ipaddress.json", "r")
			self.ip=json.load(ipaddress)
		
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
		self.addJournalContent()
		self.setCentralWidget(self.widget)
		self.show()
	
	def window_close(self):
		self.close()	

	def addJournalContent(self):
		
		self.widget=QWidget()
		
		
		self.requireddata1=json.load(open("db/invoicepaymentdata.json", "r"))

		self.requireddata2=json.load(open("db/cashaccounts.json", "r"))

		self.requireddata=json.load(open("db/addinvoice.json", "r"))

	
		self.appliedList=[]
		self.customerpayable=''		
		self.balance=self.comborow=self.dc_balance=self.amountpayable=0
		

		self.MessageBox=QMessageBox()
		self.amt_placeholder=format_currency(0,'NGN', locale='en_US')

		self.journaltypelist=["General","Payments","Sales","Receipts","Purchases"]
		self.journalAuto=["GJ[AUTO]","PMT[AUTO]","SLS[AUTO]","REC[AUTO]","PRC[AUTO]"]

		self.mainlayout=QVBoxLayout()
		labellayout=QVBoxLayout()
		formlayout=QFormLayout()	
		formlayout.setHorizontalSpacing(150)
		tablelayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)

		self.mainlayout.addLayout(labellayout,1)
		self.mainlayout.addLayout(formlayout,2)
		self.mainlayout.addLayout(tablelayout,5)

		date=QLabel("Date:")
		customer=QLabel("customer:")
		deposit=QLabel("Deposit accounts :")
		method=QLabel("Method:")
		amount=QLabel("Amount:")
		ref=QLabel("Reference number:")
		memo=QLabel("Memo:")

		self.date1()
		customerlayout=QGridLayout()
		self.customer=QComboBox()
		self.customerbtn=QPushButton("")
		self.customeredit=QPushButton("")
		customerlayout.addWidget(self.customer,0,0,0,4)
		customerlayout.addWidget(self.customerbtn,0,4)
		customerlayout.addWidget(self.customeredit,0,5)
		self.deposit=QComboBox()
		self.method=QComboBox()
		self.amount=ClickableLineEdit()
		self.ref=QLineEdit()
		self.memo=QTextEdit()
		self.memo.setToolTip("Enter the transactions discription.")

		self.customerbtn.setIcon(QIcon('image/icon/team.png'))
		self.customerbtn.setIconSize(QtCore.QSize(20,20))
		self.customeredit.setIcon(QIcon('image/icon/boy.png'))
		self.customeredit.setIconSize(QtCore.QSize(15,15))

		self.amount.setPlaceholderText(self.amt_placeholder)
		self.amount.textChanged.connect(self.text_changed_function)
		self.amount.clicked.connect(self.ClickableLinedit)
		self.memo.setMaximumHeight(50)
		self.memo.setText(" Receipts")

		self.customer.currentTextChanged.connect(self.CustomerChange)
		self.InvoivePaymentdata=self.requireddata1
		
		
		self.customer.addItem("")
		data=self.requireddata["customerdata"]
		print(sorted(data))
		print((data))
		row=0
		for item in sorted(data):
			self.customer.insertItem(row,data[item][0])
			row+=1
		self.cashaccountdata=self.requireddata2
		self.deposit.addItem("")
		for key in sorted(self.cashaccountdata):
			self.deposit.insertItem(0,self.cashaccountdata[key][1])
			
					
		self.method.addItems(["Cash","Check","Credit Card","Bank Deposit","Other"])
				
		self.customerbtn.clicked.connect(self.CustomerWindow)
		self.customeredit.clicked.connect(self.CustomerEdit)

		formlayout.addRow(date,self.dateedit1)
		formlayout.addRow(customer,customerlayout)
		formlayout.addRow(amount,self.amount)
		formlayout.addRow(method,self.method)
		formlayout.addRow(deposit,self.deposit)
		formlayout.addRow(ref,self.ref)
		formlayout.addRow(memo,self.memo)
		
		self.addJournalTable()
		tablelayout.addWidget(QLabel("Account Allocation"))
		tablelayout.addLayout(self.tablelayout)
		self.balencelabel=QLineEdit()
		tablelayout.addWidget(self.balencelabel,1)
		#tablelayout.addSeparator()
		buttongridLayout=QGridLayout()
		tablelayout.addLayout(buttongridLayout)
		templatebutton=QPushButton("Save As Template...")
		recordbutton=QPushButton("Record")
		cancelbutton=QPushButton("Cancel")
		helpbutton=QPushButton("Help")

		templatebutton.clicked.connect(self.Save_template)
		recordbutton.clicked.connect(self.Save_record)
		cancelbutton.clicked.connect(self.Cancel_button)

		buttongridLayout.addWidget(templatebutton,0,0,0,2)
		buttongridLayout.addWidget(QLabel(),0,2)
		buttongridLayout.addWidget(QLabel(),0,3)
		buttongridLayout.addWidget(recordbutton,0,4)
		buttongridLayout.addWidget(cancelbutton,0,5)
		buttongridLayout.addWidget(helpbutton,0,6)
	
	def date1(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit1 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)
	
	def CustomerChange(self,obj):
		print(obj)
		
		if obj=='':
			return False
		#obj=self.customer.currentText()	
		self.paidupdate={}	
		self.customerdata=self.requireddata1
		customer=self.customerdata[obj]	
		self.row=len(customer)
		self.table.setRowCount(0)
		if self.row>0:
			self.table.setRowCount(self.row+10)
		self.totalamount=0
		self.appliedList=[]
		for items in customer:
			applied=ClickableLineEdit()
			self.totalamount=self.totalamount+float(items[5])
			row=customer.index(items)
			self.table.setCellWidget(int(row),0,QLabel(items[3]))
			self.table.setCellWidget(int(row),1,QLabel(items[1]))
			self.table.setCellWidget(int(row),2,QLabel(items[2]))
			self.table.setCellWidget(int(row),3,QLabel(str(format_currency(float(items[4]),'NGN', locale='en_US'))))
			
			if float(items[5])==0.0:
				self.table.setCellWidget(int(row),4,QLabel(''))
				self.table.setCellWidget(int(row),5,QLabel(''))
			else:	
				self.table.setCellWidget(int(row),4,QLabel(str(format_currency(float(items[5]),'NGN', locale='en_US'))))
				self.table.setCellWidget(int(row),5,applied)
				applied.setText(str(format_currency(float(items[5]),'NGN', locale='en_US')))	
				applied.textChanged.connect(self.text_changed_function)
				applied.clicked.connect(self.ClickableLinedit)
				self.appliedList.append(applied)
				self.paidupdate[items[6]]=applied

		self.amount.setText(str(format_currency((self.totalamount),'NGN', locale='en_US')))
		self.table.resizeRowsToContents()

	def ClickableLinedit(self):
		widget=self.sender()
		widget.setText(str(0.00))

	def CustomerWindow(self):
		self.customerlist=Customers(self)
		self.customerlist.show()
	
	def CustomerEdit(self):
		self.customeredit=AddCustomer({})	
		self.customeredit.show()	
	
	def addJournalTable(self):
		JournalHeader=["	Bill #	","	Date   ","	Date Due ","	Total   	","	Due 	 ","	applied  "]
		self.tablelayout=QVBoxLayout()
		self.table =QTableWidget()
		self.table.setColumnCount(len(JournalHeader))     #Set three columns
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		#self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = self.table.horizontalHeader()       
		header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3,QtWidgets.QHeaderView.Stretch)

		self.tablelayout.addWidget(self.table)
				
		self.table.clicked.connect(self.AddJournals)
		
		self.table.resizeRowsToContents()
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(JournalHeader)
		
		self.table.horizontalHeaderItem(0).setToolTip("Click on any row to add an account")
		self.table.horizontalHeaderItem(1).setToolTip("Type amount here")
		self.table.horizontalHeaderItem(2).setToolTip("Choose either Debit or Credit")
		self.table.horizontalHeaderItem(3).setToolTip("Click to delete a row")
		
	def AddJournals(self,item):
		currRow=(item.row())
	
	def text_changed_function(self):
		#print(self.sender())
		self.totalpayble=0
		if self.appliedList==[]:
			return False
		for item in self.appliedList:
			payable=((item.text()).split('₦'))
			print(payable)
			
			if len(payable)==2:
				self.totalpayble=self.totalpayble+(parse_decimal(payable[1],locale='en_US'))
			if len(payable)==1 and payable[0]!='':
				self.totalpayble=self.totalpayble+(parse_decimal(payable[0],locale='en_US'))
				

		if self.amount.text()=='' or self.amount.text()=='0':
			self.amountpayable = 0
			bal=abs(self.totalpayble-self.amountpayable)
			bal=format_currency(abs(bal),'NGN', locale='en_US')
			self.balencelabel.setText('   Amount not yet applied to an account (out of balance):  {}'.format(bal))
			return False
		else:
			amountpayable =(self.amount.text()).split('₦')

		if amountpayable[0]=='':
			self.amountpayable=parse_decimal(amountpayable[1],locale='en_US')
		else:
			self.amountpayable=parse_decimal(amountpayable[0],locale='en_US')
		
		
		bal=abs(self.totalpayble-self.amountpayable)
		if bal>0:
			bal=format_currency(abs(bal),'NGN', locale='en_US')
			self.balencelabel.setText('   Amount not yet applied to an account (out of balance):  {}'.format(bal))
		else:
			self.balencelabel.setText('  ')

	def comboboxAccount_changed(self,row):
		pass	
	
	def Save_template(self):
		pass
	def Cancel_button(self):
		AddJournal().window_close()
				
	def Save_record(self):
		self.customerpayable=self.customer.currentText()
		if self.customerpayable=='':
			print('no customer')
			return False
		if self.deposit.currentText()=='':
			print('no payable from')
			return False	
		
		
		method=self.method.currentText()	
		self.payableref=self.ref.text()	

		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)
		

		userdb=open("db/user.json", "r")
		
				
		ref="REC[AUTO]"
		customer=self.customer.currentText()
		memo=(self.memo.toPlainText())
		memo=memo+';'+customer
		
		user=json.load(userdb)

		ref1=(self.ref.text())

		payableList={}
		for invoiceid in self.paidupdate:
			paidupdate=((self.paidupdate[invoiceid]).text()).split('₦')
			if paidupdate[0]=='':
				payableList[invoiceid]=[float(parse_decimal(paidupdate[1],locale='en_US')),date,method]
			else:	
				payableList[invoiceid]=[float(parse_decimal(paidupdate[0],locale='en_US')),date,method]

		postDic={}
		receivableacct=self.customerdata[self.customer.currentText()]
		depositacct=self.cashaccountdata[str(self.deposit.currentIndex())]
		depositacct=depositacct[0]+' - '+depositacct[1]
		
		row=0
		key=sorted((payableList).keys())
		for each in key:
			postList=[]
			postList.append(receivableacct[row][7])
			postList.append(float(payableList[each][0]))
			postList.append('Credit')
			postList.append(ref)
			postList.append("Receipts")
			postList.append(memo)
			postList.append(date)
			postList.append(user)
			postDic[row]=postList
			row=row+1

		postList=[]
		postList.append(depositacct)
		postList.append(float(self.amountpayable))
		postList.append('Debit')
		postList.append(ref)
		postList.append("Receipts")
		postList.append(memo)
		postList.append(date)
		postList.append(user)
		postList.append(ref1)
		postList.append(payableList)
		postDic[row]=postList

		
			
		#print(postDic)		
		if abs(self.amountpayable-self.totalpayble)>0.00001:
			self.MessageBox.setWindowTitle('Payments')
			self.MessageBox.setText("")
			self.MessageBox.setInformativeText("\n 	Amount must be equal  		\n")
			self.MessageBox.setIcon(self.MessageBox.Critical)
			self.MessageBox.setStandardButtons(self.MessageBox.Close)
			self.MessageBox.show()
			return False
		
						
		postDic=json.dumps(postDic)
		postDic=base64.b64encode(postDic.encode())
		
		data = QtCore.QByteArray()
		data.append("action=postjournal&")
		data.append("invoicepayment=invoicepayment&")
		data.append("journal={}".format(postDic.decode("utf-8")))
		url = "http://{}:5000/journal".format(self.ip)
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
	        
	        json_ar = json.loads(str(bytes_string, 'utf-8'))
	        #data = json_ar['form']
	        if json_ar['19']=='Success':
	        	journaltype=json_ar['30']
	        	ref=json_ar['25']
	        	date=json_ar['35']
	        	self.MessageBox.setWindowTitle('Post Journal')
	        	self.MessageBox.setText("")
	        	self.MessageBox.setInformativeText("{j} Journal with Ref: {r} was succesfully posted\non {d}. " "\n\nClick Ok to exit.".format(j=journaltype,r=ref,d=date))
	        	self.MessageBox.setIcon(self.MessageBox.Information)
	        	self.MessageBox.setStandardButtons(self.MessageBox.Ok)
	        	self.MessageBox.show()
	        	#self.table.clearContents()
	        	self.CustomerChange(self.customer.currentText())
	        
	        result = self.MessageBox.exec_()
	        if result==self.MessageBox.Ok:
	        	pass
	        
	    else:
	       QMessageBox.critical(self, 'Databese Connection  ', "\n {}	 \n".format(reply.errorString()))

	      

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = InvoivePayment()
	ex.show()
	sys.exit(app.exec_())