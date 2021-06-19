from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QAction,QTabWidget,QCompleter,QTableWidgetItem,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QFormLayout,QTextEdit,QSpinBox
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPainter
from PyQt5.QtCore import Qt, QDate,QDateTime,pyqtSignal
from customers import Customers
from addcustomer import AddCustomer
import sys, json,base64
from babel.numbers import format_currency,parse_decimal#,parse_number 
from functools import partial

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

class Invoice(QMainWindow):
	def __init__(self,dic, parent=None):
		super(Invoice, self).__init__(parent)
		self.title = 'Invoice'
		self.left = (self.x()+230)
		self.top = (self.x()+50)
		self.width = 900
		self.height = 550
		self.edit_data=dic
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))
		#self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
		self.InvoiceContent()
		self.setCentralWidget(self.widget)
		self.show()
	
	def window_close(self):
		self.close()	



	def InvoiceContent(self):
		self.widget=QWidget()
		self.widgetDic={}
		self.balance=self.comborow=0
		self.row=10
		#self.row_col='00'
		self.rowCounts=self.row
		self.amt_placeholder=format_currency(0,'NGN', locale='en_US')

		self.requireddata=json.load(open("db/addinvoice.json", "r"))

		self.MessageBox=QMessageBox()
		mainlayout=QVBoxLayout()
		self.widget.setLayout(mainlayout)

		billinglayout=QHBoxLayout()
		mainlayout.addLayout(billinglayout,2)

		billingtab=QTabWidget()
		invoicetab=QTabWidget()
		billinglayout.addWidget(billingtab,3)
		billinglayout.addWidget(invoicetab,2)

		

		self.billing = QWidget()
		billingform=QFormLayout()
		billingform.setHorizontalSpacing(50)
		self.billing.setLayout(billingform)
		self.billing.setStatusTip("Enter supplier information")

		self.invoice = QWidget()
		invoiceform=QFormLayout()
		invoiceform.setHorizontalSpacing(50)
		self.invoice.setLayout(invoiceform)
		self.invoice.setStatusTip("Enter supplier information")

		billingtab.addTab(self.billing,"Billing")
		invoicetab.addTab(self.invoice,"Invoice")

		customerlayout=QGridLayout()
		self.customer=QComboBox()
		self.customer.setEditable(True)
		self.customerbtn=QPushButton("")
		self.customeredit=QPushButton("")
		customerlayout.addWidget(self.customer,0,0,0,4)
		customerlayout.addWidget(self.customerbtn,0,4)
		customerlayout.addWidget(self.customeredit,0,5)

		self.customerbtn.setIcon(QIcon('image/icon/team.png'))
		self.customerbtn.setIconSize(QtCore.QSize(20,20))
		self.customeredit.setIcon(QIcon('image/icon/boy.png'))
		self.customeredit.setIconSize(QtCore.QSize(15,15))

		self.customerbtn.clicked.connect(self.CustomerWindow)
		self.customeredit.clicked.connect(self.CustomerEdit)

		self.address=QTextEdit()
		self.address.setMaximumHeight(50)

		self.po_no=QLineEdit()

		self.customertax=QComboBox()
		self.customertax.addItems(['Default','Exempt'])

		createfromlayout=QGridLayout()
		self.createfrom=QComboBox()
		self.createfrombtn=QPushButton("")
		createfromlayout.addWidget(self.createfrom,0,0,0,4)
		createfromlayout.addWidget(self.createfrombtn,0,4)
		self.date()

		termlayout= QGridLayout()
		self.term=QComboBox()
		self.term.addItems(["Pay in days","COD"])
		self.spinbox = QSpinBox()
		self.spinbox.setValue(30)

		termlayout.addWidget(self.term,0,0)
		termlayout.addWidget(self.spinbox,0,1)
		self.salesperson=QComboBox()
		self.salesperson.setEditable(True)
		self.invoice_no=QLineEdit()
		self.invoice_no.setReadOnly(True)

		self.createfrom.addItems(["[ New Invoice]","Existing Invoice"])
		self.invoice_number=self.requireddata['invoiceno']
		self.invoice_no=QLineEdit(self.invoice_number)
		self.salesaccount=QComboBox()
		self.salesaccount.setEditable(True)
		self.receivableaccount=QComboBox()
		self.receivableaccount.setEditable(True)

		self.customerdata=self.requireddata['customerdata']
		self.customer.addItem("")
		self.customer.currentTextChanged.connect(self.CustomerChange)
		
		row=0
		for key in sorted(self.customerdata):
			self.customer.insertItem(row,self.customerdata[key][0])
			row=row+1

		self.revenueaccounts=self.requireddata['revenueaccounts']
		self.salesaccount.addItem("")
		self.salesaccount.insertItem(0,'-- Create a new account --')
		row=1
		completerlist=[]
		for key in self.revenueaccounts:
			self.salesaccount.insertItem(row,self.revenueaccounts[key][2])
			row=row+1
			completerlist.append(self.revenueaccounts[key][2])

		completer = QCompleter(completerlist)	
		self.salesaccount.setCompleter(completer)

		self.receivables=self.requireddata['receivableaccounts']
		self.receivableaccount.addItem("")
		self.receivableaccount.insertItem(0,'-- Create a new account --')
		row=1
		completerlist=[]
		for key in self.receivables:
			self.receivableaccount.insertItem(row,self.receivables[key][2])	
			row=row+1
			completerlist.append(self.receivables[key][2])
		
		completer = QCompleter(completerlist)	
		self.receivableaccount.setCompleter(completer)
			
		billingform.addRow("Customer:",customerlayout)
		billingform.addRow("Billing to:",self.address)
		billingform.addRow("Customer PO No:",self.po_no)
		billingform.addRow("Customer Tax:",self.customertax)


		invoiceform.addRow("Create from:",createfromlayout)
		invoiceform.addRow("Date:",self.dateedit1)
		invoiceform.addRow("Terms:",termlayout)
		invoiceform.addRow("Salesperson:",self.salesperson)
		invoiceform.addRow("Invoice No:",self.invoice_no)
		invoiceform.addRow("Revenue Account:",self.salesaccount)
		invoiceform.addRow("Receivables Account:",self.receivableaccount)

		self.addJournalTable()
		textlayout=QGridLayout()
		buttonlayout=QGridLayout()
		mainlayout.addLayout(self.tablelayout,5)
		mainlayout.addLayout(textlayout,2)
		mainlayout.addLayout(buttonlayout,1)

		self.comment=QTextEdit()
		self.comment.setPlaceholderText('[Enter invoice note]')
		self.nocomment=QTextEdit('Please contact us for more information about payment options.')
		self.privatecomment=QTextEdit()
		self.privatecomment.setPlaceholderText('[Enter internal notes]')
		self.footnote=QTextEdit('Thank you for your business.')

		commentgtab=QTabWidget()
		commentgtab.addTab(self.comment,"Comments")
		commentgtab.addTab(self.privatecomment,"Private comments")
		commentgtab.addTab(self.nocomment,"No comment")
		commentgtab.addTab(self.footnote,"Foot Comments")

		totalform=QFormLayout()
		totalform.setVerticalSpacing(5)

		
		self.subtotal=QLabel(self.amt_placeholder)
		self.tax=QLabel(self.amt_placeholder)
		self.total=QLabel()
		self.total.setText('<b>'+self.amt_placeholder+'</b>')
		totalform.addRow('Subtotal:',self.subtotal)
		totalform.addRow('Tax:',self.tax)
		totalform.addRow('<b>Total</b>',self.total)

		
		textlayout.addWidget(commentgtab,0,0,1,2)
		textlayout.addWidget(QLabel(''),0,2)
		textlayout.addLayout(totalform,0,3)


		self.record=QPushButton('Record')
		self.cancel=QPushButton('Cancel')
		self.help=QPushButton('Help')

		self.record.clicked.connect(self.Save_record)
		self.cancel.clicked.connect(self.close)

		buttonlayout.addWidget(QLabel(),0,0,1,3)
		buttonlayout.addWidget(self.record,0,4)
		buttonlayout.addWidget(self.cancel,0,5)
		buttonlayout.addWidget(self.help,0,6)
		
		
		if self.edit_data !={}:
			edit_data=self.edit_data['0']
			date=edit_data['0'][10]
			year=(date.split('-'))[0]
			month=(date.split('-'))[1]
			day=(date.split('-'))[2]

			self.dateedit1.setDate(QDate(int(year),int(month),int(day)))
			self.customer.setCurrentText(edit_data['0'][6])
			self.address.setText(edit_data['0'][7])
			self.invoice_no.setText(edit_data['0'][9])
			self.salesperson.setCurrentText(edit_data['0'][11])
			self.receivableaccount.setCurrentText(edit_data['0'][1])
			self.salesaccount.setCurrentText(edit_data['0'][4])	

			edit_data=self.edit_data['1']
			self.UpdateRows(edit_data)
			self.comborow=len(edit_data)
			self.unitprice_changed_function(self.comborow-1)
			self.comborow=len(self.edit_data)

			if self.comborow>10:
				self.rowCounts=(self.comborow+5)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()	

	def CustomerWindow(self):
		self.customerlist=Customers(self)
		self.customerlist.show()
	
	def CustomerEdit(self):
		self.customeredit=AddCustomer({})	
		self.customeredit.show()

	def CustomerChange(self,obj):
		
		try:
			index=str(self.customer.currentIndex())
			address=(self.customerdata.get(index))[7]
		except Exception as e:
			address=''
		self.address.setText(address)
	
	def date(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit1 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)	

	def addJournalTable(self):
		JournalHeader=["	Qty 	","			Item   		","    Description     ","    Unit Price     ","    Tax     ","    Total    ",""]
		self.tablelayout=QVBoxLayout()
		self.table =QTableWidget()
		self.table.setColumnCount(7)     #Set three columns
		self.table.setRowCount(self.row)
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		#self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = self.table.horizontalHeader()   
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents) 
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)   
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(5,1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
		
		self.tablelayout.addWidget(self.table)
		
		
		self.table.clicked.connect(self.AddJournals)
		
		self.table.resizeRowsToContents()
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(JournalHeader)
		
		self.table.horizontalHeaderItem(0).setToolTip("Click on any row to add an account")
		self.table.horizontalHeaderItem(1).setToolTip("")
		self.table.horizontalHeaderItem(2).setToolTip("")
		self.table.horizontalHeaderItem(6).setToolTip("Click to delete a row")	
	
	def AddJournals(self,item):
		currRow=(item.row())
		col=item.column()
		if col==0:

			qty=QComboBox()
			qty.setEditable(True)
			item=QComboBox()
			item.setEditable(True)
			description=QComboBox()
			description.setEditable(True)
			unitprice=QLineEdit()
			tax=QComboBox()
			tax.setEditable(True)
			total=QLabel()
			image = ImageWidget('image/icon/clear.png', self)
			unitprice.setPlaceholderText(self.amt_placeholder)
			total.setText(self.amt_placeholder)
			
			if self.comborow not in self.widgetDic:
				widgetList=[]
				widgetList.append(qty)
				widgetList.append(item)
				widgetList.append(description)
				widgetList.append(unitprice)
				widgetList.append(tax)
				widgetList.append(total)
				self.widgetDic[self.comborow]=widgetList				
				(self.widgetDic[self.comborow][3]).textChanged.connect(partial(self.unitprice_changed_function,self.comborow))
				(self.widgetDic[self.comborow][0]).currentTextChanged.connect(partial(self.unitprice_changed_function,self.comborow))
				
			self.table.setCellWidget(self.comborow,0,qty)
			self.table.setCellWidget(self.comborow,1,item)
			self.table.setCellWidget(self.comborow,2, description)
			self.table.setCellWidget(self.comborow,3,unitprice)
			self.table.setCellWidget(self.comborow,4,tax)
			self.table.setCellWidget(self.comborow,5, total)
			self.table.setCellWidget(self.comborow, 6, image)
			self.comborow=self.comborow+1
			
			if self.comborow==self.rowCounts:
				self.rowCounts+5
				self.rowCounts=(self.rowCounts+5)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()
		
		if col==6:
			self.DeleteRow(currRow)

	def DeleteRow(self,row):
		if row in self.widgetDic.keys():

			self.widgetDic.pop(row)
			invoicedata={}
			index=0
			for key in sorted(self.widgetDic):
				data_list=[]
				for col in range(6):
					if col==0:	
						data_list.append((self.widgetDic[key][0]).currentText())
					if col==1:	
						data_list.append((self.widgetDic[key][1]).currentText())
					if col==2:	
						data_list.append((self.widgetDic[key][2]).currentText())	
					if col==3:	
						data_list.append((self.widgetDic[key][3]).text())
					if col==4:	
						data_list.append((self.widgetDic[key][4]).currentText())
					if col==5:	
						data_list.append((self.widgetDic[key][5]).text())
					
											
				invoicedata[index]=data_list
				index=index+1
				
			self.UpdateRows(invoicedata)
			
			self.comborow=self.comborow-1
			if self.rowCounts>10:
				self.rowCounts=(self.rowCounts-1)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()

			self.unitprice_changed_function(row-1)
	
	def UpdateRows(self,invoicedata):
		self.table.clearContents()	
		self.widgetDic={}
		
		for keys in sorted(invoicedata):
			try:
				widgetList=[]
				qty=QComboBox()
				qty.setEditable(True)
				item=QComboBox()
				item.setEditable(True)
				description=QComboBox()
				description.setEditable(True)
				unitprice=QLineEdit()
				tax=QComboBox()
				tax.setEditable(True)
				total=QLabel()

				unitprice.setPlaceholderText(self.amt_placeholder)
	
				qty.setCurrentText(invoicedata[keys][0])
				item.setCurrentText(str(invoicedata[keys][1]))
				description.setCurrentText(invoicedata[keys][2])
				unitprice.setText(invoicedata[keys][3])
				tax.setCurrentText(str(invoicedata[keys][4]))
				total.setText(invoicedata[keys][5])

				self.table.setCellWidget(int(keys),0,qty)
				self.table.setCellWidget(int(keys),1,item)
				self.table.setCellWidget(int(keys),2, description)
				self.table.setCellWidget(int(keys),3,unitprice)
				self.table.setCellWidget(int(keys),4,tax)
				self.table.setCellWidget(int(keys),5, total)
				image = ImageWidget('image/icon/clear.png', self)
				self.table.setCellWidget(int(keys), 6, image)


				widgetList.append(qty)
				widgetList.append(item)
				widgetList.append(description)
				widgetList.append(unitprice)
				widgetList.append(tax)
				widgetList.append(total)
				
				self.widgetDic[int(keys)]=widgetList
			
				unitprice.textChanged.connect(partial(self.unitprice_changed_function,int(keys)))
				qty.currentTextChanged.connect(partial(self.unitprice_changed_function,int(keys)))

				
			except Exception as e:
				print(e)

	def unitprice_changed_function(self,currrow):
		
		if currrow==-1:
			return False

		try:
			float((self.widgetDic[currrow][0]).currentText())
		except Exception as e:
				(self.widgetDic[currrow][0]).setCurrentText('')
		try:
			float((self.widgetDic[currrow][3]).text())
		except Exception as e:
				(self.widgetDic[currrow][3]).setText('')		
				
		try:
			qty=(self.widgetDic[currrow][0]).currentText()	
			unitprice=(self.widgetDic[currrow][3]).text()
			if qty=="" or unitprice=="":
				return False	
			total_=float(qty)*float(unitprice)	
			(self.widgetDic[currrow][5]).setText(format_currency(total_,'NGN', locale='en_US'))
			total=0
			for row in self.widgetDic:
				widget=self.widgetDic[row]
				if (widget[3]).text()=="" or (widget[3]).text()=="":
					return False
				qty=(widget[0]).currentText()
				unitprice=(widget[3]).text()
				total=total+float(qty)*float(unitprice)
			self.subtotal.setText(format_currency(total,'NGN', locale='en_US'))
			#self.tax=QLabel(self.amt_placeholder)
			self.total.setText('<b>'+format_currency(total,'NGN', locale='en_US')+'</b>')
		except Exception as e:
			if (self.widgetDic[currrow][5]).text()=="":
				return False
			val1=(((self.widgetDic[currrow][5]).text()).split('₦'))[1]
			val2=((((self.total.text()).split('₦'))[1]).split('</b>'))[0]
			val=float(val2)-float(val1)
			(self.widgetDic[currrow][5]).clear()
			self.subtotal.setText(format_currency(val,'NGN', locale='en_US'))
			#self.tax=QLabel(self.amt_placeholder)
			self.total.setText('<b>'+format_currency(val,'NGN', locale='en_US')+'</b>')

			
		
	def Save_record(self):
					
		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)

		date2=self.dateedit1.date()
		year2=str(date2.year())
		day2=str(date2.day()) if len(str(date2.day()))==2 else '0'+str(date2.day())
		month2=str(date2.month()) if len(str(date2.month()))==2 else '0'+str(date2.month())
		duedate=(year2+'-'+month2+'-'+day2)

		userdb=open("db/user.json", "r")
		user=json.load(userdb)		

		journaltype="Sales"
		address=(self.address.toPlainText())
		customer=self.customer.currentText()
		memo="Sales;"+customer		
		ref="SLS[AUTO]"

		revenueaccounts=self.salesaccount.currentText()
		receivables=self.receivableaccount.currentText()
		customerdata=self.customer.currentText()
		if revenueaccounts=="" or receivables=="" or customerdata=="":
			return False

		salesaccount=self.revenueaccounts[str(self.salesaccount.currentIndex()-1)]
		receivableaccount=self.receivables[str(self.receivableaccount.currentIndex()-1)]
		customer=self.customerdata[str(self.customer.currentIndex())]
				
		invoiceDic={}
		total=0
		subtotal=[]
		for row in self.widgetDic:
			amnt=(self.widgetDic[row][5]).text()
			amnt=amnt.split('₦')
			invoicelist=[]
			invoicelist.append(receivableaccount[2])
			invoicelist.append(customer[8])
			invoicelist.append(customer[0])
			invoicelist.append(address)
			invoicelist.append(ref)
			invoicelist.append(self.invoice_no.text())
			#invoicelist.append(int(self.requireddata['invoiceid'])+counts)
			invoicelist.append(date)
			invoicelist.append(duedate)
			invoicelist.append(self.salesperson.currentText())
			invoicelist.append((self.widgetDic[row][0]).currentText())
			invoicelist.append((self.widgetDic[row][1]).currentText())
			invoicelist.append((self.widgetDic[row][2]).currentText())
			invoicelist.append((self.widgetDic[row][3]).text())
			invoicelist.append(str(float(parse_decimal(amnt[1],locale='en_US'))))
			invoicelist.append("Not Paid")
			invoicelist.append(user)
			invoicelist.append(salesaccount[2])
			invoiceDic[row]=invoicelist
			total=total+float(parse_decimal(amnt[1],locale='en_US'))
			subtotal.append(float(parse_decimal(amnt[1],locale='en_US')))
		
		postDic={}
		
		rw=0
		for sub in subtotal:
			postList=[]
			postList.append(salesaccount[2])			
			postList.append(str(sub))
			postList.append('Credit')	
			postList.append(ref)
			postList.append(journaltype)
			postList.append(memo)
			postList.append(date)
			postList.append(user)
			postDic[rw]=postList
			rw=rw+1

		postList=[]	
		postList.append(receivableaccount[2])			
		postList.append(str(total))
		postList.append('Debit')	
		postList.append(ref)
		postList.append(journaltype)
		postList.append(memo)
		postList.append(date)
		postList.append(user)
		postList.append(invoiceDic)
		postDic[rw]=postList
		
		
		postDic=json.dumps(postDic)
		postDic=base64.b64encode(postDic.encode())
		
		data = QtCore.QByteArray()
		data.append("action=postjournal&")
		data.append("invoice=invoice&")
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

	        	self.invoice_no.setText(str(int(self.invoice_no.text())+1))
	        	
	        
	        result = self.MessageBox.exec_()
	        if result==self.MessageBox.Ok:
	        	pass
	        
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "\n {}	 \n".format(reply.errorString()))


		
		
				

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Invoice({})
	ex.show()
	sys.exit(app.exec_())		