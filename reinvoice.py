from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QTextEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency
from jinja2 import Template




class InvoiceRe(QMainWindow):
	def __init__(self,data,date1,date2, parent=None):
		super(InvoiceRe, self).__init__(parent)
		self.title = 'Invoice Report'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.data=data
		self.date1=date1
		self.date2=date2
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.InvoiveContent()
		self.setCentralWidget(self.widget)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		BalanceSheet = mainMenu.addMenu('General Invoive')
		Journal = mainMenu.addMenu('Journal')
		help_ = mainMenu.addMenu('Help')

		preview=QAction('Preview General Invoive', self)
		preview.setShortcut('Ctrl+V')
		BalanceSheet.addAction(preview)
		print_=QAction('Print General Invoive', self)
		print_.setShortcut('Ctrl+P')
		BalanceSheet.addAction(print_)
		save=QAction('Save General Invoive', self)
		save.setShortcut('Ctrl+S')
		BalanceSheet.addAction(save)
		BalanceSheet.addSeparator()
		mail=QAction('Mail General Invoive', self)
		mail.setShortcut('Ctrl+M')
		BalanceSheet.addAction(mail)
		exit=QAction('Exit General Invoive', self)
		exit.setShortcut('Ctrl+Q')
		BalanceSheet.addAction(exit)

		addjournal=QAction('Add Journal', self)
		Journal.addAction(addjournal)
		viewjournal=QAction('View journal', self)
		viewjournal.setShortcut('Ctrl+ V')
		Journal.addAction(viewjournal)
		 
		#Findnextbutton.setDisabled(True)
		self.statusBar()
			
		toolbar = self.addToolBar('tool bar')
		toolbar.setObjectName('toolbar')
		
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview Invoive', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print Invoive', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Invoive', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Invoive', self)
		
		toolbar.addAction(self.preview)
		toolbar.addAction(self.print)
		toolbar.addAction(self.save)
		toolbar.addSeparator()
		toolbar.addAction(self.mail)
			
		self.preview.triggered.connect(self.Preview)
		self.print.triggered.connect(self.Print)
		self.save.triggered.connect(self.Save)
		self.mail.triggered.connect(self.Mail)

	def Preview(self):
		loaddata=open("db/InvoiceRe.json", "r")
		self.printdata=json.load(loaddata)
		self.handlePreview()		

	def Print(self):
		loaddata=open("db/InvoiceRe.json", "r")
		self.printdata=json.load(loaddata)
		#from print import handlePreview
		self.handle_print()
	def Save(self):
		pass	
	def Mail(self):
		pass



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

		
		headers =["Date","Invoice","Customer","Salesperson","status","Tax","Amount"]
		data=self.printdata['invoicedata']
		
		total=self.printdata['total']
		key=sorted(data)
		
		

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
      <p>Invoice Report<p/>
      </div>
      <div style="font-size:13px; text-align:left">
      <p>Invoices Report<br>Period:{{date1}} to {{date2}} <p/>
     </div>

      <div style="font-size:13px; text-align:right">
      <p style=color:"">Number of Invoices: {{invoiceno}}<br>Total Amount: {{total[1]}} <p/>
      </div>
		<table border=".3" cellSpacing="0" width="100%">
		<tr>{% for header in headers %}<th>{{header}}</th>{% endfor %}</tr>
		{% for row in key %}<tr>
		{% for element in data[row] %}<td>
		{{element}}
		</td>{% endfor %}
		</tr>{% endfor %}
		<tr><td></td><td></td><td></td><td></td><td></td><td>{{total[0]}}</td><td>{{total[1]}}</td>
		</tr>
		

		</table>
		"""
		cursor.insertHtml(Template(table).render(headers=headers,key=key,data=data,total=total,date1=self.date1,date2=self.date2,invoiceno=self.invoiceno))	
		document.print_(printer)

	def InvoiveContent(self):
		self.widget=QWidget()
		main = QGridLayout()
		self.widget.setLayout(main)
		layout = QGridLayout()
		self.setLayout(main)
		
		self.textedit = QTextEdit()
		self.textedit.setObjectName('InvoiveTextEdit')
		self.textedit.setReadOnly(True)
		
		main.addWidget(self.textedit)

		self.GeneralInvoive()

	def GeneralInvoive(self):
		
		self.invoicedata=self.data['invoicedata']
		self.invoiceno=len(self.invoicedata)
		trows=''
		
		totalamount=self.data['total'][1]
		for row in sorted(self.invoicedata):
			date=self.invoicedata[row][0]
			invoice=self.invoicedata[row][1]
			customer=self.invoicedata[row][2]
			salesperson=self.invoicedata[row][3]
			status=self.invoicedata[row][4]
			tax=self.invoicedata[row][5]
			amount=self.invoicedata[row][6]

		
			
			tr='''	
			<tr>
			<td  style="border: 1px solid red; text-align: left;padding: 8px;">{date}</td><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;">{invoice}</td>
			<td style="border: 1px solid #dddddd; text-align: left;padding: 8px;">{customer}</td><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;">{salesperson}</td>
			<td style="border: 1px solid #dddddd; text-align: left;padding: 8px;">{status}</td><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;">{tax}</td>
			<td style="border: 1px solid #dddddd; text-align: left;padding: 8px;">{amount}</td>
			</tr>			
			'''.format(date=date,invoice=invoice,customer=customer,salesperson=salesperson,status=status,tax=tax,amount=amount)
			trows=trows + tr
			
		table= '''
			
             <table border=".3" cellSpacing="0" width="100%">
            <tbody>
	        <tr><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Date</td><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Invoice</td>
	        <td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Customer</td><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Salesperson</td>
	        <td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Status</td><td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Tax</td>
	        <td style="border: 1px solid #dddddd; text-align: left;padding: 8px;font-weight: bold;">Amount</td>
	        </tr>
	          {}
	          <tbody>
	        </table><br><br>'''.format(trows)
			
			#print(table)
		fulltable='''

							<!DOCTYPE html>
		                      <html>
		                      <head>
		                      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		                        <title></title>
		                        <style type="text/css">
		                        
		                        </style>
		                      </head>
		                      <body style="margin-left: 150px;margin-right: 150px">
		                      <div style=" font-weight: bold;font-size:13px; text-align:center">
						       <img source="image/report.JPG">
								   <p>FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
						      <p>Invoice Report<p/>
						      </div>

		                     <div style="font-size:13px; text-align:left">
		                      <p>Invoices Report<br>Period:{date1} to {date2} <p/>
		                     </div>

		                      <div style="font-size:13px; text-align:right">
		                      <p style=color:"">Number of Invoices: {invoiceno}<br>Total Amount: {totalamount} <p/>
		                      </div>

		                        {table}
		                      </div>  
		                      </body>
		                      </html>
					'''.format(table=table,date1=self.date1,date2=self.date2,invoiceno=self.invoiceno,totalamount=totalamount)

		self.textedit.insertHtml('<br>'+ fulltable)
		printdata=open("db/InvoiceRe.json", "w")
		json.dump(self.data, printdata)		
	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = InvoiceRe()
	ex.show()
	sys.exit(app.exec_())
