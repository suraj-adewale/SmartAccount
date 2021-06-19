from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QTextEdit
from PyQt5 import QtWidgets
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency
from jinja2 import Template


class TrialBalance(QMainWindow):
	def __init__(self,data,date1,date2, parent=None):
		super(TrialBalance, self).__init__(parent)
		self.title = 'Trial Balance'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.date1=date1
		self.date2=date2
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.content =TrialBalanceContent(data,date1,date2)
		self.setCentralWidget(self.content)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		BalanceSheet = mainMenu.addMenu('Trial Balance')
		Journal = mainMenu.addMenu('Journal')
		help_ = mainMenu.addMenu('Help')

		preview=QAction('Preview Trial Balance', self)
		preview.setShortcut('Ctrl+V')
		BalanceSheet.addAction(preview)
		print_=QAction('Print Trial Balance', self)
		print_.setShortcut('Ctrl+P')
		BalanceSheet.addAction(print_)
		save=QAction('Save Trial Balance', self)
		save.setShortcut('Ctrl+S')
		BalanceSheet.addAction(save)
		BalanceSheet.addSeparator()
		mail=QAction('Mail Trial Balance', self)
		mail.setShortcut('Ctrl+M')
		BalanceSheet.addAction(mail)
		exit=QAction('Exit Trial Balance', self)
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
		
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Preview Trial Balance', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Print Trial Balance', self)
		self.excel= QAction(QIcon('image/icon/excel.png'), 'View in Excel', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Trial Balance', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Trial Balance', self)
		
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

		table=json.load(open("db/print_trialbalnce.json", "r"))
		workbook = xlsxwriter.Workbook('{}/Documents/TrialBalance_{} to {}.xlsx'.format(home,self.date1,self.date2))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1,'num_format': '#,##.00'})
		money_format1 = workbook.add_format({'bold': 1,'border':1,'num_format': '#,##.00'})

		worksheet.set_column(0, 0, 35)
		worksheet.set_column(1, 2, 15)
		

		pd=(pd.read_html(table))[0]
		pd=pd.fillna('')
		
		#print(pd)
		worksheet.insert_image(1, 1,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 1,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 1,'Trial Balance Account from {date1} to {date2}'.format(date1=self.date1,date2=self.date2),bold)
		row_end1=0
		row_end2=0
		for index,row in pd.iterrows():
			for col in pd.columns:
				if  col==0:
					worksheet.write(index+7, col,row[col],format1)
					if row[col]== "Description":
						worksheet.write(index+7, col,row[col],format2)
					if row[col]== "Total":
						worksheet.write(index+7, col,row[col],format2)
						row_end2=index+7	
					
				if col==1:
					if row[col] == "":
						worksheet.write(index+7, col,row[col],format1)
					if row[col]== "Debit(NGN)":
						worksheet.write(index+7, col,row[col],format2)
					if row[col] != "" and  row[col] != "Debit(NGN)":
						worksheet.write(index+7, col,float(row[col]), money_format)	
					if row_end2==index+7:
						worksheet.write(index+7,col, '=SUM(B{}:B{})'.format(9,index+7), money_format1)
								
				if col==2:
					if row[col] == "":
						worksheet.write(index+7, col,row[col],format1)
					if row[col]== "Credit(NGN)":
						worksheet.write(index+7, col,row[col],format2)
					if row[col] != "" and  row[col] != "Credit(NGN)":
						worksheet.write(index+7, col,float(row[col]), money_format)		
					if row_end2==index+7:
						worksheet.write(index+7,col, '=SUM(C{}:C{})'.format(9,index+7), money_format1)	
								
		import os
		os.system("start EXCEL.EXE {}/Documents/TrialBalance_{} to {}.xlsx".format(home,self.date2,self.date2))
		workbook.close()
		
	def Preview(self):
		loaddata=open("db/print_trialbalnce.json", "r")
		self.printdata=json.load(loaddata)
		self.handlePreview()		

	def Print(self):
		loaddata=open("db/print_trialbalnce.json", "r")
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
		print(printdata)
		
		

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
	      <p>Nominal Ledger account, Journal Postings from {{date1}} to {{date2}}<p/>
	      </div>
		<br>
		{{data}}
		</body>
		"""
		cursor.insertHtml(Template(table).render(data=printdata,date1=self.date1,date2=self.date2))	
		document.print_(printer)

class TrialBalanceContent(QWidget):
	
	def __init__(self,data,date1,date2):
		super(QWidget, self).__init__()
		self.data=data
		self.date1=date1
		self.date2=date2
	
		main = QGridLayout()
		layout = QGridLayout()
		self.setLayout(main)
		
		self.textedit = QTextEdit()
		self.textedit.setObjectName('LedgerTextEdit')
		self.textedit.setReadOnly(True)
		
		main.addWidget(self.textedit)
		self.LoadTrialBalance()

	def LoadTrialBalance(self):
			
		
		description_list=(self.data['description_list'])
		tables='<br>'
		trows=''
		style="border: 1px solid #dddddd; text-align: left;padding: 4px;font-weight: bold;"
		style1="border: 1px solid #dddddd; text-align: right;padding: 4px;font-weight: bold;"
		for desc in description_list:
			if self.data[desc][0] is not '':
				debit=str(format_currency(float(self.data[desc][0]),'', locale='en_US'))
			else:
				debit=self.data[desc][0]
			if self.data[desc][1] is not '':
				credit=str(format_currency(float(self.data[desc][1]),'', locale='en_US'))
			else:
				credit=self.data[desc][1]		
			

			
			tr='''
			<tr>
			<td  style="border: 1px solid #dddddd;text-align: left;padding: 3px;">{}</td>
			<td style="border: 1px solid #dddddd; text-align: right;padding: 3px;">{}</td>
			<td style="border: 1px solid #dddddd; text-align: right;padding: 3px;">{}</td>
			</tr>
			'''.format(desc,debit,credit)
			trows=trows + tr	

		total_cr=self.data['bal'][0]
		total_de=self.data['bal'][1]
		naira=str(format_currency(0,'NGN', locale='en_US'))
		naira.split('0')
		naira=naira[0]
			
		table= '''
				
                <table border=".3" cellSpacing="0" width="100%">
                
                <tbody>
		        <tr>
		        <td style="{style}">Description</td>
		        <td style="{style1}">Debit({naira})</td>
		        <td style="{style1}">Credit({naira})</td>
		        </tr>
		          {rows}
		         <tr>
		        <td style="{style}">Total</td>
		        <td style="{style1}">{de}</td>
		        <td style="{style1}">{cr}</td>
		        </tr> 
		          <tbody>
		        </table><br><br>'''.format(style=style,style1=style1,naira='NGN',rows=trows, de=total_de,cr=total_cr)

		html='''

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
			      <p>Trial Balance Account from {date1} to {date2}<p/>
			      </div>
                    {table}
                  </div>  
                  </body>
                  </html>
					'''.format(table=table,date1=self.date1,date2=self.date2)        	
		self.textedit.insertHtml('<br>'+html )			
		printdata=open("db/print_trialbalnce.json", "w")
		json.dump(table, printdata)
	
					
				
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = TrialBalance()
	ex.show()
	sys.exit(app.exec_())




