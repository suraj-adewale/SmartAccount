from PyQt5.QtWidgets import QPushButton,QAction,QTableWidgetItem,QAbstractItemView,QTableWidget,QTextEdit,QLabel,QFormLayout,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from payable import Payable
from babel.numbers import format_currency
from jinja2 import Template


class AccountsPayable(QMainWindow):
	def __init__(self,DATA,date1,date2,report, parent=None):
		super(AccountsPayable, self).__init__(parent)
		self.title = 'Account Payable'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.date1=date1
		self.date2=date2
		
		if report=='report':
			self.requireddata=DATA
		else:
			requireddata=open("db/accountpayable.json", "r")
			self.requireddata=json.load(requireddata)

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.AccountPayableList()
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
		NewEntryButton.triggered.connect(self.CreateNewAccount)

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
		self.addaccount= QAction(QIcon('image/icon/add.ico'), 'Add Account', self)
		self.edit= QAction(QIcon('image/icon/edit.ico'), 'Edit Account', self)
		self.delete= QAction(QIcon('image/icon/delete.ico'), 'Delete Account', self)
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview Journal', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print Journal', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Journal', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Journal', self)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		if self.requireddata=={}:
			self.preview.setDisabled(True)
			self.print.setDisabled(True)
			self.save.setDisabled(True)
			self.mail.setDisabled(True)
		
		toolbar.addAction(self.addaccount)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()

		toolbar.addAction(self.preview)
		toolbar.addAction(self.print)
		toolbar.addAction(self.save)
		toolbar.addAction(self.mail)

		self.addaccount.triggered.connect(self.CreateNewAccount)
		self.edit.triggered.connect(self.Edit)
		self.delete.triggered.connect(self.Delete)
		self.preview.triggered.connect(self.Preview)
		self.print.triggered.connect(self.Print)
		self.save.triggered.connect(self.Save)
		self.mail.triggered.connect(self.Mail)		

	def CreateNewAccount(self):
		self.supplier=Payable()
		self.supplier.show()	

	def Edit(self):
		journaltypelist=['all',"General","Payments","Sales","Receipts","Purchases"]
		index=self.tabs.currentIndex()
		self.delref=self.deljournal[self.delkey]
		self.JournalData(journaltypelist[index],self.date1,self.date2,'Edit')
	
	def Delete(self):
		
		index=self.tabs.currentIndex()
		self.delref=self.deljournal[self.delkey]
		
		QMessageBox.critical(self, 'Confirm Delete', "	\n Are you sure you want to delete selected journal entries {} at row {}	\n\n  ".\
			format(self.delref,self.delkey+1))

		#print(self.message.Cancel)
		journaltypelist=['all',"General","Payments","Sales","Receipts","Purchases"]
		if  QMessageBox.Ok==1024:
			self.TabTable(self.tabs.currentIndex())
			self.JournalData(journaltypelist[index],self.date1,self.date2,'Delete')


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
		dataDic={}
		dataList=[]
		total=0
		for row in self.requireddata:
			dataList.append(self.requireddata[row][0])
			dataList.append(self.requireddata[row][1])
			dataList.append(self.requireddata[row][3])
			dataList.append(self.requireddata[row][4])
			dataList.append(self.requireddata[row][8])
			dataList.append(format_currency(float(self.requireddata[row][5]),'NGN', locale='en_US'))
			dataDic[int(row)]=dataList
			total=total+float(self.requireddata[row][5])
		number=len(self.requireddata)



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
		padding: 8px;
		}
		</style>
		<body>
		<div style=" font-weight: bold;font-size:13px; text-align:center">
       <img source="image/report.JPG">
		   <p>FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
      <p>Accounts Payable Report<p/>
      </div>
     
      <p style="font-size:13px; text-align:right">Period: {{date1}} to {{date2}}<br>Number: {{num}}<br>Total: {{total}}<p/>
     

		<table border=".3" cellSpacing="0" width="100%">
		<tr><th>Date</th><th>Due Date</th><th>Ref</th><th>Supplier</th><th>Payment Ref</th><th>Amount</th></tr>
		{% for row in data %}<tr>
		{% for element in data[row] %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}
		<tr><th>Total</th><th></th><th></th><th></th><th></th><th>{{total}}</th></tr>
		

		</table>
		</body>
		"""
		cursor.insertHtml(Template(table).render(data=dataDic,total=format_currency(float(total),'NGN', locale='en_US'),num=number,date1=self.date1,date2=self.date2))	
		document.print_(printer)		
		
		
	def Print(self):
		self.handle_print()
		
	def Save(self):
		pass	
	def Mail(self):
		pass		

	def AccountPayableList(self):
	
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.table =QTableWidget()
		self.mainlayout.addWidget(self.table)

		self.SupplierTable()
		self.AccountData()

	def SupplierTable(self):
		
		AccountsPayableHeader=["  Date","         Due Date        ","         Reference           ","          Payable   ","          supplier   ","          Amount   ","          Due   ","          Status   "]
		self.table.setColumnCount(len(AccountsPayableHeader))     #Set three expense
		
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		header = self.table.horizontalHeader()
		for row in AccountsPayableHeader:
			header.setSectionResizeMode(AccountsPayableHeader.index(row), QtWidgets.QHeaderView.Stretch)
				
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(AccountsPayableHeader)	

	def AccountData(self):
		data=self.requireddata
		rows=len(data)
		self.table.setRowCount(rows)
		self.table.resizeRowsToContents()
		self.table.clicked.connect(self.TableAction)
		for row in sorted(data):
			self.table.setItem(int(row),0, QTableWidgetItem(data[row][0]))
			self.table.setItem(int(row),1, QTableWidgetItem(data[row][1]))
			self.table.setItem(int(row),2, QTableWidgetItem(data[row][2]))
			self.table.setItem(int(row),3, QTableWidgetItem(data[row][3]))
			self.table.setItem(int(row),4, QTableWidgetItem(data[row][4]))
			self.table.setItem(int(row),5, QTableWidgetItem(format_currency(data[row][5],'NGN', locale='en_US')))
			if data[row][6]==0.0:
				self.table.setItem(int(row),6, QTableWidgetItem(''))
			else:
				self.table.setItem(int(row),6, QTableWidgetItem(format_currency(data[row][6],'NGN', locale='en_US')))
			self.table.setItem(int(row),7, QTableWidgetItem(data[row][7]))

			
	def TableAction(self,item):

		row=item.row()
		self.deljournal={}
		self.delkey= row
		
		if self.requireddata.get(str(row), '') is not '':
			self.deljournal[row]=self.requireddata[str(row)][3]	
		self.edit.setEnabled(True)
		self.delete.setEnabled(True)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AccountsPayable()
	ex.show()
	sys.exit(app.exec_())
