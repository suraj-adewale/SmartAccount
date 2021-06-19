from PyQt5.QtWidgets import QPushButton,QAbstractItemView,QTableWidget,QCompleter,QTableWidgetItem,QTextEdit,QLabel,QFormLayout,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPainter
from PyQt5.QtCore import Qt, QDate,QDateTime,pyqtSignal
import sys, json,base64
from babel.numbers import format_currency,parse_number,format_number,parse_decimal,format_decimal
from suppliers import Suppliers
from addsupplier import AddSupplier
from addaccount import AddAccount

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

class Payable(QMainWindow):
	def __init__(self, parent=None):
		super(Payable, self).__init__(parent)
		self.title = 'Accounts Payable'
		self.left = (self.x()+430)
		self.top = (self.x()+150)
		self.width = 500
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
		self.addPayableContent()
		self.setCentralWidget(self.widget)
		#self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)
		self.show()
	
	
	def addPayableContent(self):
		
		self.widget=QWidget()
		
		requireddata1=open("db/accounts.json", "r")
		self.requireddata1=json.load(requireddata1)

		requireddata2=open("db/suppliersdata.json", "r")
		self.requireddata2=json.load(requireddata2)

		requireddata3=open("db/payabledata.json", "r")
		self.requireddata3=json.load(requireddata3)

		self.widgetDic={}
		self.payableaccount=''		
		self.balance=self.comborow=self.dc_balance=0
		self.row=10
		self.display_text=''

		self.rowCounts=self.row

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
		duedate=QLabel("Due Date:")
		supplier=QLabel("supplier:")
		address=QLabel("supplier Address:")
		payable=QLabel("Accounts Payable:")
		balance=QLabel("Accounts Balance:")
		amount=QLabel("Amount:")
		ref=QLabel("Reference number:")
		memo=QLabel("Memo:")

		self.date1()
		self.date2()

		supplierlayout=QGridLayout()
		self.supplier=QComboBox()
		self.supplierbtn=QPushButton("")
		self.supplieredit=QPushButton("")
		supplierlayout.addWidget(self.supplier,0,0,0,4)
		supplierlayout.addWidget(self.supplierbtn,0,4)
		supplierlayout.addWidget(self.supplieredit,0,5)
		self.address=QTextEdit()
		self.address.setMaximumHeight(50)
		self.payable=QComboBox()
		self.balance=QLineEdit()
		self.amount=ClickableLineEdit()
		self.ref=QLineEdit()
		self.memo=QTextEdit()
		self.memo.setToolTip("Enter the transactions discription.")

		self.supplierbtn.setIcon(QIcon('image/icon/team.png'))
		self.supplierbtn.setIconSize(QtCore.QSize(20,20))
		self.supplieredit.setIcon(QIcon('image/icon/boy.png'))
		self.supplieredit.setIconSize(QtCore.QSize(15,15))

		self.balance.setReadOnly(True)
		self.amount.setPlaceholderText(self.amt_placeholder)
		self.amount.textChanged.connect(self.text_changed_function)
		self.amount.clicked.connect(self.Payable)
		self.memo.setMaximumHeight(50)
		self.memo.setText(" Purchases")

		self.supplier.currentTextChanged.connect(self.SupplierChange)

		self.supplierdata=self.requireddata2
		self.supplier.setEditable(True)
		self.supplier.addItem("")
		for item in sorted(self.supplierdata):
			self.supplier.insertItem(int(item),self.supplierdata[item][0])

		self.payable.currentTextChanged.connect(self.PayableChange)
		self.payable.addItem("")
		self.payable.insertItem(0,"-- Create new account --")

		self.payabledata3=self.requireddata3
		for item in sorted(self.payabledata):
			self.payable.insertItem(int(item)+1,self.payabledata[item][0])	
		
		self.supplierbtn.clicked.connect(self.SupplierWindow)
		self.supplieredit.clicked.connect(self.SupplierEdit)

		formlayout.addRow(date,self.dateedit1)
		formlayout.addRow(duedate,self.dateedit2)
		formlayout.addRow(supplier,supplierlayout)
		formlayout.addRow(address,self.address)
		formlayout.addRow(payable,self.payable)
		formlayout.addRow(balance,self.balance)
		formlayout.addRow(amount,self.amount)
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
	
	def Payable(self):
		self.amount.setText(str(self.dc_balance))
	def date1(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit1 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)

	def date2(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit2 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit2.setDate(currentdate)
		self.dateedit2.setDisplayFormat('dd/MM/yyyy')
		self.dateedit2.setCalendarPopup(True)	
	
	def PayableChange(self,obj):
		self.payabledata=self.requireddata3
		if obj=='':
			return False
		if obj=="-- Create new account --":
			self.newaccount=AddAccount('widg',[])
			self.newaccount.show()
			return False
		index=(self.payable.currentIndex())
		self.balance.setText(format_currency(self.payabledata[str(index-1)][1],'NGN', locale='en_US'))
		self.payableaccount=self.payabledata[str(index-1)]
	
	def SupplierChange(self,obj):

		if obj=='':
			return False
		for key,val in (self.supplierdata.items()):
			if (val[0]).lower()==obj.lower():	
				address=self.supplierdata[key][4]
				self.address.setText(address)
				self.supplier_data=self.supplierdata[key]
				break
			else:
				self.address.setText('')	
		
		
	def SupplierWindow(self):
		self.supplierlist=Suppliers(self)
		self.supplierlist.show()
	
	def SupplierEdit(self):
		self.supplieredit=AddSupplier('')	
		self.supplieredit.show()	
	

	def addJournalTable(self):
		JournalHeader=["Account","   Amount   ","    DR/CR     ",""]
		self.tablelayout=QVBoxLayout()
		self.table =QTableWidget()
		self.table.setColumnCount(4)     #Set three columns
		self.table.setRowCount(self.row)
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		#self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = self.table.horizontalHeader()       
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1,1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

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
		#self.templatebutton.setEnabled(True)
		#self.templatebutton.setText("Save As Template...")
		currRow=(item.row())
		AccountsList=self.requireddata1
		AccountsList.sort()
		
		if self.amount.text()=='':
			self.amountpayable = 0
		else:
			self.amountpayable = (parse_decimal(self.amount.text(), locale='en_US'))

		if item.column()==0:
			self.AddTableCell()
			Dr_=Cr_=0
			for key in self.widgetDic:
				if (self.widgetDic[key][2]).currentText()=='Debit' and (self.widgetDic[key][1]).text() is not '':
					Dr_=Dr_+ (parse_decimal((self.widgetDic[key][1]).text(), locale='en_US'))
							
				if (self.widgetDic[key][2]).currentText()=='Credit' and (self.widgetDic[key][1]).text() is not '':
					Cr_=Cr_+ (parse_decimal((self.widgetDic[key][1]).text(), locale='en_US'))	
			bal=abs(self.amountpayable-(Dr_ - Cr_))
			
			if self.amountpayable > abs(Dr_ - Cr_):
				(self.widgetDic[self.comborow-1][2]).setCurrentText('Debit')
				(self.widgetDic[self.comborow-1][1]).setText(format_number(bal, locale='en_US'))
			
			if  (self.amountpayable) < abs(Dr_ - Cr_):
				(self.widgetDic[self.comborow-1][2]).setCurrentText('Credit')
				(self.widgetDic[self.comborow-1][1]).setText(format_number(bal, locale='en_US'))
		
		self.text_changed_function()		
		if item.column()==3:
			self.DeleteRow(currRow)

	def AddTableCell(self):
		AccountsList=self.requireddata1
		AccountsList.sort()
		comboboxAccount=QComboBox()
		comboboxAccount.setEditable(True)
		completer = QCompleter(AccountsList)
		comboboxAccount.setCompleter(completer)
		amount=QLineEdit()
		amount.setPlaceholderText(self.amt_placeholder)
		debit_credit = QComboBox()
		comboboxAccount.setObjectName('comboboxAccount')
		comboboxAccount.addItem('')
		image = ImageWidget('image/icon/clear.png', self)

		if self.comborow not in self.widgetDic:
			widgetList=[]
			widgetList.append(comboboxAccount)
			widgetList.append(amount)
			widgetList.append(debit_credit)
			self.widgetDic[self.comborow]=widgetList
			(self.widgetDic[self.comborow][1]).textChanged.connect(self.text_changed_function)
			
		comboboxAccount.addItems(AccountsList)
		debit_credit.addItems(["Debit","Credit"])
		
		self.table.setCellWidget(self.comborow,0,comboboxAccount)
		self.table.setCellWidget(self.comborow,1,amount)
		self.table.setCellWidget(self.comborow,2, debit_credit)
		self.table.setCellWidget(self.comborow, 3, image)
		self.comborow=self.comborow+1
		
		if self.comborow==self.rowCounts:
			self.rowCounts+5
			self.rowCounts=(self.rowCounts+5)
			self.table.setRowCount(self.rowCounts)
			self.table.resizeRowsToContents()

	def DeleteRow(self,row):
		if row in self.widgetDic.keys():

			self.widgetDic.pop(row)
			journaldata={}
			index=0
			for key in sorted(self.widgetDic):
				data_list=[]
				for col in range(3):
					if col==0:	
						data_list.append((self.widgetDic[key][0]).currentText())
					if col==1:	
						data_list.append((self.widgetDic[key][1]).text())
					if col==2:	
						data_list.append((self.widgetDic[key][2]).currentText())		
				journaldata[index]=data_list
				index=index+1
				
			self.UpdateRows(journaldata)
			
			self.comborow=self.comborow-1
			if self.rowCounts>10:
				self.rowCounts=(self.rowCounts-1)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()

			self.text_changed_function()
	
	def UpdateRows(self,journaldata):
		self.table.clearContents()	
		self.widgetDic={}
		
		for keys in sorted(journaldata):
			try:
				widgetList=[]
				account=QComboBox()#self.widgetDic[keys][0]
				amount=QLineEdit()#self.widgetDic[keys][1]
				dc=QComboBox()#self.widgetDic[keys][2]					
				account.setEditable(True)
				AccountsList=self.requireddata1
				AccountsList.sort()
				account.addItem('')
				account.addItems(AccountsList)
				dc.addItems(["Debit","Credit"])

				completer = QCompleter(AccountsList)
				account.setCompleter(completer)

				amount.setPlaceholderText(self.amt_placeholder)

				amount.textChanged.connect(self.text_changed_function)
				dc.currentTextChanged.connect(self.text_changed_function)
	
				account.setCurrentText(journaldata[keys][0])
				amount.setText(str(journaldata[keys][1]))
				dc.setCurrentText(journaldata[keys][2])

				self.table.setCellWidget(int(keys),0,account)
				self.table.setCellWidget(int(keys),1,amount)
				self.table.setCellWidget(int(keys),2, dc)
				image = ImageWidget('image/icon/clear.png', self)
				self.table.setCellWidget(int(keys), 3, image)


				widgetList.append(account)
				widgetList.append(amount)
				widgetList.append(dc)
				
				self.widgetDic[int(keys)]=widgetList
				
			except Exception as e:
				raise(e)

	def text_changed_function(self):
	
		Debit_bal=Credit_bal=0
		for row in self.widgetDic:
			if ((self.widgetDic[row][1]).text())=='':
				return False
			try:
				amt=((self.widgetDic[row][1]).text())
				format_amt='{:,}'.format(int(amt.replace(',','')))
			except Exception as e:
				amt=((self.widgetDic[row][1]).text())
				format_amt=amt	
				
			(self.widgetDic[row][1]).setText(str(format_amt))

			try:
				if (self.widgetDic[row][2]).currentText()=='Debit':
			 		Debit_bal=Debit_bal+(parse_decimal(amt, locale='en_US'))
				if (self.widgetDic[row][2]).currentText()=='Credit':
			 		Credit_bal=Credit_bal+(parse_decimal(amt, locale='en_US'))
			except Exception as e:
				List=list(amt)
				del List[-1]
				(self.widgetDic[row][1]).setText(str(','.join(List)).replace(',',''))	

		try:
			amountpayable =(self.amount.text())
			if amountpayable=='':
				return False
			format_amt1='{:,}'.format(int(amountpayable.replace(',','')))
		except Exception as e:
			amountpayable =(self.amount.text())
			format_amt1=amountpayable
		(self.amount).setText(str(format_amt1))

		try:
			bal=abs(parse_decimal(amountpayable,locale='en_US')-abs(Debit_bal- Credit_bal))
		except Exception as e:
			List=list(amountpayable)
			del List[-1]
			(self.amount).setText(str(','.join(List)).replace(',',''))
			return False
	
		if abs(bal)>0:
			bal=format_currency(abs(bal),'NGN', locale='en_US')
			self.balencelabel.setText('   Amount not yet applied to an account (out of balance):  {}'.format(bal))
		else:
			self.balencelabel.setText('  ')
		self.amountpayable=(parse_decimal(amountpayable,locale='en_US'))

	def comboboxAccount_changed(self,row):
		pass	
	
	def Save_template(self):
		pass
	def Cancel_button(self):
		self.close()
				
	def Save_record(self):
		if self.payableaccount=='':
			print('no payable')
			return False
			
		self.payableref=self.ref.text()	

		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)

		date2=self.dateedit2.date()
		year2=str(date2.year())
		day2=str(date2.day()) if len(str(date2.day()))==2 else '0'+str(date2.day())
		month2=str(date2.month()) if len(str(date2.month()))==2 else '0'+str(date2.month())
		duedate=(year2+'-'+month2+'-'+day2)

		userdb=open("db/user.json", "r")
		user=json.load(userdb)
		
		journaltype="Purchases"
		ref1=(self.ref.text())
		memo=(self.memo.toPlainText())

		
		ref="PRC[AUTO]"
			
		Account=amount=dc=0
		postDic={}
		
		rows=len(self.widgetDic)
		cols=3
		Credit_bal=Debit_bal=0
		for row in range(rows):
			postList=[]
			for col in range(cols):
				if col==0:
					Account=(self.widgetDic[row][col]).currentText()
					postList.append(Account)
				if col==1:
					amount=(self.widgetDic[row][col]).text()
					if amount=='' or Account=='':
						self.MessageBox.setWindowTitle('Post Journal')
						self.MessageBox.setText("")
						self.MessageBox.setInformativeText("Empty field at row {}		\n".format(row+1))
						self.MessageBox.setIcon(self.MessageBox.Critical)
						self.MessageBox.setStandardButtons(self.MessageBox.Close)
						self.MessageBox.show()
						return False
					amount=float(parse_decimal(amount,locale='en_US'))	
					postList.append(amount)
				if col==2:
					dc=(self.widgetDic[row][col]).currentText()
					postList.append(dc)

					if dc=='Debit':
						Debit_bal=Debit_bal+float(amount)
					if dc=='Credit':
						Credit_bal=Credit_bal+float(amount)	
						
			postList.append(ref)
			postList.append(journaltype)
			postList.append(memo)
			postList.append(date)
			postList.append(user)
			postDic[row]=postList
		
		self.amountpayable=float(self.amountpayable)
		bal=abs(self.amountpayable-(Debit_bal - Credit_bal))
		if abs(bal)>0:
			bal=format_currency(abs(bal),'NGN', locale='en_US')
			self.balencelabel.setText('   Amount not yet applied to an account (out of balance):  {}'.format(bal))
			return False
		self.balencelabel.setText('')
		postList=[]
		postList.append(self.payableaccount[2])			
		postList.append(self.amountpayable)
		postList.append('Credit')	
		postList.append(ref)
		postList.append(journaltype)
		postList.append(memo)
		postList.append(date)
		postList.append(user)
		postList.append(self.payableref)
		postList.append(self.supplier_data[0])
		postList.append(duedate)
		postDic[row+1]=postList
				
		
		postDic=json.dumps(postDic)
		postDic=base64.b64encode(postDic.encode())
		
		data = QtCore.QByteArray()
		data.append("action=postjournal&")
		data.append("payable=payable&")
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
	        	self.table.clearContents()
	        
	        result = self.MessageBox.exec_()
	        if result==self.MessageBox.Ok:
	        	pass
	        
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', " {}    ".format(reply.errorString()))

	      

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Payable()
	ex.show()
	sys.exit(app.exec_())