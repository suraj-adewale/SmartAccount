from PyQt5.QtWidgets import QMainWindow, QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json
from babel.numbers import format_currency

class AddAccount(QWidget):
	def __init__(self,widg,editdata):
		QWidget.__init__(self)
		self.title = 'Add Account'
		self.left = (self.x()+400)
		self.top = (self.x()+150)
		self.width = 500
		self.height = 400
		self.editList=editdata
		self.widg=widg
		self.option=""
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		#import uuid,re
		#print(uuid.getnode())
		#print (':'.join(re.findall('..', '%012x' % uuid.getnode())))#Use this to get Mac address of Computer 

		usertype_db=open("db/usertype.json", "r")
		usertype=json.load(usertype_db)
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			ipaddress=open("db/ipaddress.json", "r")
			self.ip=json.load(ipaddress)
		try:
			if self.editList[5]=='Delete':
				self.option="Delete"
				self.AddAccount('addaccount',self.editList)
		except Exception as e:
			pass
			
		requireddata=open("db/selectreportcode.json", "r")
		self.requireddata=json.load(requireddata)
				
		self.mainlayout=QGridLayout()
		self.setLayout(self.mainlayout)	
		
		self.amt_placeholder=format_currency(0,'NGN', locale='en_US')
		self.MessageBox=QMessageBox()
		self.mainbox = QGroupBox('Create New Account')
		self.mainlayout.addWidget(self.mainbox,0,0)

		mainboxlayout=QVBoxLayout()
		self.mainbox.setLayout(mainboxlayout)

		accountLayout=QFormLayout()
		self.acctname=QLineEdit()
		self.acctname.setMaximumWidth(200)
		accountLayout.addRow(QLabel('Account Name:'),self.acctname)
		
		mainboxlayout.addLayout(accountLayout)

				
		self.radiobox = QGroupBox('Type')
		mainboxlayout.addWidget(self.radiobox)

		radioLayout=QFormLayout()
		radioLayout.setHorizontalSpacing(200)
		self.radiobox.setLayout(radioLayout)
		
		self.Asset=QRadioButton("Asset")
		self.Liability=QRadioButton("Liability")
		self.Equity=QRadioButton("Equity")
		self.Income=QRadioButton("Revenue")
		self.Expense=QRadioButton("Expense")

		self.assetType = QComboBox()
		self.assetType.setMaximumWidth(250)
		self.liabilityType = QComboBox()
		self.liabilityType.setMaximumWidth(250)
		self.equityType = QComboBox()
		self.equityType.setMaximumWidth(250)
		self.incomeType = QComboBox()
		self.incomeType.setMaximumWidth(250)
		self.expenseType = QComboBox()
		self.expenseType.setMaximumWidth(250)

		radioLayout.addRow(self.Asset,self.assetType)
		radioLayout.addRow(self.Liability,self.liabilityType)
		radioLayout.addRow(self.Equity,self.equityType)
		radioLayout.addRow(self.Income,self.incomeType)
		radioLayout.addRow(self.Expense,self.expenseType)


		classificationLayout=QFormLayout()
		classificationLayout.setHorizontalSpacing(140)
		mainboxlayout.addLayout(classificationLayout)
		
		self.cashflow=QComboBox()
		cashflowList=["OAFRCUST","OAPDSUPP","OAPAYROL","OAINPAID","OATXPAID","IAASSETS","IAFRDIV","FAPDDIV","FAPDLOAN"]
		self.cashflow.addItem("       - - Cash Flow Classification - -")
		self.cashflow.addItems(cashflowList)
		self.cashflow.setMaximumWidth(250)
		self.accountnumber=QLineEdit()
		self.accountnumber.setMaximumWidth(250)
		self.reportgroup=QComboBox()
		reportgroupList=self.requireddata
		self.reportgroup.addItem("     - - Report Group Code - -")
		self.reportgroup.addItems(reportgroupList)
		self.reportgroup.setMaximumWidth(250)
		self.balance=QLineEdit()
		self.balance.setPlaceholderText(self.amt_placeholder)
		self.balance.setMaximumWidth(250)
		
		classificationLayout.addRow(QLabel("Classification for Cash Flow:"),self.cashflow)
		classificationLayout.addRow(QLabel("Account Number:"),self.accountnumber)
		classificationLayout.addRow(QLabel("Default Linked for Account:"),self.reportgroup)
		classificationLayout.addRow(QLabel("Opening Balance:"),self.balance)

		responselayout=QGridLayout()
		self.mainlayout.addWidget(QLabel(),1,0)
		self.mainlayout.addLayout(responselayout,2,0)

		self.add=QPushButton('Add')
		self.add.setMaximumWidth(60)
		self.done=QPushButton('Done')
		self.done.setMaximumWidth(60)
		self.help=QPushButton('Help')
		self.help.setMaximumWidth(60)

		responselayout.addWidget(QLabel(),0,0,0,2)
		
		responselayout.addWidget(self.add,0,4)
		responselayout.addWidget(self.done,0,5)
		responselayout.addWidget(self.help,0,6)

		self.add.clicked.connect(self.Add)
		self.done.clicked.connect(self.Done)

		try:
			if self.editList[5]=="Edit":
				self.option=self.editList[0]
				self.acctname.setText(self.editList[1])
				if self.editList[3]=='Revenue':
					self.Income.setChecked(True)
				if self.editList[3]=='Expense':
					self.Expense.setChecked(True)	
				if self.editList[3]=='Asset':
					self.Asset.setChecked(True)
				if self.editList[3]=='Liability':
					self.Liability.setChecked(True)
				if self.editList[3]=='Equity':
					self.Equity.setChecked(True)	
				self.accountnumber.setText(self.editList[0])
				self.reportgroup.setCurrentText(self.editList[4])
				for reportcode in reportgroupList:
					if reportcode.split(' - ')[0]==self.editList[4]:
						self.reportgroup.setCurrentText(reportcode)
						break
		except Exception as e:
			pass

	def AlertMessage(self,title,info,type):
		self.MessageBox.setWindowTitle(title)
		self.MessageBox.setText("")
		self.MessageBox.setInformativeText("\n{}\n".format(info))
		self.MessageBox.setIcon(self.MessageBox.Critical)
		self.MessageBox.setStandardButtons(self.MessageBox.Close)
		self.MessageBox.show()	

	def AccountVerification(self,initial,Type):
		if self.accountnumber.text() is not '':
			initia_l=str(self.accountnumber.text())[0]

			if initia_l is not initial:
				self.AlertMessage("Add Account","{} Account Number must start with {}	".format(Type,initial),"Critical".format(Type,initial))
				return False
	def Done(self):
		try:
			self.widg.edit.setDisabled(True)
			self.widg.delete.setDisabled(True)
			self.close()
		except Exception as e:
			self.close()
	def closeEvent(self, event):
		try:
			self.widg.edit.setDisabled(True)
			self.widg.delete.setDisabled(True)
			self.close()
		except Exception as e:
			self.close()
					
	
	def Add(self):
		Type=''
		acctname=self.acctname.text()
		cashflow=self.cashflow.currentText()
		accountnumber=self.accountnumber.text()	
		reportgroup=self.reportgroup.currentText() 
		balance=self.balance.text()
		if "&" in acctname:
			QMessageBox.critical(self, 'String Error', "\nSymbol \"&\" is not allowed use \"and\" instead\n")
			return False			
		if self.Asset.isChecked()==True:
			Type=self.Asset.text()
			self.AccountVerification('3','Asset')
		if self.Liability.isChecked()==True:
			Type=self.Liability.text()
			self.AccountVerification('4','Liability')
		if self.Equity.isChecked()==True:
			Type=self.Equity.text()
			self.AccountVerification('4','Equity')		
		if self.Expense.isChecked()==True:
			Type=self.Expense.text()
			self.AccountVerification('2','Expense')
		if self.Income.isChecked()==True:
			Type=self.Income.text()
			self.AccountVerification('1','Income')

		if accountnumber=='' or acctname=='' or Type=='' or reportgroup=="     - - Report Group Code - -" or cashflow=="       - - Cash Flow Classification- -":
			QMessageBox.critical(self, 'Empty input  ', "\n    Fields cannot be empty    \n") 
			return False
		
		reportgroup=reportgroup.split(' - ')[0]
	
		self.postList=[]
		self.postList.append(accountnumber)
		self.postList.append(acctname)
		self.postList.append(Type)
		self.postList.append(reportgroup)
		self.postList.append(cashflow)
		self.postList.append(balance)
		self.AddAccount('addaccount',self.postList)

	def AddAccount(self,action,postList):		
		postList=json.dumps(postList)
		data = QtCore.QByteArray()
		data.append("action={}&".format(action))
		data.append("account={}&".format(postList))
		data.append("option={}".format(self.option))
		url = "http://{}:5000/addaccount".format(self.ip)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse)
		self.nam.post(req, data)

	def handleResponse(self, reply):
	    er = reply.error()
	    if er == QtNetwork.QNetworkReply.NoError:
	        bytes_string = reply.readAll()
	        json_ar = json.loads(str(bytes_string, 'utf-8'))
	       
	        if json_ar['2']=='accountexists':
	        	QMessageBox.critical(self, 'Databese Connection  ', "\nThis account already exists please try again with different one	 \n")
	        	return False   	

	        if json_ar['2']=='accountcreated':	
	        	QMessageBox.critical(self, 'Databese Connection  ', "\nAccount created successfully	 \n")
	        	return False
	        if json_ar['2']=='accountedited':	
	        	QMessageBox.critical(self, 'Databese Connection  ', "\nAccount edited successfully	 \n")
	        	return False

	        if json_ar['2']=='accountdeleted':	
	        	QMessageBox.critical(self, 'Databese Connection  ', "\nAccount deleted successfully	 \n")
	        	return False		
	        
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "\n{} 	 \n".format(reply.errorString()))			

		


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AddAccount()
	ex.show()
	sys.exit(app.exec_())
