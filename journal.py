from PyQt5.QtWidgets import QMainWindow,QDialog,QDialogButtonBox,QAction,QTabWidget,QTableWidgetItem,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtGui import QIcon,QPixmap
from loader import overlay
from PyQt5.QtCore import Qt, QDate,QDateTime,pyqtProperty
import sys,json
from addjournal import AddJournal
from ledger import Ledger
from jinja2 import Template
from functools import partial


class Journal(QMainWindow):
	def __init__(self, parent=None):
		super(Journal, self).__init__(parent)
		self.title = 'View Journal'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		#self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)
		#self.setWindowModality(Qt.ApplicationModal)

		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))
				
		self.initmenu()
		self.JournalContent()
		#self.setLayout(self.widget)
		self.setCentralWidget(self.widget)
		
	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		Journal = mainMenu.addMenu('Journal')
		homeMenu = mainMenu.addMenu('Report')
		homeMenu = mainMenu.addMenu('Help')
		 
		NewEntryButton = QAction(QIcon('exit24.png'), 'New Entry                    ', self)
		NewEntryButton.setShortcut('Ctrl+N')
		NewEntryButton.setStatusTip('New Journal')
		NewEntryButton.triggered.connect(self.CreateNewJournal)

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

		self.addaccount= QAction(QIcon('image/icon/add.ico'), 'Add Account', self)
		self.edit= QAction(QIcon('image/icon/edit.ico'), 'Edit Account', self)
		self.delete= QAction(QIcon('image/icon/delete.ico'), 'Delete Account', self)
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview Journal', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print Journal', self)
		self.excel= QAction(QIcon('image/icon/excel.png'), 'View in Excel', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Journal', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Journal', self)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		self.preview.setDisabled(True)
		self.print.setDisabled(True)
		self.excel.setDisabled(True)
		self.excel.setDisabled(True)
		self.save.setDisabled(True)
		self.mail.setDisabled(True)
		
		toolbar.addAction(self.addaccount)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()

		toolbar.addAction(self.preview)
		toolbar.addAction(self.print)
		toolbar.addAction(self.excel)
		toolbar.addAction(self.save)
		toolbar.addAction(self.mail)
		
		self.addaccount.triggered.connect(self.CreateNewJournal)
		self.edit.triggered.connect(self.Edit)
		self.delete.triggered.connect(self.Delete)
		self.preview.triggered.connect(self.Preview)
		self.print.triggered.connect(self.Print)
		self.excel.triggered.connect(self.ViewInExcel)
		self.save.triggered.connect(self.Save)
		self.mail.triggered.connect(self.Mail)		
	
	def ViewInExcel(self):
		import pandas as pd
		import xlsxwriter
		from os.path import expanduser

		home=expanduser("~")
		table=json.load(open("db/print_jounal.json", "r"))
		workbook = xlsxwriter.Workbook('{}/Documents/journal.xlsx'.format(home))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1, 'align':'right','num_format': '#,##.00'})

		worksheet.set_column(0, 4, 12)
		worksheet.set_column(5, 5, 35)
		worksheet.set_column(6, 7, 15)

		#pd=(pd.read_html(table))[0]
		#pd=pd.fillna('')
		
		journaltypelist=['All',"General","Payments","Sales","Receipts","Purchases"]
		index=self.tabs.currentIndex()
		self.journaltype=journaltypelist[index]

		worksheet.insert_image(1, 4,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 2,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 2,'{journaltype} Journal Posted from {date1} to {date2}'.format(journaltype=self.journaltype,date1=self.date1,date2=self.date2),bold)
		row_end1=0
		row_end2=0

		data = table[0]
		cols =range(8)
		for row in sorted(data):
			for col in cols:
				if col>=6:
					worksheet.write(int(row)+7, col,data[row][col],money_format)
				else:
					worksheet.write(int(row)+7, col,data[row][col],format1)

				
		
		import os,time
		time.sleep(2)
		os.system('start EXCEL.EXE {}/Documents/journal.xlsx'.format(home))
		
		workbook.close()		
					

	def CreateNewJournal(self):
		AddJournal(self,{},self.date1,self.date2).exec_()
		
	
	def Edit(self):
		journaltypelist=['all',"General","Payments","Sales","Receipts","Purchases"]
		index=self.tabs.currentIndex()
		self.delref=self.deljournal[self.delkey]
		self.JournalData(journaltypelist[index],self.date1,self.date2,'Edit',self.delref)
		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
	
	def Delete(self):
		self.delref=self.deljournal[self.delkey]
		
		self.dialog=QDialog(self)
		#self.dialog.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)
		self.dialog.setWindowTitle("Delete Journal")
		layout = QGridLayout()
		self.dialog.setLayout(layout)
		layout.addWidget(QLabel("\nAre you sure you want to delete selected journal entries {} at row {}	\n\n  ".\
			format(self.delref,self.delkey+1)))

		self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		self.buttonbox.button(QDialogButtonBox.Ok).setText("Yes, Delete!")
		self.buttonbox.accepted.connect(self.DeleteRow)
		self.buttonbox.rejected.connect(self.dialog.close)
		layout.addWidget(self.buttonbox)
		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		self.dialog.exec_()
	
	def DeleteRow(self):
		index=self.tabs.currentIndex()
		self.TabTable(self.tabs.currentIndex())
		journaltypelist=['all',"General","Payments","Sales","Receipts","Purchases"]
		self.JournalData(journaltypelist[index],self.date1,self.date2,'Delete',self.delref)
		self.dialog.close()
			
	def Preview(self):
		loaddata=open("db/print_jounal.json", "r")
		self.printdata=json.load(loaddata)
		self.handlePreview()
	def handlePreview(self):
		dialog = QtPrintSupport.QPrintPreviewDialog()
		dialog.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)
		dialog.paintRequested.connect(self.handle_paint_request)
		dialog.exec_()	

	def handle_print(self):
		printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
		dialog = QtPrintSupport.QPrintDialog(printer, self)
		if dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
		    self.handle_paint_request(printer)

	def handle_paint_request(self, printer):
		document=QtGui.QTextDocument()
		cursor=QtGui.QTextCursor(document)	

		headers =["Date","Journal","Ref","Narration","Account","Account Description","Debit Amount","Credit Amount"]
		if self.printdata=={}:
			journal={}
			total=[]
		else:
			journal=self.printdata[0]
			total=self.printdata[1]
		rowlenght=len((journal).keys())
		rows=[]
		for key in range(rowlenght):
			rows.append(str(key))
		
		journaltypelist=['All',"General","Payments","Sales","Receipts","Purchases"]
		index=self.tabs.currentIndex()
		self.journaltype=journaltypelist[index]
		#print(journal)
		table = """
		<style>
		table {
		font-family: arial, sans-serif;
		border-collapse: collapse;
		width: 100%;
		}

		td, th {
		border: 1px solid black;
		text-align: center;
		padding: 2px;
		}
		</style>
		<body>
		<div style="text-align:center">
		<img source="image/report.JPG">
		   <p style="font-weight: bold;font-size:18px;">FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
      	<p style="font-weight: bold;font-size:18px;">{{journaltype}} Journal Posted from {{date1}} to {{date2}}<p/>
      	</div>
		<table border=".3" cellSpacing="0" width="100%">
		<tr>{% for header in headers %}<th>{{header}}</th>{% endfor %}</tr>
		{% for row in rows %}<tr>
		{% for element in (journal[row][:-1]) %}
		{% if  (journal[row][:-1]).index(element)>5 %}
		<td style="text-align:right">
		{{element}}
		</td>
		{% else %}
		<td style="text-align:left">
		{{element}}
		</td>
		{% endif %}

		{% endfor %}
		</tr>{% endfor %}
		<tr><td></td><td></td><td></td><td></td><td></td><td></td>
		{% for element in total %}<td>{{element}}</td>{% endfor %}</tr>
		</table>
		</body>
		"""
		#(journal[row][0:3]+ journal[row][4:-1])
		cursor.insertHtml(Template(table).render(headers=headers,rows=rows, journal=journal,total=total,journaltype=self.journaltype,date1=self.date1,date2=self.date2))	
		document.print_(printer)		
		
		
	def Print(self):
		self.handle_print()
	def Save(self):
		pass	
	def Mail(self):
		pass			

		
	def JournalContent(self):
		self.widget=QWidget()
		self.currentTabDic={}
		self.delref=self.memo_=''
		self.account_search='All Accounts'
		self.currdata={}
		self.mainlayout=QVBoxLayout()
		self.gridLayout=QGridLayout()
		self.tabs = QTabWidget()

		self.overlay = overlay(self.tabs)
		#self.overlay.hide()
		
		self.mainlayout.addLayout(self.gridLayout,1)
		self.mainlayout.addWidget(self.tabs,18)
		self.widget.setLayout(self.mainlayout)

		requireddata=open("db/accounts.json", "r")
		self.requireddata=json.load(requireddata)
		
		reflineedit=QLineEdit()
		reflineedit.textChanged.connect(self.SearchRef)

		lab1=QLabel('Period:')
		self.comboboxPeriod = QComboBox()
		#comboboxPeriod.setMinimumHeight(5)
		lab2=QLabel('Start:')
		Startdate = QCalendarWidget()
		lab3=QLabel('End:')
		Enddate = QCalendarWidget()
		lab4=QLabel('Account:')
		self.comboboxAccount = QComboBox()
		self.comboboxAccount.setObjectName('comboboxAccount')
		lab5=QLabel('Ref:')
		
		
		AccountsList=self.requireddata
		AccountsList.sort()
		self.comboboxAccount.addItem("All Accounts")
		self.comboboxAccount.addItems(AccountsList)
		self.comboboxAccount.currentTextChanged.connect(self.comboboxAccount_changed)

		date = QDate()
		currentdate=date.currentDate()
		dateLayout1 = QGridLayout()
		dateLayout1.setContentsMargins(0, 0, 0, 0)
		self.dateedit1 = QDateEdit()
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)
		dateLayout1.addWidget(self.dateedit1, 0, 0)
		
		dateLayout2 = QGridLayout()
		dateLayout2.setContentsMargins(0, 0, 0, 0)
		self.dateedit2 = QDateEdit()
		self.dateedit2.setDate(currentdate)
		self.dateedit2.setDisplayFormat('dd/MM/yyyy')
		self.dateedit2.setCalendarPopup(True)
		dateLayout2.addWidget(self.dateedit2, 0, 0)

		self.dateedit1.dateChanged.connect(self.DateChange)
		self.dateedit2.dateChanged.connect(self.DateChange)
		
		self.gridLayout.addWidget(lab1,0,0)
		self.gridLayout.addWidget(self.comboboxPeriod,0,1)
		self.gridLayout.addWidget(lab2,0,2)
		self.gridLayout.addLayout(dateLayout1,0,3)
		self.gridLayout.addWidget(lab3,0,4)
		self.gridLayout.addLayout(dateLayout2,0,5)
		self.gridLayout.addWidget(lab4,0,6)
		self.gridLayout.addWidget(self.comboboxAccount,0,7)
		self.gridLayout.addWidget(lab5,0,8)
		self.gridLayout.addWidget(reflineedit,0,9,1,2)

		self.allTab = QWidget()
		self.alllayout=QVBoxLayout()
		self.allTab.setLayout(self.alllayout)
		self.allTab.setStatusTip("This table contains all accounts journal")
		self.generalTab = QWidget()
		self.generallayout=QVBoxLayout()
		self.generalTab.setLayout(self.generallayout)
		self.generalTab.setStatusTip("This table contains general accounts journal")
		self.paymentTab = QWidget()
		self.paymentlayout=QVBoxLayout()
		self.paymentTab.setLayout(self.paymentlayout)
		self.paymentTab.setStatusTip("This table contains payment accounts journal")
		self.salesTab = QWidget()
		self.saleslayout=QVBoxLayout()
		self.salesTab.setLayout(self.saleslayout)
		self.salesTab.setStatusTip("This table contains sales accounts journal")
		self.receiptTab = QWidget()
		self.receiptlayout=QVBoxLayout()
		self.receiptTab.setLayout(self.receiptlayout)
		self.receiptTab.setStatusTip("This table contains receipt accounts journal")
		self.purchasesTab = QWidget()
		self.purchaseslayout=QVBoxLayout()
		self.purchasesTab.setLayout(self.purchaseslayout)
		self.purchasesTab.setStatusTip("This table contains purchses accounts journal")

		self.tabs.addTab(self.allTab,"All")
		self.tabs.addTab(self.generalTab,"General")
		self.tabs.addTab(self.paymentTab,"Payments")
		self.tabs.addTab(self.salesTab,"Sales")
		self.tabs.addTab(self.receiptTab,"Receipts")
		self.tabs.addTab(self.purchasesTab,"Purchases")

		self.comboboxPeriod.currentTextChanged.connect(self.comboboxPeriod_changed)
		Period=["Custom Period","Today","Yesterday","This Week","Last Week","This Month","Last Month","This Year"]
		self.comboboxPeriod.addItems(Period)

		self.tabs.currentChanged.connect(self.currentTab)

		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.date1=self.FormatDate(date1)
		self.date2=self.FormatDate(date2)
		
	def TabTable(self, tabscurrentIndex):
		
		#add each tab tablewidget to their respective layout and the table to  currentTabDic 
		#if tabscurrentIndex not in self.currentTabDic:
		if tabscurrentIndex  in self.currentTabDic:
			self.alllayout.removeWidget(self.currentTabDic[tabscurrentIndex])
			self.generallayout.removeWidget(self.currentTabDic[tabscurrentIndex])
			self.paymentlayout.removeWidget(self.currentTabDic[tabscurrentIndex])
			self.saleslayout.removeWidget(self.currentTabDic[tabscurrentIndex])
			self.receiptlayout.removeWidget(self.currentTabDic[tabscurrentIndex])
			self.purchaseslayout.removeWidget(self.currentTabDic[tabscurrentIndex])

			self.currentTabDic.pop(tabscurrentIndex)

		if tabscurrentIndex not  in self.currentTabDic:
			#print('Not in Dic')
			JournalHeader=["Date","Journal","Ref","Description","Account","Account Description","Debit Amount","Credit Amount","User"]
			self.currNoRow=22			
			self.table =QTableWidget()
			self.table.setColumnCount(len(JournalHeader))     #Set three columns
			self.table.setRowCount(self.currNoRow)
			
			self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
			header = self.table.horizontalHeader()
			#for index in JournalHeader:
			header.setSectionResizeMode(JournalHeader.index("Description"),  QtWidgets.QHeaderView.ResizeToContents)
			header.setSectionResizeMode(JournalHeader.index("Account Description"),  QtWidgets.QHeaderView.ResizeToContents)
			header.setSectionResizeMode(JournalHeader.index("Debit Amount"),  QtWidgets.QHeaderView.ResizeToContents)
			header.setSectionResizeMode(JournalHeader.index("Credit Amount"),  QtWidgets.QHeaderView.ResizeToContents)
			
			self.table.resizeColumnsToContents()
			self.table.resizeRowsToContents()
			self.table.setSelectionMode(QAbstractItemView.MultiSelection)
			self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
			
			self.table.setShowGrid(True)
			self.table.setHorizontalHeaderLabels(JournalHeader)
			for Header in JournalHeader:
				self.table.horizontalHeaderItem(JournalHeader.index(Header)).setToolTip("{}".format(Header))
				if Header=="Date":
					self.table.horizontalHeaderItem(JournalHeader.index(Header)).setTextAlignment(Qt.AlignLeft)
				if Header=="User":
					self.table.horizontalHeaderItem(JournalHeader.index(Header)).setTextAlignment(Qt.AlignCenter)
		
			self.currentTabDic[tabscurrentIndex]=self.table

		if tabscurrentIndex==0:
			self.alllayout.addWidget(self.table)
		if tabscurrentIndex==1:
			self.generallayout.addWidget(self.table)
		if tabscurrentIndex==2:
			self.paymentlayout.addWidget(self.table)
		if tabscurrentIndex==3:
			self.saleslayout.addWidget(self.table)
		if tabscurrentIndex==4:
			self.receiptlayout.addWidget(self.table)
		if tabscurrentIndex==5:
			self.purchaseslayout.addWidget(self.table)
						
	def JournalData(self,journaltype,date1,date2,delete_edit,ref):
		self.overlay.setVisible(True)
		#print(journaltype,date1,date2,delete_edit,ref)
		account_search=self.comboboxAccount.currentText()
		account_search=account_search.split(' - ')
		self.account_search=account_search[0]
		data = QtCore.QByteArray()

		data.append("action=fetchjournal&")
		data.append("journaltype={}&".format(journaltype))
		data.append("date1={}&".format(date1))
		data.append("date2={}&".format(date2))
		data.append("account={}&".format(self.account_search))
		data.append("option={}&".format(delete_edit))
		data.append("memo={}&".format(self.memo_))
		data.append("ref={}".format(ref))
		
		url = "http://{}:5000/fetchjournal".format(self.ip)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(partial(self.handleResponse,delete_edit))
		self.nam.post(req, data)

	def handleResponse(self,delete_edit, reply):
		self.tabledata={}
		data_total={}
		er = reply.error()	
		if er == QtNetwork.QNetworkReply.NoError:
			bytes_string = reply.readAll()
			data_total = json.loads(str(bytes_string, 'utf-8'))
			if delete_edit=='Edit':
				self.addjournal=AddJournal(self,data_total,self.date1,self.date2)
				self.addjournal.exec_()
				return False
			self.tabledata=data_total[0]
			#print(self.tabledata)
			rowNumber=len(self.tabledata)
			self.table.setRowCount(rowNumber) if rowNumber > self.currNoRow else self.table.setRowCount(self.currNoRow) 
			#self.table.resizeColumnsToContents()
			#self.table.resizeRowsToContents()
			#write to table contents
			cols=9
			for row in self.tabledata:
				for col in range(cols):
					item=QTableWidgetItem(self.tabledata[row][col])
					if col>=6:
						amnt=QLineEdit(self.tabledata[row][col])
						amnt.setAlignment(Qt.AlignRight)
						amnt.setStyleSheet("border:none;font-size:13px;")
						self.table.setCellWidget(int(row),col, amnt)
					else:
						self.table.setItem(int(row),col, item)
			
			self.overlay.setVisible(False)
		else:
			self.overlay.setVisible(False)
			QMessageBox.critical(self, 'Database Connection  ', "\n{} 	 \n".format(reply.errorString()))
			
		self.table.clicked.connect(self.TableAction)	
		json.dump(data_total, open("db/print_jounal.json", "w"))	
		#print(data_total)
		if self.tabledata != {}:
			self.preview.setEnabled(True)
			self.print.setEnabled(True)
			self.excel.setEnabled(True)
			self.save.setEnabled(True)
			self.mail.setEnabled(True)
		

	def currentTab(self,index):	
		#self.tabs.removeTab(index)						
		if index==0:
			self.JournalData('all',self.date1,self.date2,'No','')
		if index==1:
			self.JournalData('General',self.date1,self.date2,'No','')
		if index==2:
			self.JournalData('Payments',self.date1,self.date2,'No','')
		if index==3:
			self.JournalData('Sales',self.date1,self.date2,'No','')
		if index==4:
			self.JournalData('Receipts',self.date1,self.date2,'No','')
		if index==5:
			self.JournalData('Purchases',self.date1,self.date2,'No','')
					
		self.TabTable(index)# call this fn to create new table if not yet exists in self.currentTabDic	
		currentTabdb=open("db/journaltabs.json", "w")
		json.dump(index, currentTabdb)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		self.preview.setDisabled(True)
		self.print.setDisabled(True)
		self.excel.setDisabled(True)
		self.save.setDisabled(True)
		self.mail.setDisabled(True)

	def TableAction(self,item):
		if self.tabledata=={}:
			return False
		row=item.row()
		self.deljournal={}
		self.delkey= row
		
		#for row in self.table.selectionModel().selectedRows():
		if self.tabledata.get(str(row), '') is not '':
			self.deljournal[row]=self.tabledata[str(row)][2]
			self.memo_=self.tabledata[str(row)][3]	
			print(self.memo_)
		self.edit.setEnabled(True)
		self.delete.setEnabled(True)

	def FormatDate(self,date1):
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)
		return date	
	def comboboxPeriod_changed(self,obj):
		#self.table.removeRow(0)
		#self.JournalData('all',self.date1,self.date2)
		date = QDate()
		currentdate=date.currentDate()
		year=currentdate.year()
		month=currentdate.month()
		day=currentdate.day()
		

		if obj=="Custom Period":
			self.dateedit1.setEnabled(True)
			self.dateedit2.setEnabled(True)

	
		if obj=="Today":
			self.dateedit1.setDate(currentdate)
			self.dateedit2.setDate(currentdate)
			self.dateedit1.setEnabled(False)
			self.dateedit2.setEnabled(False)
			
		if obj== "Yesterday":
			self.dateedit1.setDate(currentdate.addDays(-1))
			self.dateedit2.setDate(currentdate.addDays(-1))
			self.dateedit1.setEnabled(False)
			self.dateedit2.setEnabled(False)
			
		
		if obj=="This Week":
			day_of_week=currentdate.dayOfWeek()
			if day_of_week==1:
				self.dateedit1.setDate(currentdate.addDays(-1))
				self.dateedit2.setDate(currentdate.addDays(5))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==2:
				self.dateedit1.setDate(currentdate.addDays(-2))
				self.dateedit2.setDate(currentdate.addDays(4))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==3:
				self.dateedit1.setDate(currentdate.addDays(-3))
				self.dateedit2.setDate(currentdate.addDays(3))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==4:
				self.dateedit1.setDate(currentdate.addDays(-4))
				self.dateedit2.setDate(currentdate.addDays(2))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)	
			if day_of_week==5:
				self.dateedit1.setDate(currentdate.addDays(-5))
				self.dateedit2.setDate(currentdate.addDays(1))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==6:
				self.dateedit1.setDate(currentdate.addDays(-6))
				self.dateedit2.setDate(currentdate.addDays(0))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==7:
				self.dateedit1.setDate(currentdate.addDays(0))
				self.dateedit2.setDate(currentdate.addDays(6))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)			
		if obj=="Last Week":
			day_of_week=currentdate.dayOfWeek()
			if day_of_week==1:
				self.dateedit1.setDate(currentdate.addDays(-1-7))
				self.dateedit2.setDate(currentdate.addDays(5-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==2:
				self.dateedit1.setDate(currentdate.addDays(-2-7))
				self.dateedit2.setDate(currentdate.addDays(4-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==3:
				self.dateedit1.setDate(currentdate.addDays(-3-7))
				self.dateedit2.setDate(currentdate.addDays(3-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==4:
				self.dateedit1.setDate(currentdate.addDays(-4-7))
				self.dateedit2.setDate(currentdate.addDays(2-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)	
			if day_of_week==5:
				self.dateedit1.setDate(currentdate.addDays(-5-7))
				self.dateedit2.setDate(currentdate.addDays(1-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==6:
				self.dateedit1.setDate(currentdate.addDays(-6-7))
				self.dateedit2.setDate(currentdate.addDays(0-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			if day_of_week==7:
				self.dateedit1.setDate(currentdate.addDays(0-7))
				self.dateedit2.setDate(currentdate.addDays(6-7))
				self.dateedit1.setEnabled(False)
				self.dateedit2.setEnabled(False)
			self.dateedit1.setEnabled(False)
			self.dateedit2.setEnabled(False)	
		if obj=="This Month":
			days_in_month=currentdate.daysInMonth()
			begin_date=QDate(year, month, 1)
			end_date=QDate(year, month, days_in_month)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)
			self.dateedit1.setEnabled(False)
			self.dateedit2.setEnabled(False)	
		if obj=="Last Month":
			prev_date=currentdate.addMonths(-1)
			year=prev_date.year()
			month=prev_date.month()
			days=prev_date.daysInMonth()
			begin_date=QDate(year,month,1)
			end_date=QDate(year,month,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)
			self.dateedit1.setEnabled(False)
			self.dateedit2.setEnabled(False)	
		if obj=="This Year":
			days=QDate(year,12,1).daysInMonth()
			begin_date=QDate(year,1,1)
			end_date=QDate(year,12,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)
			self.dateedit1.setEnabled(False)
			self.dateedit2.setEnabled(False)	
			
		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		self.date1=(year1+'-'+month1+'-'+day1)
		
		date2=self.dateedit2.date()
		year2=str(date2.year())
		day2=str(date2.day()) if len(str(date2.day()))==2 else '0'+str(date2.day())
		month2=str(date2.month()) if len(str(date2.month()))==2 else '0'+str(date2.month())
		self.date2=(year2+'-'+month2+'-'+day2)

		currentTab=self.tabs.currentIndex()
		self.currentTab(currentTab)
	
	def DateChange(self):
		if self.comboboxPeriod.currentText()=="Custom Period":
			date1=self.dateedit1.date()
			year1=str(date1.year())
			day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
			month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
			self.date1=(year1+'-'+month1+'-'+day1)
			
			date2=self.dateedit2.date()
			year2=str(date2.year())
			day2=str(date2.day()) if len(str(date2.day()))==2 else '0'+str(date2.day())
			month2=str(date2.month()) if len(str(date2.month()))==2 else '0'+str(date2.month())
			self.date2=(year2+'-'+month2+'-'+day2)
			currentTab=self.tabs.currentIndex()
			self.currentTab(currentTab)

	def comboboxAccount_changed(self, account):
		currentTab=self.tabs.currentIndex()
		self.currentTab(currentTab)

	def SearchRef(self,ref):
		self.delref=ref	
		index=self.tabs.currentIndex()
		journaltypelist=['all',"General","Payments","Sales","Receipts","Purchases"]
		self.TabTable(self.tabs.currentIndex())
		self.JournalData(journaltypelist[index],self.date1,self.date2,'No',self.delref)

	def resizeEvent(self,event):
		self.overlay.resize(event.size())
		event.accept()
        

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Journal()
	ex.show()
	sys.exit(app.exec_())