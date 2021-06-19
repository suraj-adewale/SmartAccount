from PyQt5.QtWidgets import QMainWindow,QAction,QTabWidget,QCalendarWidget,QTableWidget,QAbstractItemView, QApplication,QDialog, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup,QTextEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency
from jinja2 import Template



class FinPerformance(QMainWindow):
	def __init__(self, data,date1,date2, parent=None):
		super(FinPerformance, self).__init__(parent)
		self.title = 'Balance Sheet'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.date1=date1
	
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.content =PerformanceContent(data,date1,date2)
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

		table=json.load(open("db/print_balancesheet.json", "r"))
		workbook = xlsxwriter.Workbook('excel.xlsx')
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		format1 = workbook.add_format({'border':1})
		format2 = workbook.add_format({'bold': 1,'border':1})
		money_format = workbook.add_format({'border':1,'num_format': '#,##.00'})

		worksheet.set_column(0, 0, 35)
		worksheet.set_column(1, 2, 25)
		

		pd=(pd.read_html(table))[0]
		pd=pd.fillna('')
		
		#print(pd)
		worksheet.insert_image(1, 1,"image/report.JPG", {'x_scale':3,'y_scale':3})
		worksheet.write(5, 1,'FEDERAL COLLEGE OF AGRICULTURE, AKURE',bold)
		worksheet.write(6, 1,'STATEMENT OF FINANCIAL PERFORMANCE AS AT {date1}'.format(date1=self.date1),bold)
		row1=0
		row2=0
		total=a=b=c=d=e=f=g=row_=0
		for index,row in pd.iterrows():
			for col in pd.columns:
				if  col==0:
					worksheet.write(index+7, col,row[col],format1)
					
					if row[col]=="REVENUE":
						worksheet.write(index+7, col,row[col],format2)
						row_=row1=index+7
					if row[col]=="Total Revenue(a)":
						worksheet.write(index+7, col,row[col],format2)
						a=row2=index+7

					if row[col]=="EXPENDITURE":
						worksheet.write(index+7, col,row[col],format2)
						row1=index+7
					if row[col]=="Total Expendicture(b)":
						worksheet.write(index+7, col,row[col],format2)
						b=row2=index+7

					if row[col]=="Surplus/(Deficit) from Operating Activities for the Period c=(a-b)":
						worksheet.write(index+7, col,row[col],format2)
						c=index+7

					if row[col]=="Revenue/(Expense) (d)":
						worksheet.write(index+7, col,row[col],format2)
						d=index+7
					if row[col]=="Ordinary Activities e=(c+d)":
						e=index+7

					if row[col]=="Minority Interest Share of Surplus/(Deficit)(f)":
						f=index+7

					if row[col]=="Net Surplus/(Deficit) for the Period g=(e-f)":
						worksheet.write(index+7, col,row[col],format2)
						g=index+7
					
				if col==1:
					worksheet.write(index+7, col,row[col],format1)
				if col==2:

					if row2==index+7:
						worksheet.write(index+7,col, "=SUM(C{}:C{})".format(row1+2,row2),money_format)
					elif c==index+7:
						worksheet.write(index+7,col, "=(C{}-C{})".format(a+1,b+1),money_format)
					elif e==index+7:
						worksheet.write(index+7,col, "=(C{}+C{})".format(c+1,d+1),money_format)	
					elif g==index+7:
						worksheet.write(index+7,col, "=(C{}-C{})".format(e+1,f+1),money_format)		

					else:
						worksheet.write(index+7, col,row[col],money_format)
					
					if row_==index+7:
						worksheet.write(index+6, col,'row[col]',bold)
						print(index+7, col)
					
		#existingws=workbook.get_worksheet_by_name("jcdjjkd")	
		import os
		os.system("start EXCEL.EXE excel.xlsx ")
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
		   <p style="font-weight: bold;font-size:18px;">FEDERAL COLLEGE OF AGRICULTURE, AKURE<p/>
      <p style="font-weight: bold;font-size:18px;">STATEMENT OF FINANCIAL PERFORMANCE AS AT {{date}}<p/>
      </div>
		<br>
		{{data}}
		</body>
		"""
		cursor.insertHtml(Template(table).render(data=printdata,date=self.date1))	
		document.print_(printer)		

			

class PerformanceContent(QWidget):
	
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
		
		r1=int(self.data.get('StatutoryRevenue', '0'))
		r2=int(self.data.get('GovernmentShareofVAT', '0'))
		r3=int(self.data.get('TaxRevenue', '0'))
		r4=int(self.data.get('NonTaxRevenues', '0'))
		r5=int(self.data.get('InvestmentIncome', '0'))
		r6=int(self.data.get('InterestEarned', '0'))
		r7=int(self.data.get('AidGrants', '0'))
		r8=int(self.data.get('140401 - 140402', '0'))
		r9=int(self.data.get('OtherRevenues', '0'))
		r10=int(self.data.get('TransferfromotherGovernmentEntities', '0'))
		

		r11=int(self.data.get('SalariesWages', '0'))
		r12=int(self.data.get('SocialBenefits', '0'))
		r13=int(self.data.get('OverheadCost', '0'))
		r14=int(self.data.get('GrantsContributions', '0'))
		r15=int(self.data.get('Subsidies', '0'))
		r16=int(self.data.get('DepreciationCharges', '0'))
		r17=int(self.data.get('ImpairmentCharges', '0'))
		r18=int(self.data.get('AmortizationCharges', '0'))
		r19=int(self.data.get('BadDebtsCharges', '0'))
		r20=int(self.data.get('PublicDebtCharges', '0'))
		r21=int(self.data.get('TransfertootherGovernmentEntities', '0'))
		r22=int(self.data.get('GainLossonDisposalofAsset', '0'))
		r23=int(self.data.get('GainLossonForeignExchangeTransaction', '0'))
		r24=(self.data.get('NA', '0'))
		f=r25=int(self.data.get('MinorityInterestShare', '0'))

		a=(r4+r5+r6+r7+r8+r9+r10)
		
		b=(r11+r12+r13+r14+r15+r16+r17+r18+r19+r20+r21)

		c=(a-b)

		revenue=r1+r2+r3
		expense=b
		d=revenue-expense

		e=(c+d)
		g=(e-f)

		
		
		
		
			
		style='border: 1px solid #dddddd; text-align: left;padding: 4px;'
		style1='border: 1px solid #dddddd; text-align: right;padding: 4px;'
		
		table= '''
				
                <table border=".3" cellSpacing="0" width="100%">
                
                <tbody>
                <tr>
		        <td style="{style}"></td><td style="{style}"><b>NCOA CODES</b></td><td style="{style}"><b>2019</b></td>
		        </tr>
		        
		        <tr>
		        <td style="{style}"><b>REVENUE</b></u></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        
		        <tr>
		        <td style="{style}">Government Share of FAAC (Statutory Revenue)</td><td style="{style}">110101 & 110103</td><td style="{style1}">{r1}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Government Share of VAT</td><td style="{style}">110102</td><td style="{style1}">{r2}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Tax Revenue</td><td style="{style}">120101</td><td style="{style1}">{r3}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Non-Tax Revenue</td><td style="{style}">120201 - 120210 &  120213</td><td style="{style1}">{r4}</td>
		        </tr>
		           		     
		        <tr>
		        <td style="{style}">Investment Income</td><td style="{style}">120211</td><td style="{style1}">{r5}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Interest earned</td><td style="{style}">120212</td><td style="{style1}">{r6}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Aid & Grants</td><td style="{style}">130101 - 130204</td><td style="{style1}">{r7}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Debt Forgiveness</td><td style="{style}">140401 - 140402</td><td style="{style1}">{r8}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Other Revenues</td><td style="{style}">140701</td><td style="{style1}">{r9}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Transfer from other Government Entities</td><td style="{style}">150101</td><td style="{style1}">{r10}</td>
		        </tr>
		        <tr>
		        <td style="{style}"><b>Total Revenue(a)</b></td><td style="{style}"></td><td style="{style1}"><b>{a}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        <tr>
		        <td style="{style}"><b>EXPENDITURE</b></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		       
		        <tr>
		        <td style="{style}">Salaries & Wages</td><td style="{style}">210101 - 210202</td><td style="{style1}">{r11}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Social Benefits</td><td style="{style}">210301</td><td style="{style1}">{r12}</td>
		        </tr>
		        		        
		        <tr>
		        <td style="{style}">Overhead Cost</td><td style="{style}">220201 - 220208, 220210 & 230501</td><td style="{style1}">{r13}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Grants & Contributions</td><td style="{style}">220401 - 220402</td><td style="{style1}">{r14}</td>
		        </tr>	       
		        
		        <tr>
		        <td style="{style}">Subsidies</td><td style="{style}">220501 & 220502</td><td style="{style1}">{r15}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Depreciation Charges</td><td style="{style}">240101 - 240201</td><td style="{style1}">{r16}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Impairment Charges</td><td style="{style}">260101 - 260301</td><td style="{style1}">{r17}</td>
		        </tr>
		        
		        <tr>
		        <td style="{style}">Amortization Charges</td><td style="{style}">250101</td><td style="{style1}">{r18}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Bad Debts Charges</td><td style="{style}">270101 & 270102</td><td style="{style1}">{r19}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Public Debt Charges</td><td style="{style}">220209</td><td style="{style}">{r20}</td>
		        </tr>
		        <tr>
		        <td style="{style}">Transfer to other Government Entities</td><td style="{style}">220701 - 220801</td><td style="{style1}">{r21}</td>
		        </tr>
		        
		        <tr>
		        <td style="{style}"><b>Total Expendicture(b)</b></td><td style="{style}"></td><td style="{style1}"><b>{b}</b></td>
		        </tr>

		        <tr>
		        <td style="{style}"><b>Surplus/(Deficit) from Operating Activities for the Period c=(a-b)</b></td><td style="{style}"></td><td style="{style1}"><b>{c}</b></td>
		        </tr>

		        <tr>
		        <td style="{style}">Gain/ Loss on Disposal of Asset</td><td style="{style}">140501 - 140503 & 140801 - 140901/(280101 - 280105)</td><td style="{style1}">{r22}</td>
		        </tr>

		        <tr>
		        <td style="{style}">Gain/Loss on Foreign Exchange Transaction</td><td style="{style}">141001/(220901)</td><td style="{style1}">{r23}</td>
		        </tr>		    
		        <tr>
		        <td style="{style}">Share of Surplus/(Deficit) in Associates & Joint Ventures</td><td style="{style}">NA</td><td style="{style1}">{r24}</td>
		        </tr>

		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>
		        
		         <tr>
		        <td style="{style}"><b>Revenue/(Expense) (d)</b></td><td style="{style}"></td><td style="{style1}"><b>{d}</b></td>
		        </tr>

		        <tr>
		        <td style="{style}"><b>Ordinary Activities e=(c+d)</b></td><td style="{style}"></td><td style="{style1}"><b>{e}</b></td>
		        </tr>
		        <tr>
		        <td style="{style}"></td><td style="{style}"></td><td style="{style}"></td>
		        </tr>

		        <tr>
		        <td style="{style}">Minority Interest Share of Surplus/(Deficit)(f)</td><td style="{style}">140601</td><td style="{style1}">{r25}</td>
		        </tr>

		        <tr>
		        <td style="{style}"><b>Net Surplus/(Deficit) for the Period g=(e-f)</b></td><td style="{style}"></td><td style="{style1}"><b>{g}</b></td>
		        </tr>
		         
		          <tbody>
		        </table><br><br>'''.format(style=style,style1=style1,\
		        	r1=self.Currency(r1),r2=self.Currency(r2),r3=self.Currency(r3),r4=self.Currency(r4),r5=self.Currency(r5)\
		        	,r6=self.Currency(r6),r7=self.Currency(r7), r8=self.Currency(r8),r9=self.Currency(r9),r10=self.Currency(r10),\
		        	a=self.Currency(a),r11=self.Currency(r11),r12=self.Currency(r12), r13=self.Currency(r13),r14=self.Currency(r14),r15=self.Currency(r15),\
		        	r16=self.Currency(r16),r17=self.Currency(r17),r18=self.Currency(r18),r19=self.Currency(r19),\
		        	r20=self.Currency(r20),r21=self.Currency(r21),b=self.Currency(b),c=self.Currency(c),r22=self.Currency(r22),r23=self.Currency(r23),r24=(r24),\
		        	d=self.Currency(d),e=self.Currency(e),r25=self.Currency(r25),g=self.Currency(g))

		        
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
                  <p>STATEMENT OF FINANCIAL PERFORMANCE AS AT {date1}<p/>
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
	ex = FinPerformance()
	ex.show()
	sys.exit(app.exec_())




