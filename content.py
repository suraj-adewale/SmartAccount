from PyQt5.QtWidgets import QMainWindow,QCompleter, QApplication,QDialog,QDialogButtonBox, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,QMenuBar, QMenu,\
 QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5.QtGui import QIcon,QPixmap
from loader import overlay
from PyQt5.QtCore import QDate,QTimer,pyqtSlot,pyqtSignal,Qt,QRunnable, QThreadPool
from PyQt5 import QtCore, QtNetwork,QtWidgets
from journal import Journal
from charts import AccountsChart
from payable import Payable
from paypayable import PayPayable
from accountspayable import AccountsPayable
from suppliers import Suppliers
from addjournal import  AddJournal
from  trialbal import TrialBalance
from balsheet import BalanceSheet
from performance import FinPerformance
from paymentpurchase import PaymentPurchase
from receiptdeposit import ReceiptDeposit
from ledger import Ledger
from addinvoice import Invoice
from invoicepayment import InvoivePayment
from invoice import InvoicePayable
from customers import Customers
from settings import Settings
from register import Register
from addaccount import  AddAccount
from transfer import TransferAccount
from backup import BackUp
from reinvoice import InvoiceRe
from enquiry import AccountsEnquiry
from income import Income
from reinvoicepayment import InvoicePaymentRe
from functools import partial
from server.routing import StartServer
import sys,json,base64,time,random


class ClickableLabel(QLabel):
	clicked=pyqtSignal()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton: self.clicked.emit()

