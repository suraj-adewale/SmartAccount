from PyQt5.QtWidgets import QPushButton,QListWidget,QDialogButtonBox,QDialog,QAbstractItemView,QTableWidget,QCompleter,QTableWidgetItem,QTextEdit,QLabel,QFormLayout,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPainter
from PyQt5.QtCore import Qt, QDate,QDateTime,pyqtSignal
import sys, json,base64
from babel.numbers import format_currency,parse_number,format_number,parse_decimal,format_decimal
from suppliers import Suppliers
from addsupplier import AddSupplier
from addaccount import AddAccount

class ImageWidget(QWidget):

    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)
#from server.routing import StartServer
class ClickableLineEdit(QLineEdit):
	clicked=pyqtSignal()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton: self.clicked.emit()

class PaymentPurchase(QMainWindow):
	def __init__(self,edit_data, parent=None):

		super(PaymentPurchase, self).__init__(parent)
		self.title = 'Payments and Purchases'
		self.left = (self.x()+430)
		self.top = (self.x()+150)
		self.width = 600
		self.height = 500
		self.edit_data=edit_data
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))

		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
		self.addJournalContent()
		self.setCentralWidget(self.widget)
		#self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)
		self.show()


	def addJournalContent(self):
		self.widget=QWidget()		
		
		requireddata1=open("db/accounts.json", "r")
		self.requireddata1=json.load(requireddata1)

		requireddata2=open("db/paysuppliersdata.json", "r")
		self.requireddata2=json.load(requireddata2)

		requireddata3=open("db/cashaccounts.json", "r")
		self.requireddata3=json.load(requireddata3)

		self.widgetDic={}
				
		self.balance=self.comborow=self.dc_balance=self.amountpayable=0
		self.row=10
		self.display_text=''

		self.rowCounts=self.row

		self.MessageBox=QMessageBox()
		
		self.amt_placeholder=format_currency(0,'NGN', locale='en_US')

		self.mainlayout=QVBoxLayout()
		labellayout=QVBoxLayout()
		formlayout=QFormLayout()	
		formlayout.setHorizontalSpacing(150)
		tablelayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)

		self.mainlayout.addLayout(labellayout,1)
		self.mainlayout.addLayout(formlayout,2)
		self.mainlayout.addLayout(tablelayout,5)

		date=QLabel("Transaction date:")
		supplier=QLabel("Pay to:")
		paymentfrom=QLabel("Accounts paid from:")
		balance=QLabel("Accounts Balance:")
		method=QLabel("Method:")
		amount=QLabel("Amount:")
		ref=QLabel("Reference number:")
		ref1=QLabel("Transaction reference:")
		memo=QLabel("Memo:")

		self.date1()
		supplierlayout=QGridLayout()
		self.supplier=QComboBox()
		self.supplier.setEditable(True)
		self.supplierbtn=QPushButton("")
		self.supplieredit=QPushButton("")
		supplierlayout.addWidget(self.supplier,0,0,0,4)
		supplierlayout.addWidget(self.supplierbtn,0,4)
		supplierlayout.addWidget(self.supplieredit,0,5)
		self.paymentfrom=QComboBox()
		self.balance=QLineEdit()
		self.method=QComboBox()
		self.amount=ClickableLineEdit()
		self.ref=QLineEdit()
		self.ref1=QLineEdit('PMT[AUTO]')
		self.memo=QTextEdit()
		self.memo.setToolTip("Enter the transactions discription.")

		self.supplierbtn.setIcon(QIcon('image/icon/team.png'))
		self.supplierbtn.setIconSize(QtCore.QSize(20,20))
		self.supplieredit.setIcon(QIcon('image/icon/boy.png'))
		self.supplieredit.setIconSize(QtCore.QSize(15,15))

		self.amount.setPlaceholderText(self.amt_placeholder)
		self.amount.textChanged.connect(self.text_changed_function)
		self.amount.clicked.connect(self.PaymentAmount)
		self.amount.clicked.connect(self.ClickableLinedit)
		self.memo.setMaximumHeight(50)
		self.memo.setText(" Payments")
		self.balance.setReadOnly(True)
		
		self.paypayabledata=self.requireddata2

		#self.supplier.addItem("")
		row=0
		supplierList=[]
		self.supplier.addItem("")
		for item in self.paypayabledata:
			self.supplier.insertItem(row,item)
			row=row+1
			supplierList.append(item)
		completer = QCompleter(supplierList)
		self.supplier.setCompleter(completer)

		self.paymentfrom.currentTextChanged.connect(self.PaymentFromChange)	
		self.cashaccountdata=self.requireddata3
		self.paymentfrom.addItem("")
		self.paymentfrom.insertItem(0,"-- Create new account --")
		
		for key in sorted(self.cashaccountdata):
			self.paymentfrom.insertItem(int(key)+1,self.cashaccountdata[key][1])
		
		self.method.addItems(["Cash","Check","Credit Card","Bank Deposit","Other"])
				
		self.supplierbtn.clicked.connect(self.SupplierWindow)
		self.supplieredit.clicked.connect(self.SupplierEdit)

		formlayout.addRow(date,self.dateedit1)
		formlayout.addRow(supplier,supplierlayout)
		formlayout.addRow(paymentfrom,self.paymentfrom)
		formlayout.addRow(balance,self.balance)
		formlayout.addRow(method,self.method)
		formlayout.addRow(amount,self.amount)
		formlayout.addRow(ref,self.ref)
		formlayout.addRow(ref1,self.ref1)
		formlayout.addRow(memo,self.memo)
		
		self.addJournalTable()
		tablelayout.addWidget(QLabel("Account Allocation"))
		tablelayout.addLayout(self.tablelayout)
		self.balencelabel=QLineEdit()
		tablelayout.addWidget(self.balencelabel,1)
		#tablelayout.addSeparator()
		buttongridLayout=QGridLayout()
		tablelayout.addLayout(buttongridLayout)
		self.templatebutton=QPushButton("Save As Template...")
		recordbutton=QPushButton("Record")
		cancelbutton=QPushButton("Cancel")
		helpbutton=QPushButton("Help")

		try:
			self.template=json.load(open("db/paymentpurchase_template.json","r"))
			self.templatebutton.setText("Use Template {}".format(len(self.template)))
		except Exception as e:
			json.dump({},open("db/paymentpurchase_template.json", "w"))
			self.template={}

		if len(self.template)==0:
			self.templatebutton.setDisabled(True)
			self.templatebutton.setText("Use Template {}".format(len(self.template)))

		self.templatebutton.clicked.connect(self.Template)
		
		recordbutton.clicked.connect(self.PostData)
		cancelbutton.clicked.connect(self.Cancel_button)

		buttongridLayout.addWidget(self.templatebutton,0,0,0,2)
		buttongridLayout.addWidget(QLabel(),0,2)
		buttongridLayout.addWidget(QLabel(),0,3)
		buttongridLayout.addWidget(recordbutton,0,4)
		buttongridLayout.addWidget(cancelbutton,0,5)
		buttongridLayout.addWidget(helpbutton,0,6)

		self.AddData()
	
	def AddData(self):

		if self.edit_data !={}:
			if 'data' in self.edit_data:
				edit_data=self.edit_data["data"]
				del self.edit_data['data']
				date=edit_data[0]
				supplier=edit_data[1]
				paymentfrom=edit_data[2]
				method=edit_data[3]
				amount=edit_data[4]
				memo=edit_data[5]

				year=(date.split('-'))[0]
				month=(date.split('-'))[1]
				day=(date.split('-'))[2]

				self.dateedit1.setDate(QDate(int(year),int(month),int(day)))
				self.supplier.setCurrentText(supplier)
				self.paymentfrom.setCurrentText(paymentfrom)
				self.method.setCurrentText(method)
				self.amount.setText(amount)
				self.memo.setText(memo)
				del self.edit_data[str(len(self.edit_data)-1)]
				
			self.UpdateRows(self.edit_data)
			self.text_changed_function()
			self.comborow=len(self.edit_data)

			if self.comborow>10:
				self.rowCounts=(self.comborow+5)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()
	
	
	def PaymentAmount(self):
		self.amount.setText(str(self.dc_balance))
		#print(self.dc_balance)

	def date1(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit1 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)

	def PaymentFromChange(self,obj):
		self.cashaccountdata=self.requireddata3
		if obj=='':
			return False
		if obj=="-- Create new account --":
			self.newaccount=AddAccount()
			self.newaccount.show()
			return False
		index=(self.paymentfrom.currentIndex())
		
		self.balance.setText(format_currency(self.cashaccountdata[str(index-1)][2],'NGN', locale='en_US'))
				
	def ClickableLinedit(self):
		self.amount.setText(str(self.amountpayable))
		

	def SupplierWindow(self):
		self.supplierlist=Suppliers(self)
		self.supplierlist.show()
	
	def SupplierEdit(self):
		self.supplieredit=AddSupplier({})	
		self.supplieredit.show()	
	

	def addJournalTable(self):
		JournalHeader=["Account ","	  Amount    ","    DR/CR     ",""]
		self.tablelayout=QVBoxLayout()
		self.table =QTableWidget()
		self.table.setColumnCount(4)     #Set three columns
		self.table.setRowCount(self.row)
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		#self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = self.table.horizontalHeader()       
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1,2*(QtWidgets.QHeaderView.Stretch)//2)
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
			
	def addJournalTable(self):
		JournalHeader=["Account ","			Amount   		","    DR/CR     ",""]
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
		self.templatebutton.setEnabled(True)
		self.templatebutton.setText("Save As Template...")
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
					Dr_=Dr_+(parse_decimal((self.widgetDic[key][1]).text(), locale='en_US'))
							
				if (self.widgetDic[key][2]).currentText()=='Credit' and (self.widgetDic[key][1]).text() is not '':
					Cr_=Cr_+(parse_decimal((self.widgetDic[key][1]).text(), locale='en_US'))
					
			bal= (self.amountpayable+ Cr_  - Dr_)
			
			if (self.amountpayable+Dr_) > Cr_:
				(self.widgetDic[self.comborow-1][2]).setCurrentText('Debit')
				(self.widgetDic[self.comborow-1][1]).setText(format_number(bal, locale='en_US'))
			
			if  (self.amountpayable+Dr_) < Cr_:
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
			(self.widgetDic[self.comborow][2]).currentTextChanged.connect(self.text_changed_function)
			
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

		self.template=json.load(open("db/paymentpurchase_template.json","r"))	
		if len(self.template)==0 and len(self.widgetDic)==0:
			self.templatebutton.setText("Use Template {}".format(len(self.template)))
			self.templatebutton.setDisabled(True)
		elif len(self.template)>0 and len(self.widgetDic)==0:
			self.templatebutton.setText("Use Template {}".format(len(self.template)))
			self.templatebutton.setEnabled(True)

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
			bal=(parse_decimal(amountpayable,locale='en_US')+ Credit_bal - Debit_bal)
		except Exception as e:
			List=list(amountpayable)
			del List[-1]
			(self.amount).setText(str(','.join(List)).replace(',',''))
			return False
	
		if abs(bal)>0:
			bal=format_currency(bal,'NGN', locale='en_US')
			self.balencelabel.setText('   Amount not yet applied to an account (out of balance):  {}'.format(bal))
		else:
			self.balencelabel.setText('  ')
		self.amountpayable=(abs(Debit_bal- Credit_bal))

	def comboboxAccount_changed(self,row):
		pass	
	
	def Template(self):
		text=self.templatebutton.text()
		if text=="Save As Template...":
			self.NewTemplate()
		if text=="Use Template {}".format(len(self.template)):
			self.ViewTemplate()	
	
	def ViewTemplate(self):
		self.dialog=QDialog(self)
		layout = QGridLayout()
		self.dialog.setWindowTitle("Templates")
		self.dialog.setLayout(layout)
		self.listwidget = QListWidget()
		layout.addWidget(self.listwidget)
		row=0
		for keyname in self.template:
			self.listwidget.insertItem(row, keyname)
			row=row+1
		self.listwidget.clicked.connect(self.TemplateList)

		self.delbtn=QPushButton("Delete Template")
		self.delbtn.clicked.connect(self.DeleteTemplate)
		layout.addWidget(self.delbtn)
		self.delbtn.setDisabled(True)
		self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		self.buttonbox.accepted.connect(self.Load)
		self.buttonbox.rejected.connect(self.dialog.close)
		self.buttonbox.setDisabled(True)
		layout.addWidget(self.buttonbox)
		self.dialog.exec_()

	

	def DeleteTemplate(self):
		
		item = (self.listwidget.currentItem()).text()
		self.template.pop(item)
		self.listwidget.clear()
		row=0
		for keyname in self.template:
			self.listwidget.insertItem(row, keyname)
			row=row+1
		self.listwidget.clicked.connect(self.TemplateList)
		
		json.dump(self.template,open("db/paymentpurchase_template.json", "w"))
		self.templatebutton.setText("Use Template {}".format(len(self.template)))
		if len(self.template)==0:
			self.templatebutton.setDisabled(True)
			self.delbtn.setDisabled(True)
			self.buttonbox.setDisabled(True)
		
	def Load(self):
		item = (self.listwidget.currentItem()).text()
		data=self.template[item]
		self.edit_data = (data)
		self.AddData()
		self.dialog.close

	def TemplateList(self, qmodelindex):
		self.delbtn.setEnabled(True)
		self.buttonbox.setEnabled(True)
		item = (self.listwidget.currentItem()).text()	

	def NewTemplate(self):
				
		self.dialog=QDialog(self)
		self.dialog.setWindowTitle("New Template")
		layout=QVBoxLayout()
		self.dialog.setLayout(layout)
		self.templatename=QLineEdit()
		self.templatename.setPlaceholderText("Type name...")

		layout.addWidget(self.templatename)
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		layout.addWidget(buttonbox)

		buttonbox.accepted.connect(self.SaveTemplate)
		buttonbox.rejected.connect(self.dialog.close)

		self.dialog.exec_()

	def SaveTemplate(self):
		self.SaveRecord()

		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)

		self.template_data=[]
		self.template_data.append(date)
		self.template_data.append(self.supplier.currentText())
		self.template_data.append(self.paymentfrom.currentText())
		self.template_data.append(self.method.currentText())
		self.template_data.append(self.amount.text())
		self.template_data.append(self.memo.toPlainText())

		name=self.templatename.text()
		if self.postDic=={}:
			return False
		if name=="":
			return False
		date = QDate()
		currentdate=date.currentDate()
		year=currentdate.year()
		month=currentdate.month()
		day=currentdate.day()
		date=(str(day)+'-'+str(month)+'-'+str(year))
		keyname=name+'  '+date
		try:
			template=json.load(open("db/paymentpurchase_template.json","r"))
			if keyname in template:
				QMessageBox.critical(self, '', "\nThe Template '{}' already exists, Do you want \nto replace it? 	\n".format(name))
				QMessageBox.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel|QMessageBox.Help)
		except Exception as e:
			template={}

		self.postDic['data']=self.template_data
		template[keyname]=self.postDic
		json.dump(template,open("db/paymentpurchase_template.json", "w"))	
		self.dialog.close()

	def Cancel_button(self):
		self.close()

	def PostData(self):
		self.SaveRecord()
		if self.error_count==0:
			self.PostJournal()	
				
	def SaveRecord(self):
		self.postDic={}
		self.error_count=0
		cashtext=self.paymentfrom.currentText()
		if cashtext=='' or cashtext=="-- Create new account --":
			self.error_count+=1
			QMessageBox.critical(self, 'Account', "\nPlease select the affected account	\n")
			return False
		
		paymentfromacct=self.cashaccountdata[str(self.paymentfrom.currentIndex()-1)]	
		#print(paymentfromacct)
		supplier=self.supplier.currentText()
		if supplier=='':
			self.error_count+=1
			QMessageBox.critical(self, 'Supplier', "\nChoose a supplier from suppliers dropdown	\n")
			return False
			
		self.payableref=self.ref.text()	

		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)

		user=json.load(open("db/user.json", "r"))
		
		journaltype="Payments"
		ref=(self.ref.text())
		memo=(self.memo.toPlainText())+';'+supplier

		
		ref="PMT[AUTO]"
			
		Account=amount=dc=0
		
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
						self.MessageBox.setInformativeText("Empty field at row {}	".format(row+1))
						self.MessageBox.setIcon(self.MessageBox.Critical)
						self.MessageBox.setStandardButtons(self.MessageBox.Close)
						self.MessageBox.show()
						self.error_count+=1
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
			self.postDic[row]=postList
		
		amount=float(parse_decimal(self.amount.text(),locale='en_US')) 
		bal=(amount + Credit_bal - Debit_bal)

		#print(amount + Credit_bal , Debit_bal)

		if abs(bal)>0.00001:
			bal=format_currency(bal,'NGN', locale='en_US')
			self.balencelabel.setText(' Amount not yet applied to an account (out of balance):  {}'.format(bal))
			self.error_count+=1
			return False
		self.balencelabel.setText('')
		if rows>0:
			paymentfromacct=paymentfromacct[0]+' - '+paymentfromacct[1]
			postList=[]
			postList.append(paymentfromacct)			
			postList.append(amount)
			postList.append('Credit')	
			postList.append(ref)
			postList.append(journaltype)
			postList.append(memo)
			postList.append(date)
			postList.append(user)
			self.postDic[row+1]=postList
				
	def PostJournal(self):
		self.postDic=json.dumps(self.postDic)
		self.postDic=base64.b64encode(self.postDic.encode())

		data = QtCore.QByteArray()
		data.append("action=postjournal&")
		data.append("paymentpurchase=paymentpurchase&")
		data.append("journal={}".format(self.postDic.decode("utf-8")))
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
	        	#self.table.clear()
	        	self.PaymentFromChange(self.paymentfrom.currentIndex())
	        
	        result = self.MessageBox.exec_()
	        if result==self.MessageBox.Ok:
	        	pass
	        
	    else:
	       QMessageBox.critical(self, 'Databese Connection  ', "{}   ".format(reply.errorString()))

	      

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = PaymentPurchase({})
	ex.show()
	sys.exit(app.exec_())