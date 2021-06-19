from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QTextEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency,parse_decimal
from jinja2 import Template


class AccountsEnquiry(QMainWindow):
	def __init__(self,data,date1,date2, parent=None):
		super(AccountsEnquiry, self).__init__(parent)
		self.title = 'Accounts Enquiry'
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

		self.AccountEqiuryContent()
		self.setCentralWidget(self.widget)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		BalanceSheet = mainMenu.addMenu('Accounts Enquiry')
		Journal = mainMenu.addMenu('Journal')
		help_ = mainMenu.addMenu('Help')

		preview=QAction('Preview Accounts Enquiry', self)
		preview.setShortcut('Ctrl+V')
		BalanceSheet.addAction(preview)
		print_=QAction('Print Accounts Enquiry', self)
		print_.setShortcut('Ctrl+P')
		BalanceSheet.addAction(print_)
		save=QAction('Save Accounts Enquiry', self)
		save.setShortcut('Ctrl+S')
		BalanceSheet.addAction(save)
		BalanceSheet.addSeparator()
		mail=QAction('Mail Accounts Enquiry', self)
		mail.setShortcut('Ctrl+M')
		BalanceSheet.addAction(mail)
		exit=QAction('Exit Accounts Enquiry', self)
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
		
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview Ledger', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print Ledger', self)
		self.excel= QAction(QIcon('image/icon/excel.png'), 'View in Excel', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Ledger', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Ledger', self)
		
		toolbar.addAction(self.preview)
		toolbar.addAction(self.print)
		toolbar.addAction(self.excel)
		toolbar.addAction(self.save)
		toolbar.addSeparator()
		toolbar.addAction(self.mail)
			
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

		table=json.load(open("db/enquiry.json", "r"))
		workbook = xlsxwriter.Workbook('{}/Documents/Account_enquiry.xlsx'.format(home))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1,'num_format': '#,##.00'})
		money_format1 = workbook.add_format({'bold': 1,'border':1,'num_format': '#,##.00'})

		worksheet.set_column(0, 0, 10)
		worksheet.set_column(1, 1, 30)
		worksheet.set_column(2, 5, 15)
		
		#print(pd)
		worksheet.insert_image(0, 2,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 1,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 1,'Ledger account, Journal Postings from  {date1} to {date2}'.format(date1=self.date1,date2=self.date2),bold)
		
		description_list=(self.data['description_list'])

		tables='<br>'
		#print(self.data)
		row1=8
		for desc in description_list:
			if len(self.data[desc])==0:
				return False
			first_row='top'
			acnt_no=self.data[desc][0][6]
			worksheet.write(row1, 0, "Account:"+desc+"    No.:"+acnt_no, format2)
			
			worksheet.write(row1+1, 0, "Date", format2)
			worksheet.write(row1+1, 1, "Description", format2)
			worksheet.write(row1+1, 2, "Jnl No", format2)
			worksheet.write(row1+1, 3, "Debit", format2)
			worksheet.write(row1+1, 4, "Credit", format2)
			worksheet.write(row1+1, 5, "Balance", format2)
			for row in range(len(self.data[desc])):
				
				for col in range(6):
					if  col==0:
						worksheet.write(row+10, col, self.data[desc][row][col],format1)
					if col==1:
						worksheet.write(row+10, col, self.data[desc][row][col],format1)
					if col==2:
						worksheet.write(row+10, col, self.data[desc][row][col],format1)
					if col==3:
						if self.data[desc][row][col]!="":
							worksheet.write(row+10, col, parse_decimal(self.data[desc][row][col], locale='en_US'),money_format)
						if self.data[desc][row][col]=="":
							worksheet.write(row+10, col, (self.data[desc][row][col]),format1)
					if col==4:
						if self.data[desc][row][col]!="":
							worksheet.write(row+10, col, parse_decimal(self.data[desc][row][col], locale='en_US'),money_format)
						if self.data[desc][row][col]=="":
							worksheet.write(row+10, col, (self.data[desc][row][col]),format1)
					
					if col==5 and (str(acnt_no)[0]=='2' or str(acnt_no)[0]=='3'):
						if first_row=="top":
							worksheet.write(row+10, col, '=(D{})'.format(row+11) ,money_format)
						else:
							worksheet.write(row+10, col, '=(D{} - E{} + F{})'.format(row+11,row+11,row+10) ,money_format)

					if col==5 and (str(acnt_no)[0]=='1' or str(acnt_no)[0]=='4'):
						if first_row=="top":
							worksheet.write(row+10, col, '=(E{})'.format(row+11) ,money_format)
						else:
							worksheet.write(row+10, col, '=(E{} - D{} + F{})'.format(row+11,row+11,row+10) ,money_format)

				first_row=""
				row1=row1+1
					
					
								
		import os
		os.system("start EXCEL.EXE {}/Documents/Account_enquiry.xlsx".format(home))
		workbook.close()
		
	def Preview(self):
		loaddata=open("db/enquiry.json", "r")
		self.printdata=json.load(loaddata)
		self.handlePreview()		

	def Print(self):
		loaddata=open("db/enquiry.json", "r")
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

		printdata=self.printdata
		
		

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
		   <p style="font-weight: bold;font-size:20px;">FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
      <p style="font-weight: bold;font-size:20px;">Ledger account, Journal Postings from {{date1}} to {{date2}}<p/>
      </div>
		{{data}}
		</body>
	
		"""
		cursor.insertHtml(Template(table).render(data=printdata,date1=self.date1,date2=self.date2))	
		document.print_(printer)

	def AccountEqiuryContent(self):
	
		self.widget=QWidget()
		main = QGridLayout()
		layout = QGridLayout()
		self.widget.setLayout(main)
		
		self.textedit = QTextEdit()
		self.textedit.setObjectName('EnquiryTextEdit')
		self.textedit.setReadOnly(True)
		
		main.addWidget(self.textedit)

		self.EnquiryTable()

	def EnquiryTable(self):
		
		
		description_list=(self.data['description_list'])

		tables='<br>'
		#print(self.data)
		for desc in description_list:
			if len(self.data[desc])==0:
				return False
			trows=''
		
			for row in range(len(self.data[desc])):
				date=self.data[desc][row][0]
				memo=self.data[desc][row][1]
				ref=self.data[desc][row][2]
				deb=self.data[desc][row][3]
				cre=self.data[desc][row][4]
				bal=self.data[desc][row][5]
				
				tr='''	
				<tr>
				<td  style="border: 1px solid red; text-align: left;padding: 4px;">{date}</td><td style="border: 1px solid #dddddd; text-align: left;padding: 4px;">{memo}</td>
				<td style="border: 1px solid #dddddd; text-align: left;padding: 4px;">{ref}</td><td style="border: 1px solid #dddddd; text-align: right;padding: 4px;">{deb}</td>
				<td style="border: 1px solid #dddddd; text-align: right;padding: 4px;">{cre}</td><td style="border: 1px solid #dddddd; text-align: right;padding: 4px;">{bal}</td>
				</tr>			
				'''.format(date=date,memo=memo,ref=ref,deb=deb,cre=cre,bal=bal)
				trows=trows + tr
			acct=self.data[desc][0][6]
			table= '''
				

                <table border=".3" cellSpacing="0" width="100%">
                
                <tbody>
                <caption>
                <div><p style=" font-weight: bold;font-size:20px; text-align:center">Account Ledger</p></div>
				<div><u><span style="text-align: left;font-size:20px;">Account:  {}</span><span style="text-align: right;font-size:20px;">&nbsp;&nbsp;&nbsp; Account Num:  {}</span></u></div>
		        </caption>
		        <tr><td style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;">Date</td><td style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;">Description</td>
		        <td style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;">Jnl No</td><td style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;">Debit</td>
		        <td style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;">Credit</td><td style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;">Balance</td>
		        </tr>
		          {}
		          <tbody>
		        </table><br><br>'''.format(desc,acct,trows)
			tables=tables+table
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
		                      <div>
		                      <div style=" font-weight: bold;font-size:13px; text-align:center">
		                       <img source="image/report.JPG">
                  			   <p>FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
		                      <p>Ledger account, Journal Postings from {date1} to {date2}<p/>
		                      </div>
		                        {table}
		                      </div>  
		                      </body>
		                      </html>
					'''.format(table=tables,date1=self.date1,date2=self.date2)

		self.textedit.insertHtml('<br>'+ fulltable)
		printdata=open("db/enquiry.json", "w")
		json.dump(tables, printdata)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AccountsEnquiry()
	ex.show()
	sys.exit(app.exec_())