class Main(QMainWindow):
	
	def __init__(self,mail,usertype, parent=None):
		super(Main, self).__init__(parent)
		self.threadpool = QThreadPool()
		#print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
		#self.setWindowTitle('Icon')
		self.title = 'Main'
		self.left = 180
		self.top = 50
		self.width = 1000
		self.height = 580
		self.useremail=mail
		self.usertype=usertype

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.setStatusTip("SmartAccount V 2.0.1 Sadel Technology")
		
		self.initmenu()	
		self.Content()
		#self.widget.loader="ajax-loader.gif"
		self.overlay = overlay(self.widget)
		self.showMaximized()
		#self.overlay.hide()
		self.setCentralWidget(self.widget)
		self.show()

		if usertype=='Administrator':
			self.ip='localhost'	
			self.StartServerConnection()
			ran=random.randint(0,3)
			self.DURATION=[60,120,180,300][ran]
			self.qtimer=QTimer(self)
			self.qtimer.timeout.connect(self.timer_fn)
			#self.qtimer.start(1000)
		if usertype=='User':
			ipaddress=open("db/ipaddress.json", "r")
			self.ip=json.load(ipaddress)
			self.RequiredData('required','date1','date2','requireddata')

		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
	
	def keyPressEvent(self, e):
		#print(e.key())
		pass
		
	def initmenu(self): 
		mainMenu = self.menuBar()
		Accountmenu = mainMenu.addMenu('Account')
		Sales = mainMenu.addMenu('Sales')
		Purchases = mainMenu.addMenu('Purchases')
		Transaction = mainMenu.addMenu('Transaction')
		Report = mainMenu.addMenu('Report')
		View = mainMenu.addMenu('View')
		Settings = mainMenu.addMenu('Settings')
			 
		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		Accountmenu.addAction(exitButton)
		
		newinvoice=QAction('New Invoice', self)
		newinvoice.setShortcut('Ctrl+N')
		Sales.addAction(newinvoice)
		customerpayment=QAction('Customers Payment', self)
		customerpayment.setShortcut('Ctrl+P')
		Sales.addAction(customerpayment)
		invoicelist=QAction('Open Invoices List', self)
		invoicelist.setShortcut('Ctrl+Y')
		Sales.addAction(invoicelist)

		newpurchase=QAction('New Purchase Order', self)
		newpurchase.setShortcut('Ctrl+P')
		Purchases.addAction(newpurchase)
		Purchases.addAction(QAction('Purchase Order List', self))
		Purchases.addAction(QAction('Enter Accounts Payable', self))
		Purchases.addAction(QAction('Enter Payments of Accounts Payable', self))
		Purchases.addAction(QAction('View Accounts Payable', self))
		Purchases.addAction(QAction('View Accounts Payable Payment', self))

		Transaction.addAction(QAction('Payment Transaction', self))
		Transaction.addAction(QAction('Receive a Payment', self))
		journal=QAction('Manul Journal Entry', self)
		journal.setShortcut('Ctrl+J')
		Transaction.addAction(journal)
		Transaction.addAction(QAction('Accounts Reconciliation', self))

		Report.addAction(QAction('Invoice Report', self))
		Report.addAction(QAction('Item Per Customer', self))
		Report.addAction(QAction('Customers Sales Report', self))
		Report.addAction(QAction('Sale Invoice Payment Report', self))
		Report.addAction(QAction('Accounts Payable Report', self))
		Report.addAction(QAction('Payments of Accounts Payable Report', self))
		Report.addAction(QAction('Unpaid Accounts Report', self))
		Report.addAction(QAction('General Ledger', self))
		Report.addAction(QAction('Account Enquiry', self))
		Report.addAction(QAction('Chart of Accounts', self))
		Report.addAction(QAction('Income Statement', self))
		Report.addAction(QAction('Trial Balance', self))
		Report.addAction(QAction('Financial Position', self))
		Report.addAction(QAction('Financial Performance', self))
		Report.addAction(QAction('Cash Flow Statement', self))
		Report.addAction(QAction('Others', self))

		View.addAction(QAction('Chart of Accounts...', self))
		View.addAction(QAction('Journal...', self))
		#View.addAction(QAction('Invoives...', self))
		#View.addAction(QAction('Accounts Payable...', self))
		#View.addAction(QAction('Payments of Accounts Payable...', self))
		#View.addAction(QAction('Customers...', self))
		#View.addAction(QAction('Suppliers...', self))
		#View.addAction(QAction('Payments...', self))

		self.statusBar()

		Accountmenu.triggered.connect(self.Accountmenu)
		Sales.triggered.connect(self.Sales)
		Purchases.triggered.connect(self.Purchases)
		Transaction.triggered.connect(self.Transaction)
		Report.triggered.connect(self.Report)
		View.triggered.connect(self.View)

		self.toolbar = self.addToolBar('Exit')
		self.toolbar.setObjectName('toolbar')

		self.addaccount= QAction(QIcon('image/icon/add.ico'), 'Add New Account', self)
		self.report= QAction(QIcon('image/icon/report1.png'), 'Income Statement', self)
		self.journal= QAction(QIcon('image/icon/audit.png'), 'Journal', self)
		self.startserver= QAction(QIcon('image/icon/Globe-Warning.ico'), ('You cannot start this server' if self.usertype=='User' else 'Start Server connection'), self)
		self.refresh= QAction(QIcon('image/icon/sync.ico'), 'Data refresh', self)
		self.setting= QAction(QIcon('image/icon/configure.ico'), 'Options', self)
		self.backup= QAction(QIcon('image/icon/data_replace.png'), 'Back up', self)

		
		if self.usertype=='User':
			self.startserver.setDisabled(True)

		self.toolbar.addAction(self.addaccount)
		self.toolbar.addAction(self.report)
		self.toolbar.addAction(self.journal)
		self.toolbar.addAction(self.startserver)
		self.toolbar.addSeparator()
		self.toolbar.addAction(self.refresh)
		self.toolbar.addAction(self.backup)
		self.toolbar.addAction(self.setting)



		self.addaccount.triggered.connect(self.AddAccount)
		self.journal.triggered.connect(self.GotoViewjournal)
		self.startserver.triggered.connect(self.StartServerConnection)
		self.refresh.triggered.connect(self.DataRefresh)
		self.setting.triggered.connect(self.ChangeSetting)
		self.backup.triggered.connect(self.BackUp)
	
	def AddAccount(self):
		self.addacc=AddAccount('widg',[])
		self.addacc.show()

	def BackUp(self):
		self.qtimer.stop()
		self.backUp=BackUp(self)
		if len(self.backup) > 5:
			self.backUp.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
			self.backUp.setWindowFlags(self.windowFlags() & ~(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint))
		self.backUp.show()

	def StartServerConnection(self):

		worker = Worker()
		self.threadpool.start(worker)
		self.RequiredData('required','date1','date2','requireddata')
		self.startserver= QAction(QIcon('image/icon/web-management.ico'), ' Server currently running...', self)
		
		self.toolbar.clear()
		self.toolbar.addAction(self.addaccount)
		self.toolbar.addAction(self.report)
		self.toolbar.addAction(self.journal)
		self.toolbar.addAction(self.startserver)
		self.toolbar.addSeparator()
		self.toolbar.addAction(self.refresh)
		self.toolbar.addAction(self.backup)
		self.toolbar.addAction(self.setting)

	def DataRefresh(self):
		self.RequiredData('required','date1','date2','requireddata')
	def ChangeSetting(self):
		(Settings(self)).exec_()	
	
	def Accountmenu(self,obj):
		if obj.text()=='Exit':
			self.close()

	def Sales(self,obj):
		if obj.text()=='New Invoice':
			self.invoice=Invoice({})
			(self.invoice.show())
		if obj.text()=='Customers Payment':		
			(InvoivePayment(self)).show()
		if obj.text()=='Open Invoices List':		
			(InvoicePayable(self)).show()	

	def Purchases(self,obj):
		if obj.text()=='Enter Accounts Payable':
			(Payable(self)).show()
		if obj.text()==	'Enter Payments of Accounts Payable':
			(PayPayable(self)).show()
		if obj.text()==	'View Accounts Payable':
			self.accpay=AccountsPayable({},1,2,3)
			self.accpay.show()	

			
	def Transaction(self,obj):
		#if obj.text()=='Payment Transaction':	
			#(PaymentPurchase(self)).show()
		if obj.text()=='Receive a Payment':	
			self.receivepay=ReceiptDeposit(self)
			self.receivepay.show()	
		if obj.text()=='Manul Journal Entry':	
			self.addjournal=AddJournal('',{},'','')
			self.addjournal.exec_()


	def Report(self,obj):

		if obj.text()=='Accounts Payable Report':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewAccountPayable)
			self.dialog.exec_()

		if obj.text()=='Chart of Accounts':
			(AccountsChart(self)).show()

		if obj.text()=='Customers Sales Report':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewCustomersSales)
			self.dialog.exec_()

		if obj.text()=='Account Enquiry':
			self.BetweenDates()
			requireddata=open("db/accounts.json", "r")
			self.requireddata=json.load(requireddata)
			AccountsList=self.requireddata
			AccountsList.sort()
		
			self.comboboxAccount=QComboBox()
			self.comboboxAccount.setEditable(True)
			self.comboboxAccount.addItem('')	
			completer = QCompleter(AccountsList)
			self.comboboxAccount.setCompleter(completer)
			self.comboboxAccount.addItems(AccountsList)
			self.formlayout.addRow('Account:', self.comboboxAccount)

			self.viewbutn.clicked.connect(self.ViewAccountEnquiry)
			self.dialog.exec_()	

		if obj.text()=='Sale Invoice Payment Report':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewInvoicesPayment)
			self.dialog.exec_()

		if obj.text()=='Invoives Report':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewInvoices)
			self.dialog.exec_()	

		if obj.text()=='General Ledger':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewGeneralLedger)
			self.dialog.exec_()
			
		if obj.text()=='Income Statement':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewIncomeStatement)
			self.dialog.exec_()

		if obj.text()=='Trial Balance':
			self.BetweenDates()
			self.viewbutn.clicked.connect(self.ViewTrialBalsheet)
			self.dialog.exec_()	
		
		if obj.text()=='Financial Position':
			self.SingleDate()
			self.viewbutn.clicked.connect(self.ViewBalsheet)
			self.dialog.exec_()

		if obj.text()=='Financial Performance':
			self.SingleDate()
			self.viewbutn.clicked.connect(self.ViewFinPerformance)
			self.dialog.exec_()	
	
	def ViewAccountEnquiry(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		account=(self.comboboxAccount.currentText())
		datacc=json.dumps([self.FormatDate(date2),account])
		datacc=base64.b64encode(datacc.encode())
		if account=="":
			return False
		self.RequiredData("accountsenquiry",self.FormatDate(date1),datacc,"accountsenquiry")
	def ViewAccountPayable(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("accountspayable",self.FormatDate(date1),self.FormatDate(date2),"accountspayable")

	def ViewInvoices(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("invoices",self.FormatDate(date1),self.FormatDate(date2),"invoices")

	def ViewCustomersSales(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("customersales",self.FormatDate(date1),self.FormatDate(date2),"customersales")	

	def ViewInvoicesPayment(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("invoicepayment",self.FormatDate(date1),self.FormatDate(date2),"invoicepayment")	

	def ViewGeneralLedger(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("fetchledger",self.FormatDate(date1),self.FormatDate(date2),"fetchledger")
	
	def ViewIncomeStatement(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("incomestatement",self.FormatDate(date1),self.FormatDate(date2),"incomestatement")

	def ViewTrialBalsheet(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		date2=self.dateedit2.date()
		self.RequiredData("fetchtrialbalance",self.FormatDate(date1),self.FormatDate(date2),"trialbalance")
	
	def ViewBalsheet(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		self.RequiredData("fetchbalancesheet",self.FormatDate(date1),"date2","balancesheet")

	def ViewFinPerformance(self):
		self.dialog.close()
		date1=self.dateedit1.date()
		self.RequiredData("fetchfinperformance",self.FormatDate(date1),"date2","finperformance")	
		
	def View(self,obj):
		if obj.text()=='Chart of Accounts...':
			(AccountsChart(self)).show()	
			
			
		if obj.text()=='Journal...':
			(Journal(self)).show()
		if obj.text()=='Accounts Payable...':
			(AccountsPayable(self)).show()
		if obj.text()=='Suppliers...':
			(Suppliers(self)).show()		
	
	def BetweenDates(self):
		self.dialog=QDialog(self)
		layout=QVBoxLayout()
		groupbox = QGroupBox('Select Period')
		layout.addWidget(groupbox)
		self.dialog.setLayout(layout)
		self.dialog.setWindowTitle("Select Period for this Report")
		self.formlayout = QFormLayout()	
		self.formlayout.setHorizontalSpacing(70)
		groupbox.setLayout(self.formlayout)
		self.combo=QComboBox()
		self.combo.currentTextChanged.connect(self.SetDoubleDate)
		self.combo.addItems(['Select Period','Today','This Month','Last Month',\
			'This Quarter','Last Quarter','This Year','Last Year','This Fiscal Year','Last Fiscal Year'])
		
		self.date1()
		self.date2()
		self.formlayout.addRow('Select date:', self.combo)
		self.formlayout.addRow('Start Date:', self.dateedit1)
		self.formlayout.addRow('End Date:', self.dateedit2)

		grid=QGridLayout()
		layout.addLayout(grid)
		self.viewbutn=QPushButton('View')
		self.cancelbutn=QPushButton('Cancel') 
		self.helpbutn=QPushButton('Help')

		self.cancelbutn.clicked.connect(self.dialog.close)

		grid.addWidget(self.viewbutn,0,1)
		grid.addWidget(self.cancelbutn,0,2)
		grid.addWidget(self.helpbutn,0,3)
		
	def SingleDate(self):
		self.dialog=QDialog(self)
		layout=QVBoxLayout()
		groupbox = QGroupBox('Select date')
		layout.addWidget(groupbox)
		self.dialog.setLayout(layout)
		self.dialog.setWindowTitle("Select Date")
		formlayout = QFormLayout()	
		formlayout.setHorizontalSpacing(50)
		groupbox.setLayout(formlayout)
		self.combo=QComboBox()
		self.combo.currentTextChanged.connect(self.SetSingleDate)
		self.combo.addItems(['Select','Today','Yesterday','End of last month','End of last year'])
		self.date1()
		formlayout.addRow('Select date:', self.combo)
		formlayout.addRow('Date:', self.dateedit1)

		grid=QGridLayout()
		layout.addLayout(grid)
		self.viewbutn=QPushButton('View')
		self.cancelbutn=QPushButton('Cancel') 
		self.helpbutn=QPushButton('Help')

		self.cancelbutn.clicked.connect(self.dialog.close)

		grid.addWidget(self.viewbutn,0,1)
		grid.addWidget(self.cancelbutn,0,2)
		grid.addWidget(self.helpbutn,0,3)
	
	def SetDoubleDate(self,obj):
		#print("Days in month: {0}".format(d.daysInMonth()))
		#print("Days in year: {0}".format(d.daysInYear()))
		if obj=='Select Period':
			return False
		date = QDate()
		currentdate=date.currentDate()
		year=currentdate.year()
		month=currentdate.month()
		day=currentdate.day()
		days_in_month=currentdate.daysInMonth()

		
		if obj=='Today':
			self.dateedit1.setDate(currentdate)
			self.dateedit2.setDate(currentdate)
		if obj=='This Month':
			begin_date=QDate(year, month, 1)
			end_date=QDate(year, month, days_in_month)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)	
		if obj=='Last Month':
			prev_date=currentdate.addMonths(-1)
			year=prev_date.year()
			month=prev_date.month()
			days=prev_date.daysInMonth()
			begin_date=QDate(year,month,1)
			end_date=QDate(year,month,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)		
		if obj=='This Quarter':
			if month==1 or month==4 or month==7 or month==10:
				next_date=currentdate.addMonths(2)
				next_month=next_date.month()
				days=next_date.daysInMonth()
				begin_date=QDate(year,month,1)
				end_date=QDate(year,next_month,days)
			if month==2 or month==5 or month==8 or month==11:
				prev_date=currentdate.addMonths(-1)
				next_date=currentdate.addMonths(1)
				prev_month=prev_date.month()
				next_month=next_date.month()
				days=next_date.daysInMonth()
				begin_date=QDate(year,prev_month,1)
				end_date=QDate(year,next_month,days)
			if month==3 or month==6 or month==9 or month==12:
				prev_date=currentdate.addMonths(-2)
				prev_month=prev_date.month()
				begin_date=QDate(year,prev_month,1)
				end_date=QDate(year,month,days_in_month)		
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)	
		if obj=='Last Quarter':
			if  month==1 or month==4 or month==7 or month==10:
				next_date=currentdate.addMonths(-1)
				prev_date=currentdate.addMonths(-3)
				next_month=next_date.month()
				prev_month=prev_date.month()
				year=next_date.year()
				days=next_date.daysInMonth()
				begin_date=QDate(year,prev_month,1)
				end_date=QDate(year,next_month,days)	
			if month==2 or month==5 or month==8 or month==11:
				next_date=currentdate.addMonths(-2)
				prev_date=currentdate.addMonths(-4)
				next_month=next_date.month()
				prev_month=prev_date.month()
				year=next_date.year()
				days=next_date.daysInMonth()
				begin_date=QDate(year,prev_month,1)
				end_date=QDate(year,next_month,days)
			if month==3 or month==6 or month==9 or month==12:
				next_date=currentdate.addMonths(-3)
				prev_date=currentdate.addMonths(-5)
				next_month=next_date.month()
				prev_month=prev_date.month()
				year=next_date.year()
				days=next_date.daysInMonth()
				begin_date=QDate(year,prev_month,1)
				end_date=QDate(year,next_month,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)		
		if obj=='This Year':
			days=QDate(year,12,1).daysInMonth()
			begin_date=QDate(year,1,1)
			end_date=QDate(year,12,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)	
		if obj=='Last Year':
			prev_date=currentdate.addYears(-1)
			year=prev_date.year()
			days=QDate(year,12,1).daysInMonth()
			begin_date=QDate(year,1,1)
			end_date=QDate(year,12,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)	
		if obj=='This Fiscal Year':
			days=QDate(year,12,1).daysInMonth()
			begin_date=QDate(year,1,1)
			end_date=QDate(year,12,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)	
		if obj=='Last Fiscal Year':
			prev_date=currentdate.addYears(-1)
			year=prev_date.year()
			days=QDate(year,12,1).daysInMonth()
			begin_date=QDate(year,1,1)
			end_date=QDate(year,12,days)
			self.dateedit1.setDate(begin_date)
			self.dateedit2.setDate(end_date)		
		
	
	def SetSingleDate(self,obj):
		if obj=='Select':
			return False
		date = QDate()
		currentdate=date.currentDate()
		
		if obj=='Today':
			self.dateedit1.setDate(currentdate)
		if obj=='Yesterday':
			self.dateedit1.setDate(currentdate.addDays(-1))
		if obj=='End of last month':
			day=currentdate.day()
			self.dateedit1.setDate(currentdate.addDays(-day))
		if obj=='End of last year':
			#QDate(2016, 12, 24).daysTo(now) can as well be used
			year=currentdate.year()
			begin_year=QDate(year, 1, 1)
			currentdate_to_julian=currentdate.toJulianDay()
			begin_year_to_julian_=begin_year.toJulianDay()
			days_pass=currentdate_to_julian - begin_year_to_julian_
			currentdate=date.currentDate()
			self.dateedit1.setDate(currentdate.addDays(-days_pass-1))			
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
			
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
	
	def FormatDate(self,date):
		year1=str(date.year())
		day1=str(date.day()) if len(str(date.day()))==2 else '0'+str(date.day())
		month1=str(date.month()) if len(str(date.month()))==2 else '0'+str(date.month())
		return (year1+'-'+month1+'-'+day1)	
	
	def GotoBackup(self):
		self.backUp=BackUp(self)
		if len(self.backup) > 5:
			self.backUp.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
			self.backUp.setWindowFlags(self.windowFlags() & ~(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint))
		self.dialog.close()
		self.backUp.show()

	def BackupDialog(self):
		self.dialog=QDialog(self)
		self.dialog.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
		self.dialog.setWindowFlags(self.windowFlags() & ~(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint))
		
		self.dialog.setWindowTitle("BackUp")
		layout = QGridLayout()
		self.dialog.setLayout(layout)
		label=QLabel(self)
		pixmap=QPixmap('image/icon/data_replace.png')
		label.setPixmap(pixmap)

		layout.addWidget(label,0,0)
		layout.addWidget(QLabel("\nPlease Backup Your data now	\n\n  "),0,1,1,2)
		

		self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		self.buttonbox.button(QDialogButtonBox.Ok).setText("Go to Backup!")
		self.buttonbox.accepted.connect(self.GotoBackup)
		self.buttonbox.rejected.connect(self.dialog.close)
		if len(self.backup) >5:
			self.buttonbox.button(QDialogButtonBox.Cancel).setDisabled(True)
		layout.addWidget(self.buttonbox,1,1)
		self.dialog.exec_()	

	def timer_fn(self):
		self.DURATION-=1
		if self.DURATION==0:
			self.BackupDialog()
			self.qtimer.stop()
		#print(self.DURATION)

	def RequiredData(self,action,date1,date2,path):
		self.overlay.setVisible(True)
		data = QtCore.QByteArray()
		data.append("action={}&".format(action))
		data.append("date1={}&".format(date1))
		if action=='accountsenquiry':
			data.append("date2={}".format(date2.decode("utf-8")))
		else:
			data.append("date2={}".format(date2))

		url = "http://{ip}:5000/{path}".format(ip=self.ip,path=path)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,"application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(partial(self.handleResponse,action,date1,date2))
		self.nam.post(req, data)

	def handleResponse(self,action,date1,date2,reply):
		er = reply.error()	
		if er == QtNetwork.QNetworkReply.NoError:
			bytes_string = reply.readAll()
			DATA = json.loads(str(bytes_string, 'utf-8'))

			self.overlay.setVisible(False)	
			if action=="accountsenquiry":
				decode=base64.b64decode(date2)
				date_=json.loads(decode.decode("utf-8"))
				self.accntenquiry=AccountsEnquiry(DATA,date1,date_[0])
				self.accntenquiry.show()
				return False
			if action=="accountspayable":
				self.accntpayable=AccountsPayable(DATA,date1,date2,'report')
				self.accntpayable.show()
				return False
			if action=="invoices":
				self.invoicere=InvoiceRe(DATA,date1,date2)
				self.invoicere.show()
				return False
				
			if action=="invoicepayment":
				self.invoicepaymentre=InvoicePaymentRe(DATA,date1,date2)
				self.invoicepaymentre.show()
				return False	
			if action=="customerpayment":
				self.customerpaymentre=CustomerPaymentRe(DATA,date1,date2)
				self.customerpaymentre.show()
				return False		
			if action=="fetchledger":
				self.ledger=Ledger(DATA,date1,date2)
				self.ledger.show()
				return False
			if action=="incomestatement":
				self.income=Income(DATA,date1,date2)
				self.income.show()
				return False
					
			if action=="fetchtrialbalance":
				self.trialbal=TrialBalance(DATA,date1,date2)
				self.trialbal.show()
				return False

			if action=="fetchbalancesheet":
				self.bal=BalanceSheet(DATA,date1,date2)
				(self.bal).show()
				#print(DATA)
				return False
			if action=="fetchfinperformance":
				self.finperformance=FinPerformance(DATA,date1,date2)
				(self.finperformance).show()
				#print(DATA)
				return False	
			#print(DATA['addinvoice'])
			self.backup=DATA.get('backup','')
			viewchart=DATA.get('viewchart','')
			addinvoice=DATA.get('addinvoice','')
			accountpayable=DATA.get('accountpayable','')			
			json.dump(viewchart, open("db/viewchart.json", "w"))
			json.dump(addinvoice, open("db/addinvoice.json", "w"))
			json.dump(accountpayable, open("db/accountpayable.json", "w"))

			accounts=DATA.get('accounts','')
			selectreportcode=DATA.get('selectreportcode','')
			suppliersdata=DATA['suppliersdata']			
			json.dump(accounts, open("db/accounts.json", "w"))
			json.dump(selectreportcode, open("db/selectreportcode.json", "w"))
			json.dump(suppliersdata, open("db/suppliersdata.json", "w"))

			paysuppliersdata=DATA.get('paysuppliersdata','')
			invoicepaymentdata=DATA.get('invoicepaymentdata','')
			cashaccounts=DATA.get('cashaccounts','')
			json.dump(paysuppliersdata, open("db/paysuppliersdata.json", "w"))
			json.dump(invoicepaymentdata,open("db/invoicepaymentdata.json", "w"))
			json.dump(cashaccounts, open("db/cashaccounts.json", "w"))

			payabledata=DATA.get('payabledata','')
			invoicedata=DATA.get('invoicedata','')			
			json.dump(payabledata, open("db/payabledata.json", "w"))
			json.dump(invoicedata, open("db/invoicedata.json", "w"))
					
		else:
			self.overlay.setVisible(False)
			QMessageBox.critical(self, 'Server Error ', "\n{}. Please start the server	\n  ".format(reply.errorString()))
			
			return 'server_error'	
		
		#StartServer()		

	def Content(self):	 
	
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.mainlayout.setSpacing(0)
		self.mainlayout.setContentsMargins(0, 0, 0, 0)

		scroll=QScrollArea()
		scroll.setWidgetResizable(True)
		
		minorlayout=QVBoxLayout()
		majorlayout=QVBoxLayout()

		scrollwidget=QWidget()
		scrollwidget.setLayout(majorlayout)
		scroll.setWidget(scrollwidget)

		self.mainlayout.addLayout(minorlayout,1)
		self.mainlayout.addWidget(scroll,8)
				
		titlelayout=QGridLayout()
		companylayout=QGridLayout()

		title=QLabel("SmartAccount")
		title.setObjectName('title')
		logoff=ClickableLabel()
		logoff.setText("<a href='/none/'>Log Off</a>")
		space=QLabel()
		space1=QLabel()
		logoff.setObjectName('logoff')
		space.setObjectName('logoff')
		#space1.setObjectName('logoff')
		logoff.clicked.connect(self.close)
		
		titlelayout.addWidget(title,0,0)
		titlelayout.addWidget(space,0,1,1,12)
		titlelayout.addWidget(logoff,0,12)
		
		company=QLabel('v 2.0.1 © Sadel Technology')
		company.setObjectName('company')
		web=QLabel()
		web.setObjectName('web')
		web.setText("<a href='http://www.sadeltech.com.ng/smartaccount'>www.sadeltech.com.ng</a>")
		web.setOpenExternalLinks(True)
		loginas=QLabel()
		loginas.setText('You log in as: %s' %self.useremail)
		loginas.setObjectName('loginas')
		
		companylayout.addWidget(company,0,0)
		companylayout.addWidget(web,0,1,1,8)
		companylayout.addWidget(loginas,0,9)
		
		
		minorlayout.addLayout(titlelayout,3)
		minorlayout.addLayout(companylayout,1)

		dashboard=QGridLayout()
		action=QHBoxLayout()
		action.setSpacing(20)

		majorlayout.addLayout(dashboard,1)
		majorlayout.addLayout(action,7)	


		dashboard.addWidget(QLabel(''))
		

		logolayout=QVBoxLayout()
		actionlayout1=QGridLayout()
		actionlayout1.setVerticalSpacing(10)
		actionlayout1.setHorizontalSpacing(5)
		actionlayout2=QVBoxLayout()
		actionlayout2.setObjectName('actionlayout2')

		action.addLayout(logolayout,1)
		action.addLayout(actionlayout1,3)
		action.addLayout(actionlayout2,1.5)

		logolayout.addWidget(QLabel(''))
	
		
		newinvoice=ClickableLabel()
		addjournal=ClickableLabel()
		viewjournal=ClickableLabel()
		transfer=ClickableLabel()
		supplier=ClickableLabel()
		payment=ClickableLabel()
		receiptmentpayment=ClickableLabel()
		invoice=ClickableLabel()
		accountspayable=ClickableLabel()
		items=ClickableLabel()
		customers=ClickableLabel()
		report=ClickableLabel()

		newinvoice.clicked.connect(self.GotoNewInvoice)
		addjournal.clicked.connect(self.GotoAddjournal)
		viewjournal.clicked.connect(self.GotoViewjournal)
		supplier.clicked.connect(self.GotoSupplier)
		receiptmentpayment.clicked.connect(self.GotoReceiptPayment)
		accountspayable.clicked.connect(self.GotoAccountPayable)
		customers.clicked.connect(self.GotoCustomers)
		transfer.clicked.connect(self.GotoAccountTransfer)
		payment.clicked.connect(self.GotoPayment)
		invoice.clicked.connect(self.GotoInvoice)

		newinvoice.setText("<a  href='/none/' style='font-size:15px;'>Create new invoice</a><br><p style='font-size:12px;'>Create a new invoice or manage existing invoices</p>")
		addjournal.setText("<a href='/none/' style='font-size:15px;'>Manual journal entry</a><br><p style='font-size:12px;'>Add custom journal entry</p>")
		viewjournal.setText("<a href='/none/'  style='font-size:15px;'>View Journal </a><br><p style='font-size:12px;'>View the full journal</p>")
		transfer.setText("<a  href='/none/' style='font-size:15px;'>Transfer between accounts</a><br><p style='font-size:12px;'>Create a new invoice or manage existing invoices</p>")
		supplier.setText("<a  href='/none/' style='font-size:15px;'>View Suppliers</a><br><p style='font-size:12px;'>create new or manage existing suppliers</p>")
		payment.setText("<a  href='/none/' style='font-size:15px;'>Make a payment</a><br><p style='font-size:12px;'>Payments and Purchases transactions</p>")
		receiptmentpayment.setText("<a  href='/none/' style='font-size:15px;'>Receive a payment</a><br><p style='font-size:12px;'>Receipts and Deposits</p>")
		invoice.setText("<a  href='/none/' style='font-size:15px;'>Invoices</a><br><p style='font-size:12px;'>View list of all invoices made</p>")
		accountspayable.setText("<a  href='/none/' style='font-size:15px;'>View accounts payable</a><br><p style='font-size:12px;'>check the lists of account payable</p>")
		items.setText("<a  href='/none/' style='font-size:15px;'>Items</a><br><p style='font-size:12px;'>view lists of sold items</p>")
		customers.setText("<a  href='/none/' style='font-size:15px;'>Customers</a><br><p style='font-size:12px;'>Create or manage existing customers</p>")
		report.setText("<a  href='/none/' style='font-size:15px;'>Reports</a><br><p>Access all transactions report</p>")

		newinvoiceimg=QLabel(self)
		pixmap=QPixmap('image/icon/invoice.png')
		newinvoiceimg.setPixmap(pixmap)
				
		addjournalimg=QLabel(self)
		pixmap=QPixmap('image/icon/addjournal.png')
		addjournalimg.setPixmap(pixmap)

		viewjournalimg=QLabel(self)
		pixmap=QPixmap('image/icon/Journal.png')
		viewjournalimg.setPixmap(pixmap)

		transferimg=QLabel(self)
		pixmap=QPixmap('image/icon/account.png')
		transferimg.setPixmap(pixmap)

		supplierimg=QLabel(self)
		pixmap=QPixmap('image/icon/document.png')
		supplierimg.setPixmap(pixmap)

		paymentimg=QLabel(self)
		pixmap=QPixmap('image/icon/payment.png')
		paymentimg.setPixmap(pixmap)

		receiptmentpaymentimg=QLabel(self)
		pixmap=QPixmap('image/icon/payment.png')
		receiptmentpaymentimg.setPixmap(pixmap)

		invoiceimg=QLabel(self)
		pixmap=QPixmap('image/icon/coins.png')
		invoiceimg.setPixmap(pixmap)

		accountspayableimg=QLabel(self)
		pixmap=QPixmap('image/icon/debit-card.png')
		accountspayableimg.setPixmap(pixmap)

		itemsimg=QLabel(self)
		pixmap=QPixmap('image/icon/goods.png')
		itemsimg.setPixmap(pixmap)

		customersimg=QLabel(self)
		pixmap=QPixmap('image/icon/customer.png')
		customersimg.setPixmap(pixmap)

		reportimg=QLabel(self)
		pixmap=QPixmap('image/icon/report.png')
		reportimg.setPixmap(pixmap)

		actionlayout1.addWidget(newinvoiceimg,0,0)
		actionlayout1.addWidget(newinvoice,0,1,1,3)
		
		actionlayout1.addWidget(addjournalimg,0,5)
		actionlayout1.addWidget(addjournal,0,6)
		
		actionlayout1.addWidget(viewjournalimg,1,0)
		actionlayout1.addWidget(viewjournal,1,1,1,3)
		
		actionlayout1.addWidget(transferimg,1,5)
		actionlayout1.addWidget(transfer,1,6)

		actionlayout1.addWidget(supplierimg,2,0)
		actionlayout1.addWidget(supplier,2,1,1,3)

		actionlayout1.addWidget(paymentimg,2,5)
		actionlayout1.addWidget(payment,2,6)

		actionlayout1.addWidget(receiptmentpaymentimg,3,0)
		actionlayout1.addWidget(receiptmentpayment,3,1,1,3)

		actionlayout1.addWidget(invoiceimg,3,5)
		actionlayout1.addWidget(invoice,3,6)

		actionlayout1.addWidget(accountspayableimg,4,0)
		actionlayout1.addWidget(accountspayable,4,1,1,3)

		actionlayout1.addWidget(itemsimg,4,5)
		actionlayout1.addWidget(items,4,6)

		actionlayout1.addWidget(customersimg,5,0)
		actionlayout1.addWidget(customers,5,1,1,3)

		actionlayout1.addWidget(reportimg,5,5)
		actionlayout1.addWidget(report,5,6)

		actionlayout2.addWidget(QLabel(''))


	def GotoNewInvoice(self):
		self.invoice=Invoice({})
		(self.invoice.show())
	def GotoAddjournal(self):
		self.addjournal=AddJournal('',{},'','')
		self.addjournal.exec_()
	def GotoViewjournal(self):
		(Journal(self)).show()
	def GotoSupplier(self):
		self.suppl=Suppliers('')
		self.suppl.show()
	def GotoReceiptPayment(self):
		self.receiptpay=ReceiptDeposit(self)
		self.receiptpay.show()
	def GotoAccountPayable(self):
		self.accountpayable=AccountsPayable({},1,2,3)
		self.accountpayable.show()
	def GotoCustomers(self):
		self.customers=Customers('')
		self.customers.show()
	def GotoAccountTransfer(self):
		self.transfer=TransferAccount(self)
		self.transfer.exec_()							
	def GotoPayment(self):
		self.paypurchase=PaymentPurchase({})
		self.paypurchase.show()
	def GotoInvoice(self):
		self.invoicepay=InvoicePayable(self)
		self.invoicepay.show()	

	def resizeEvent(self,event): 
		self.overlay.resize(event.size())
		event.accept()

	def closeEvent(self, event):
		close= QMessageBox(self)
		close.setWindowTitle('quit')
		close.setText('You sure you want to close SmartAccount now?')
		close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
		close=close.exec_()

		if close==QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

		
class Worker(QRunnable):
    @pyqtSlot()
    def run(self):

        StartServer()
        while True:
        	time.sleep(1)
       
	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Main("e-mail","Administrator")

	date = QDate()
	currentdate=date.currentDate()
	year=currentdate.year()
	month=currentdate.month()
	day=currentdate.day()

	activedate=open("db/activedate.json", "r")
	activedate=json.load(activedate)
	day_=int((activedate.split('-'))[0])
	month_=int((activedate.split('-'))[1])
	year_=int((activedate.split('-'))[2])


	dayscount=(QDate(year_, month_, day_).daysTo(QDate(year, month, day)))
	#print(dayscount)
	import re, uuid
	mac=str(uuid.getnode())
	#print(mac[7:])#mac number of the system 
	print(dayscount)
	if dayscount>1360:
		register=Register()
		register.exec_()

	sys.exit(app.exec_())


		