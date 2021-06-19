from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QTextEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency
from jinja2 import Template




class Income(QMainWindow):
	def __init__(self,data,date1,date2, parent=None):
		super(Income, self).__init__(parent)
		self.title = 'General Income'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.date1=date1
		self.date2=date2
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.content =IncomeContent(data,date1,date2)
		self.setCentralWidget(self.content)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		BalanceSheet = mainMenu.addMenu('Income')
		Journal = mainMenu.addMenu('Journal')
		help_ = mainMenu.addMenu('Help')

		preview=QAction('Preview Income', self)
		preview.setShortcut('Ctrl+V')
		BalanceSheet.addAction(preview)
		print_=QAction('Print General Ledger', self)
		print_.setShortcut('Ctrl+P')
		BalanceSheet.addAction(print_)
		save=QAction('Save General Ledger', self)
		save.setShortcut('Ctrl+S')
		BalanceSheet.addAction(save)
		BalanceSheet.addSeparator()
		mail=QAction('Mail General Ledger', self)
		mail.setShortcut('Ctrl+M')
		BalanceSheet.addAction(mail)
		exit=QAction('Exit General Ledger', self)
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
		table=json.load(open("db/print_generalledger.json", "r"))
		workbook = xlsxwriter.Workbook('{}/Documents/income.xlsx'.format(home))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1,'num_format': '#,##.00'})

		worksheet.set_column(0, 0, 15)
		worksheet.set_column(1, 1, 35)
		worksheet.set_column(2, 4, 15)

		pd=(pd.read_html(table))[0]
		pd=pd.fillna('')
		
		#print(pd)
		worksheet.insert_image(1, 2,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 1,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 1,'Income Statement from {date1} to {date2}'.format(date1=self.date1,date2=self.date2),bold)
		row_end1=0
		row_end2=0
		for index,row in pd.iterrows():
			for col in pd.columns:
				if  col==0:
					worksheet.write(index+7, col,row[col],format2)
				if col==1:
					worksheet.write(index+7, col,row[col],format1)
				if col==2:
					if row[col]=="Total Revenues":
						row_end1=index+7
					if row[col]=="Total Expenses":
						row_end2=index+7
					worksheet.write(index+7, col,row[col],format2)	
				if col==3:
					worksheet.write(index+7, col,row[col],money_format)
				if col==4:
					worksheet.write(index+7, col,row[col],format2)
					if row_end1==index+7:
						Total_Revenue = 'SUM(D{}:D{})'.format(9,index+7)
						worksheet.write(index+7, col,'={}'.format(Total_Revenue), money_format)
					if row_end2==index+7:
						Total_Expense = 'SUM(D{}:D{})'.format(row_end1+3,index+7)
						worksheet.write(index+7, col,'={}'.format(Total_Expense), money_format)
					
					if row_end2+1==index+7:
						print(index+7, col)
						worksheet.write_formula(index+7, col,"={} - {}".format(Total_Revenue,Total_Expense,Total_Expense), money_format)
					
		#existingws=workbook.get_worksheet_by_name("jcdjjkd")	
		import os
		os.system("start EXCEL.EXE {}/Documents/income.xlsx".format(home))
		workbook.close()

	def Preview(self):
		self.printdata=json.load(open("db/print_generalledger.json", "r"))
		self.handlePreview()		

	def Print(self):
		self.printdata=json.load(open("db/print_generalledger.json", "r"))
		#from print import handlePreview
		self.handle_print()
	def Save(self):
		pass	
	def Mail(self):
		pass



	def handlePreview(self):
		printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
		dialog = QtPrintSupport.QPrintPreviewDialog(printer)
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
		padding: 3px;
		}
		</style>
		<body>
		<div style="text-align:center">
          <img source="image/report.JPG">
		   <p >FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
          <p>Income Statement from {{date1}} to {{date2}}<p/>
      </div>
		{{data}}
		</body>
		"""
		cursor.insertHtml(Template(table).render(data=printdata,date1=self.date1,date2=self.date2))	
		document.print_(printer)

class IncomeContent(QWidget):
	
	def __init__(self, data,date1,date2):
		super(QWidget, self).__init__()
		main = QGridLayout()
		layout = QGridLayout()
		self.setLayout(main)
		self.data=data
		self.date1=date1
		self.date2=date2
		self.textedit = QTextEdit()
		self.textedit.setObjectName('LedgerTextEdit')
		self.textedit.setReadOnly(True)
		
		main.addWidget(self.textedit)

		self.GeneralLedger()

	def Currency(self,currency):
		return format_currency(currency,'', locale='en_US')

	def GeneralLedger(self):
		
		revenue=(self.data['revenue'])
		expense=(self.data['expense']) 
		revenuelen=len(self.data['revenue'])
		expenselen=len(self.data['expense'])
		tables='<br>'
		rows1='<tr><td><i><b>Revenues</b></i></td><td></td><td></td></tr>'
		rows2='<tr><td><i><b>Expenses</b></i></td><td></td><td></td></tr>'
		
		for row in revenue:
			count1=0
			if count1==revenuelen:
				tr='''	
				<tr>
				<td></td><td  style="border: 1px solid red; text-align: left;padding: 4px;">{desc}</td><td></td><td style="border: 1px solid #dddddd; text-align: right;padding: 4px;"><u>{amt}</u></td>
				</tr>			
				'''.format(desc=row, amt=format_currency(revenue[row],'', locale='en_US'))
			else:	
				tr='''	
				<tr>
				<td></td><td  style="border: 1px solid red; text-align: left;padding: 4px;">{desc}</td><td></td><td style="border: 1px solid #dddddd; text-align: right;padding: 4px;">{amt}</td>
				</tr>			
				'''.format(desc=row, amt=format_currency(revenue[row],'', locale='en_US'))
			rows1=rows1 + tr
		count2=0	
		for row in expense:
			count2+=1
			if count2==expenselen:
				tr='''	
				<tr>
				<td></td><td style="border: 1px solid red; text-align: left;padding: 4px;">{desc}</td><td></td><td style="border: 1px solid #dddddd; text-align: right;padding: 4px;"><u>{amt}</u></td>
				</tr>			
				'''.format(desc=row, amt=format_currency(expense[row],'', locale='en_US'))
			else:
				tr='''	
				<tr>
				<td></td><td style="border: 1px solid red; text-align: left;padding: 4px;">{desc}</td><td></td><td style="border: 1px solid #dddddd; text-align: right;padding: 4px;">{amt}</td>
				</tr>			
				'''.format(desc=row, amt=format_currency(expense[row],'', locale='en_US'))
			rows2+=tr
		rows1+='<tr><td></td><td></td><td><b>Total Revenues</b><td></td><td style="text-align:right;"><u>{}</u></td></tr>'.format(format_currency(sum(revenue.values()),'', locale='en_US'))	
		rows2+='<tr><td></td><td></td><td><b>Total Expenses</b><td></td><td style="text-align:right;"><u>{}</u></td></tr>'.format(format_currency(sum(expense.values()),'', locale='en_US'))
		rows=rows1+rows2

		net=self.data['net']
		if net > 0:
			sur_defi = "Surplus"
		else:
			sur_defi = "Deficit"	

		rows+='<tr><td><b>{}</b></td><td></td><td></td><td></td><td style="text-align:right;"><u><b>{}</b></u></td></tr>'.format(sur_defi,self.Currency(net))
		table= '''  
			<table border=".3" cellSpacing="0" width="100%">          
            <tbody>
	        {}
	        <tbody>
	        </table><br><br>'''.format(rows)
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
                  <p>Income Statement from {date1} to {date2}<p/>
                  </div>
                    {table}
                  </div>  
                  </body>
                  </html>
		'''.format(table=tables,date1=self.date1,date2=self.date2)

		self.textedit.insertHtml('<br>'+ fulltable)	
		
		json.dump(tables, open("db/print_generalledger.json", "w"))		
	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Income()
	ex.show()
	sys.exit(app.exec_())
