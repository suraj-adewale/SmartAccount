from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QTextEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency
from jinja2 import Template



class BalanceSheet(QMainWindow):
	def __init__(self, data,date1,date2, parent=None):
		super(BalanceSheet, self).__init__(parent)
		self.title = 'Balance Sheet'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.date1=date1
	
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.content =BalanceSheetContent(data,date1,date2)
		self.setCentralWidget(self.content)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		BalanceSheet = mainMenu.addMenu('Balance Sheet')
		Journal = mainMenu.addMenu('Journal')
		help_ = mainMenu.addMenu('Help')

		preview=QAction('Preview Balance Sheet', self)
		preview.setShortcut('Ctrl+V')
		BalanceSheet.addAction(preview)
		print_=QAction('Print Balance Sheet', self)
		print_.setShortcut('Ctrl+P')
		BalanceSheet.addAction(print_)
		save=QAction('Save Balance Sheet', self)
		save.setShortcut('Ctrl+S')
		BalanceSheet.addAction(save)
		BalanceSheet.addSeparator()
		mail=QAction('Mail Balance Sheet', self)
		mail.setShortcut('Ctrl+M')
		BalanceSheet.addAction(mail)
		exit=QAction('Exit Balance Sheet', self)
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
		
		self.preview= QAction(QIcon('image/icon/preview.ico'), 'Balance Sheet', self)
		self.print= QAction(QIcon('image/icon/hp_printer.png'), 'Balance Sheet', self)
		self.excel= QAction(QIcon('image/icon/excel.png'), 'View in Excel', self)
		self.save= QAction(QIcon('image/icon/save.ico'), 'Save Balance Sheet', self)
		self.mail= QAction(QIcon('image/icon/mail.ico'), 'Mail Balance Sheet', self)
		
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
		table=json.load(open("db/print_balancesheet.json", "r"))
		workbook = xlsxwriter.Workbook('{}/Documents/balsheet.xlsx'.format(home))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1,'num_format': '#,##.00'})

		worksheet.set_column(0, 0, 35)
		worksheet.set_column(1, 2, 15)
		

		pd=(pd.read_html(table))[0]
		pd=pd.fillna('')
		
		#print(pd)
		worksheet.insert_image(1, 2,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 1,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 1,'STATEMENT OF FINANCIAL POSITION AS AT {date1}'.format(date1=self.date1),bold)
		row1=0
		row2=0
		total=total1=total2=net1=net2=net=eq1=eq2=0
		for index,row in pd.iterrows():
			for col in pd.columns:
				if  col==0:
					
					if row[col]=="Current Assets":
						row1=index+7
					if row[col]=="Total Current Assets":
						total1=row2=index+7

					if row[col]=="Non-Current Assets":
						row1=index+7
					if row[col]=="Total Non-Current Assets":
						total2=row2=index+7

					if row[col]=="Total Assets":
						total=index+7
						net1=index+7
					if row[col]=="LIABILITIES":
						pass

					if row[col]=="Current Liabilities":
						row1=index+7
					if row[col]=="Total Current Liabilities":
						total1=row2=index+7

					if row[col]=="Non-Current Liabilities":
						row1=index+7
					if row[col]=="Total Non-Current Liabilities":
						total2=row2=index+7

					if row[col]=="Total Liabilities":
						total=index+7
						net2=index+7

					if row[col]=="Net Assets":
						net=index+7

					if row[col]=="NET ASSETS/EQUITY":
						eq1=index+7
					if row[col]=="Total Net Assets/Equity":
						eq2=index+7
																		
					worksheet.write(index+7, col,row[col],format2)
				if col==1:
					worksheet.write(index+7, col,row[col],format1)
				if col==2:
					if row2==index+7:
						worksheet.write(index+7,col, "=SUM(C{}:C{})".format(row1+2,row2),money_format)
					elif total==index+7:
						worksheet.write(index+7,col, "=(C{}+C{})".format(total1+1,total2+1),money_format)
					elif net==index+7:
						worksheet.write(index+7,col, "=(C{}-C{})".format(net1+1,net2+1),money_format)
					elif eq2==index+7:
						worksheet.write(index+7,col, "=SUM(C{}:C{})".format(eq1+2,eq2-1),money_format)
					else:
						worksheet.write(index+7, col,row[col],money_format)	
					
					
		#existingws=workbook.get_worksheet_by_name("jcdjjkd")	
		import os
		os.system("start EXCEL.EXE {}/Documents/balsheet.xlsx".format(home))
		workbook.close()

		
	def Preview(self):
		loaddata=open("db/print_balancesheet.json", "r")
		self.printdata=json.load(loaddata)
		self.handlePreview()		

	def Print(self):
		loaddata=open("db/print_balancesheet.json", "r")
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
		padding: 8px;
		}
		</style>
		<body>
		<div style="text-align:center">
       <img source="image/report.JPG">
		   <p style="font-weight: bold;font-size:18px;">EDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
      <p style="font-weight: bold;font-size:18px;">STATEMENT OF FINANCIAL POSITION AS AT {{date}}<p/>
      </div>
		<br>
		{{data}}
		</body>
		"""
		cursor.insertHtml(Template(table).render(data=printdata,date=self.date1))	
		document.print_(printer)		

			

class BalanceSheetContent(QWidget):
	
	def __init__(self,data,date1,date2):
		super(QWidget, self).__init__()
		main = QGridLayout()
		layout = QGridLayout()
		self.setLayout(main)
		self.data=data
		self.date1=date1
		self.date2=date2
	
		self.textedit = QTextEdit()
		self.textedit.setObjectName('balsheetTextEdit')
		self.textedit.setReadOnly(True)
		
		main.addWidget(self.textedit)
		self.LoadBalanceSheet()

	def Currency(self,currency):
		return format_currency(currency,'', locale='en_US') 

	def LoadBalanceSheet(self):
		
		r1=float(self.data.get('CashAndCashEquivalents', '0'))
		r2=float(self.data.get('Receivables', '0'))
		r3=float(self.data.get('Prepayments', '0'))
		r4=float(self.data.get('Inventories', '0'))
		tca=(r1+r2+r3+r4)

		r5=float(self.data.get('LongTermLoans', '0'))
		r6=float(self.data.get('Investments', '0'))
		r7=float(self.data.get('PropertyPlantEquipment', '0'))
		r8=float(self.data.get('InvestmentProperty', '0'))
		r9=float(self.data.get('IntangibleAssets', '0'))
		r22=float(self.data.get('ACCUMULATED', '0'))
		tnca=(r5+r6+r7+r8+r9 -r22)

		ta=tca+tnca
		r10=float(self.data.get('Deposits', '0'))
		r11=float(self.data.get('ShortTermLoansDebts', '0'))
		r12=float(self.data.get('UnremittedDeductions', '0'))
		r13=float(self.data.get('Payables', '0'))
		r15=float(self.data.get('CurrentPortionofBorrowings', '0'))
		tcl=(r10+r11+r12+r13+r15)

		r16=float(self.data.get('PublicFunds', '0'))
		r17=float(self.data.get('LongTermProvisions', '0'))
		r18=float(self.data.get('LongTermBorrowing', '0'))
		tncl=(r16+r17+r18)
		tl=tcl+tncl
		
		netAssets=ta-tl
		

		r19=int(self.data.get('CapitalGrant', '0'))
		r20=int(self.data.get('Reserves', '0'))
		r21=int(self.data.get('AccumulatedSurpluses', '0'))
		
		retainedEarnings=int(self.data.get('RetainedEarnings', '0'))
		netEquity=(r19+r20+r21+retainedEarnings)

			
		style='border: 1px solid #dddddd; text-align: left;padding: 4px;'
		style1='border: 1px solid #dddddd; text-align: right;padding: 4px;'
		
		table= '''
				
                <table border=".3" cellSpacing="0" width="100%">
                
                <tbody>
                <tr>
		        <td style="{style}"></td><td style="{style}"><b>NCOA CODES</b></td><td style="{style}"><b>2019</b></td>
		        </tr>
		        
		        <tr>
		        <td style="{style}"><u><b style="font-size:12px;">ASSETS</b></u></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Current Assets</b></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}">Cash and Cash Equivalents</td><td style="{style}">310101 - 310201</td><td style="{style1}">{r1}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Receivables </td><td style="{style}">310601 - 310604</td><td style="{style1}">{r2}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Prepayments</td><td style="{style}">310801</td><td style="{style1}">{r3}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Inventories</td><td style="{style}">310501 & 310502</td><td style="{style1}">{r4}</td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Current Assets</b></td><td style="{style}"></td><td style="{style1}"><b>{tca}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Non-Current Assets</b></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}">Long Term Loans</td><td style="{style}">311001 & 311002</td><td style="{style1}">{r5}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Investments</td><td style="{style}">310901 & 310902</td><td style="{style1}">{r6}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Property, Plant & Equipment</td><td style="{style}">320101 - 320110</td><td style="{style1}">{r7}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Investment Property</td><td style="{style}">320201</td><td style="{style1}">{r8}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Intangible Assets</td><td style="{style}">320301</td><td style="{style1}">{r9}</td>
		        </tr>
		        <tr>
		        <td style="{style}">ACCUMULATED.</td><td style="{style}">440101 - 440406</td><td style="{style1}">-{acculated}</td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Non-Current Assets</b></td><td style="{style}"></td><td style="{style1}"><b>{tnca}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Assets</b></td><td style="{style}"></td><td style="{style1}"><b>{ta}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><u><b style="font-size:12px;">LIABILITIES</b></u></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Current Liabilities</b></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}">Deposits</td><td style="{style}">410101</td><td style="{style1}">{r10}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Short Term Loans & Debts</td><td style="{style}">410201</td><td style="{style1}">{r11}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Unremitted Deductions</td><td style="{style}">410301 - 410302</td><td style="{style1}">{r12}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Payables</td><td style="{style}">410401 & 410501</td><td style="{style1}">{r13}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Short Term Provisions</td><td style="{style}">NA</td><td style="{style1}">{r14}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Current Portion of Borrowings</td><td style="{style}">410601</td><td style="{style1}">{r15}</td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Current Liabilities</b></td><td style="{style}"></td><td style="{style1}"><b>{tcl}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Non-Current Liabilities</b></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}">Public Funds</td><td style="{style}">420101 & 420102</td><td style="{style1}">{r16}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Long Term Provisions</td><td style="{style}">420201</td><td style="{style1}">{r17}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Long Term Borrowings</td><td style="{style}">420301</td><td style="{style1}">{r18}</td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Non-Current Liabilities</b></td><td style="{style}"></td><td style="{style1}"><b>{tncl}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Liabilities</b></td><td style="{style}"></td><td style="{style1}"><b>{tl}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Net Assets</b></td><td style="{style}"></td><td style="{style1}"><u><b>{netasset}</b></u></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><u><b style="font-size:12px;">NET ASSETS/EQUITY</b></u></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}">Capital Grant</td><td style="{style}">430101</td><td style="{style1}">{r19}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Reserves</td><td style="{style}">430301</td><td style="{style1}">{r20}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Accumulated Surpluses</td><td style="{style}">430201</td><td style="{style1}">{r21}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Minority Interest</td><td style="{style}">NA</td><td style="{style1}">{r22}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Retained Earnings</td><td style="{style}"></td><td style="{style1}">{re}</td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b style="font-size:12px;">Total Net Assets/Equity</b></td><td style="{style}"></td><td style="{style1}"><u><b>{netEquity}</b></u></td>
		        </tr>
		        
		         
		          <tbody>
		        </table><br><br>'''.format(style=style,style1=style1,\
		        	r1=self.Currency(r1),r2=self.Currency(r2),r3=self.Currency(r3),r4=self.Currency(r4),tca=self.Currency(tca)\
		        	,r5=self.Currency(r5),r6=self.Currency(r6), r7=self.Currency(r7),r8=self.Currency(r8),r9=self.Currency(r9),\
		        	tnca=self.Currency(tnca),ta=self.Currency(ta),r10=self.Currency(r10), r11=self.Currency(r11),r12=self.Currency(r12),r13=self.Currency(r13),r14='',\
		        	r15=self.Currency(r15),tcl=self.Currency(tcl) ,r16=self.Currency(r16),r17=self.Currency(r17),r18=self.Currency(r18),\
		        	tncl=self.Currency(tncl),tl=self.Currency(tl),netasset=self.Currency(netAssets),r19=self.Currency(r19),r20=self.Currency(r20)\
		        	,r21=self.Currency(r21),acculated=self.Currency(r22),r22='',re=self.Currency(retainedEarnings),netEquity=self.Currency(netEquity))

		        
		html='''

				<!DOCTYPE html>
                  <html>
                  <head>
                  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <title></title>
                    <style type="text/css">
                    
                    </style>
                  </head>
                  <body style="margin-left: 200px;margin-right: 200px">
                  <div>
                  <div style=" font-weight: bold;font-size:13px; text-align:center">
                  <img source="image/report.JPG">
                  <p>FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
                  <p>STATEMENT OF FINANCIAL POSITION AS AT {date1}<p/>
                  </div>
                    {table}
                  </div>  
                  </body>
                  </html>
					'''.format(table=table,date1=self.date1)        	
		self.textedit.insertHtml('<br>'+html )			
		printdata=open("db/print_balancesheet.json", "w")
		json.dump(table, printdata)
	
				
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = BalanceSheet()
	ex.show()
	sys.exit(app.exec_())




