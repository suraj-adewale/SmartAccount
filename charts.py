from PyQt5.QtWidgets import QTableWidgetItem,QDialog,QDialogButtonBox,QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
import sys
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from addaccount import AddAccount
from jinja2 import Template
from babel.numbers import format_currency,parse_decimal


class AccountsChart(QMainWindow):
	
	def __init__(self, parent=None):
		
		super(AccountsChart, self).__init__(parent)
		self.title = 'Chart of Accounts'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()
		self.Charts()
		self.setCentralWidget(self.widget)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		Journal = mainMenu.addMenu('Charts')
		homeMenu = mainMenu.addMenu('Report')
		homeMenu = mainMenu.addMenu('Help')
		 
		NewEntryButton = QAction(QIcon('exit24.png'), 'New Entry                    ', self)
		NewEntryButton.setShortcut('Ctrl+N')
		NewEntryButton.setStatusTip('New Journal')
		#NewEntryButton.triggered.connect(self.CreateNewJournal)

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
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview Journal', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print Journal', self)
		self.excel= QAction(QIcon('image/icon/excel.png'), 'View in Excel', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Journal', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Journal', self)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		
		
		toolbar.addAction(self.addaccount)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()

		toolbar.addAction(self.preview)
		toolbar.addAction(self.print)
		toolbar.addAction(self.excel)
		toolbar.addAction(self.save)
		toolbar.addAction(self.mail)

		self.addaccount.triggered.connect(self.CreateNewAccount)
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
		workbook = xlsxwriter.Workbook('{}/Documents/chart.xlsx'.format(home))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1, 'align':'right','num_format': '#,##.00'})

		worksheet.set_column(0, 0, 15)
		worksheet.set_column(1, 1, 35)
		worksheet.set_column(2, 4, 15)
		
		worksheet.insert_image(1, 2,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 1,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 1,'Chart of Accounts')
		row_end1=0
		row_end2=0

		headers =["   Number   ","  Name"," Balance(₦)        "," Type           ","   Report Group   "]
		self.income.insert(0,['','Revenue',self.total[0] ,'Revenue','Report group'])
		self.expense.insert(0,['','Expense',self.total[1],'Expense','Report group'])
		self.asset.insert(0,['','Assets',self.total[2],'Assets','Report group'])
		self.liability.insert(0,['','Liability',self.total[3],'Liability','Report group'])
		self.equity.insert(0,['','Equity',self.total[4],'Equity','Report group'])

		cols = range(4)
		row = 8

		for col in cols:
			worksheet.write(row, col,headers[col],format2)
		row = row + 1	

		for data in self.income:
			for col in cols:
				if data[col] == '' and data[col+1] == 'Revenue':
					row_end1 = row
					#row = row + 1
				if col==2:
					worksheet.write(row, col,parse_decimal(data[col], locale='en_US'),money_format)
				else:
					worksheet.write(row, col,data[col],format1)
			row = row + 1
			row_end2 = row
		worksheet.write(row_end1, 2,"=SUM(C{}:C{})".format(row_end1+2,row_end2),money_format)

		for data in self.expense:
			for col in cols:
				if data[col] == '' and data[col+1] == 'Expense':
					row_end1 = row
					#row = row + 1
				if col==2:
					worksheet.write(row, col,parse_decimal(data[col], locale='en_US'),money_format)
				else:
					worksheet.write(row, col,data[col],format1)
			row = row + 1
			row_end2 = row
		worksheet.write(row_end1, 2,"=SUM(C{}:C{})".format(row_end1+2,row_end2),money_format)	
		
		for data in self.asset:
			for col in cols:
				if data[col] == '' and data[col+1] == 'Assets':
					row_end1 = row
					#row = row + 1
				if col==2:
					worksheet.write(row, col,parse_decimal(data[col], locale='en_US'),money_format)
				else:
					worksheet.write(row, col,data[col],format1)
			row = row + 1
			row_end2 = row
		worksheet.write(row_end1, 2,"=SUM(C{}:C{})".format(row_end1+2,row_end2),money_format)
				
		for data in self.liability:
			for col in cols:
				if data[col] == '' and data[col+1] == 'Liability':
					row_end1 = row
					#row = row + 1
				if col==2:
					worksheet.write(row, col,parse_decimal(data[col], locale='en_US'),money_format)
				else:
					worksheet.write(row, col,data[col],format1)
			row = row + 1
			row_end2 = row
		worksheet.write(row_end1, 2,"=SUM(C{}:C{})".format(row_end1+2,row_end2),money_format)

		for data in self.equity:
			for col in cols:
				if data[col] == '' and data[col+1] == 'Equity':
					row_end1 = row
					#row = row + 1
				if col==2:
					worksheet.write(row, col,parse_decimal(data[col], locale='en_US'),money_format)
				else:
					worksheet.write(row, col,data[col],format1)
			row = row + 1
			row_end2 = row
		worksheet.write(row_end1, 2,"=SUM(C{}:C{})".format(row_end1+2,row_end2),money_format)


		import os,time
		time.sleep(2)
		os.system('start EXCEL.EXE {}/Documents/chart.xlsx'.format(home))
		workbook.close()
		
	def CreateNewAccount(self):
		self.addaccount=AddAccount(self,[])
		self.addaccount.show()	

	def Edit(self):
		self.editList.append('Edit')
		self.addaccount=AddAccount(self,self.editList)
		self.addaccount.show()

	def Delete(self):		
		self.dialog=QDialog(self)
		self.dialog.setWindowTitle("Delete Account")
		layout = QGridLayout()
		self.dialog.setLayout(layout)
		layout.addWidget(QLabel("\nNote that all associated (reference no.) Journal and transactions will be permanently deleted.\n Are you sure you want to delete  {} - {}?\n".\
			format(self.editList[0],self.editList[1])))

		self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		self.buttonbox.button(QDialogButtonBox.Ok).setText("Yes, Delete!")
		self.buttonbox.accepted.connect(self.DeleteRow)
		self.buttonbox.rejected.connect(self.dialog.close)
		layout.addWidget(self.buttonbox)
		self.edit.setDisabled(True)
		self.delete.setDisabled(True)
		self.dialog.exec_()

	def DeleteRow(self):
		self.editList.append('Delete')
		self.addaccount=AddAccount(self,self.editList)
		self.dialog.close()
		self.close()
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

		self.income.insert(0,['','Revenue',self.total[0] ,'Revenue','Report group'])
		self.expense.insert(0,['','Expense',self.total[1],'Expense','Report group'])
		self.asset.insert(0,['','Assets',self.total[2],'Assets','Report group'])
		self.liability.insert(0,['','Liability',self.total[3],'Liability','Report group'])
		self.equity.insert(0,['','Equity',self.total[4],'Equity','Report group'])
				
		
		headers =["   Number   ","  Name"," Balance(₦)        "," Type           ","   Report Group   "]
		
		table = """
		<style>
		table {
		font-family: arial, sans-serif;
		border-collapse: collapse;
		width: 100%;
		}

		td, th {
		border: 1px solid #dddddd;
		text-align: center;
		padding: 8px;
		}
		</style>
		<body>
		<body>
		<div style=" font-weight: bold;font-size:25px; text-align:center">
		<img source="image/report.JPG">
		   <p>FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
      	<p>Chart of Accounts<p/>
      	</div>
		<table border="1" cellSpacing="0" width="100%">
		<tr>{% for header in headers %}<th>{{header}}</th>{% endfor %}</tr>
		{% for row in income %}<tr>
		{% for element in row %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}
		{% for row in expense %}<tr>
		{% for element in row %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}
		{% for row in asset %}<tr>
		{% for element in row %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}
		{% for row in liability %}<tr>
		{% for element in row %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}
		{% for row in equity %}<tr>
		{% for element in row %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}

		</table>
		</body>
		"""
		#print(self.income)
		cursor.insertHtml(Template(table).render(headers=headers, income=self.income,expense=self.expense,asset=self.asset,liability=self.liability,equity=self.equity))	
		document.print_(printer)		
		
	def Print(self):
		self.handle_print()
	def Save(self):
		pass	
	def Mail(self):
		pass

		
	def Charts(self):

	
		self.widget=QWidget()
		self.requireddata=open("db/viewchart.json", "r")
		self.requireddata=json.load(self.requireddata)

		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		gridLayout=QGridLayout()
		self.table =QTableWidget()

		self.mainlayout.addLayout(gridLayout,1)
		self.mainlayout.addWidget(self.table,20)

		label=QLabel('Number of digits in account number:')
		lineedit=QLineEdit('  6')

		gridLayout.addWidget(label,0,0)
		gridLayout.addWidget(lineedit,0,1)

		self.AccountsTable()

	def Currency(self,currency):
		return format_currency(currency,'NGN', locale='en_US') 
	

	def AccountsTable(self):
		self.data=self.requireddata
		self.asset=self.data['assets']
		self.income=self.data['income']
		self.liability=self.data['liability']
		self.equity=self.data['equity']
		self.expense=self.data['expense']
		self.total=self.data['total']
		#print(self.income)
		
		rows=(len(self.asset)+len(self.income)+len(self.liability)+len(self.equity)+len(self.expense)+5)
		JournalHeader=["   Number   ","  Name"," Balance (₦)        "," Type           ","   Report Group   "]
		self.table.setColumnCount(5)     #Set three expense
		self.table.setRowCount(rows)
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		header = self.table.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
		self.table.resizeRowsToContents()
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(JournalHeader)

		self.table.doubleClicked.connect(self.TableAction)

		self.table.setItem(0,1, QTableWidgetItem('Revenue'))
		self.table.setItem(0,2, QTableWidgetItem((self.total[0])))
		self.table.setItem(0,3, QTableWidgetItem('Revenue'))
		self.table.setItem(0,4, QTableWidgetItem('Report group'))
		row=1
		for data in self.income:
			self.table.setItem(row,0, QTableWidgetItem(data[0]))
			self.table.setItem(row,1, QTableWidgetItem(data[1]))
			self.table.setItem(row,2, QTableWidgetItem((data[2])))
			self.table.setItem(row,3, QTableWidgetItem(data[3]))
			self.table.setItem(row,4, QTableWidgetItem(data[4]))
			row=row+1

		self.table.setItem(row,1, QTableWidgetItem('Expense'))
		self.table.setItem(row,2, QTableWidgetItem((self.total[1])))
		self.table.setItem(row,3, QTableWidgetItem('Expense'))
		self.table.setItem(row,4, QTableWidgetItem('Report group'))	
		row=row+1
		for data in self.expense:
			self.table.setItem(row,0, QTableWidgetItem(data[0]))
			self.table.setItem(row,1, QTableWidgetItem(data[1]))
			self.table.setItem(row,2, QTableWidgetItem((data[2])))
			self.table.setItem(row,3, QTableWidgetItem(data[3]))
			self.table.setItem(row,4, QTableWidgetItem(data[4]))
			row=row+1
		self.table.setItem(row,1, QTableWidgetItem('Assets'))
		self.table.setItem(row,2, QTableWidgetItem((self.total[2])))
		self.table.setItem(row,3, QTableWidgetItem('Assets'))
		self.table.setItem(row,4, QTableWidgetItem('Report group'))	
		row=row+1	
		for data in self.asset:
			self.table.setItem(row,0, QTableWidgetItem(data[0]))
			self.table.setItem(row,1, QTableWidgetItem(data[1]))
			self.table.setItem(row,2, QTableWidgetItem((data[2])))
			self.table.setItem(row,3, QTableWidgetItem(data[3]))
			self.table.setItem(row,4, QTableWidgetItem(data[4]))
			row=row+1
		self.table.setItem(row,1, QTableWidgetItem('Liability'))
		self.table.setItem(row,2, QTableWidgetItem((self.total[3])))
		self.table.setItem(row,3, QTableWidgetItem('Liability'))
		self.table.setItem(row,4, QTableWidgetItem('Report group'))	
		row=row+1
		for data in self.liability:
			self.table.setItem(row,0, QTableWidgetItem(data[0]))
			self.table.setItem(row,1, QTableWidgetItem(data[1]))
			self.table.setItem(row,2, QTableWidgetItem((data[2])))
			self.table.setItem(row,3, QTableWidgetItem(data[3]))
			self.table.setItem(row,4, QTableWidgetItem(data[4]))
			row=row+1
		self.table.setItem(row,1, QTableWidgetItem('Equity'))
		self.table.setItem(row,2, QTableWidgetItem((self.total[4])))
		self.table.setItem(row,3, QTableWidgetItem('Equity'))
		self.table.setItem(row,4, QTableWidgetItem('Report group'))	
		row=row+1
		for data in self.equity:
			self.table.setItem(row,0, QTableWidgetItem(data[0]))
			self.table.setItem(row,1, QTableWidgetItem(data[1]))
			self.table.setItem(row,2, QTableWidgetItem((data[2])))
			self.table.setItem(row,3, QTableWidgetItem(data[3]))
			self.table.setItem(row,4, QTableWidgetItem(data[4]))
			row=row+1	
		#print(data)
		
	def TableAction(self,item):
		self.editList=[]
		row=item.row()
		self.delkey= row
		no=self.table.item(row,0)
		name=self.table.item(row,1)
		bal=self.table.item(row,2)
		type_=self.table.item(row,3)
		reportg=self.table.item(row,4)
		try:
			self.editList=[no.text(),name.text(),bal.text(),type_.text(),reportg.text()]
			self.edit.setEnabled(True)
			self.delete.setEnabled(True)
			#print(self.editList)
		except Exception as e:
			pass
		
	
	

		"""blockFormat=QtGui.QTextBlockFormat()
		cursor.insertImage('image/reportp.png')
		cursor.insertBlock(blockFormat)
		blockFormat.setPageBreakPolicy(QtGui.QTextBlockFormat.PageBreak_AlwaysBefore)
		cursor.insertText('\n')
		cursor.insertText('CHART OF ACCOUNTS')
		cursor.insertText('\n')
		cursor.insertText('\n')
		table=cursor.insertTable(self.table.rowCount(),self.table.columnCount())

		for row in range(table.rows()):
			for col in range(table.columns()):
				it = self.table.item(row,col)
				if it is not None:
					cursor.insertText(it.text())
					cursor.movePosition(QtGui.QTextCursor.NextCell)
				else:
					cursor.insertText('')
					cursor.movePosition(QtGui.QTextCursor.NextCell)
		"""
		
					
		
		


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AccountsChart()
	ex.show()
	sys.exit(app.exec_())





