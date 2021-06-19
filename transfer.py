from PyQt5.QtWidgets import QApplication,QWidget,QDialogButtonBox,QDateEdit,QComboBox,QMessageBox,QDialog,QGroupBox,QFormLayout, QPushButton,QLabel, QVBoxLayout, QGridLayout,QLineEdit
from PyQt5.QtCore import Qt, QDate,QDateTime
from PyQt5 import QtCore, QtNetwork,QtWidgets
from babel.numbers import format_currency,parse_number,format_number,parse_decimal,format_decimal
import sys,json,base64
from functools import partial

class TransferAccount(QDialog):
	def __init__(self,parent=None):
		QWidget.__init__(self)
		self.setWindowTitle("Account Transfer")

		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))
		
		self.display_text=''

		layout = QGridLayout()
		self.setLayout(layout)
		self.MessageBox=QMessageBox()
		self.amt_placeholder=format_currency(0,'NGN', locale='en_US')
		labelaccount1 = QLabel("Transfer from account:")
		labelaccount2 = QLabel("Transfer to account:")
		self.bal1 = QLabel("	")
		self.bal2 = QLabel("	")
		amountlabel=QLabel("Amount to transfer:")
		date=QLabel("Date:")
		
		self.account1=QComboBox()
		self.account2=QComboBox()

		self.account1.currentTextChanged.connect(self.BalAccount1)
		self.account2.currentTextChanged.connect(self.BalAccount2)

		self.account1.addItems(['','31020101 - GIFMIS  (Capital)','31020102 - GIFMIS Personnel','31020103 - GIFMIS Overhead','31020104 - TSA Revenue','31020106 - TSA Aids & Grants','31020108 - TSA Other Funds'])
		self.account2.addItems(['','31020101 - GIFMIS  (Capital)','31020102 - GIFMIS Personnel','31020103 - GIFMIS Overhead','31020104 - TSA Revenue','31020106 - TSA Aids & Grants','31020108 - TSA Other Funds'])
		labelbal1 = QLabel("Balance:")
		labelbal2 = QLabel("Balance:")
		
		self.amount=QLineEdit()
		self.amount.setPlaceholderText(self.amt_placeholder)
		self.amount.textChanged.connect(self.TextChange)

		self.date()
		
		layout.addWidget(labelaccount1, 0, 0)
		layout.addWidget(self.account1, 0, 1)
		layout.addWidget(labelbal1, 0, 2)
		layout.addWidget(self.bal1, 0, 3)
		layout.addWidget(labelaccount2, 1, 0)
		layout.addWidget(self.account2, 1, 1)
		layout.addWidget(labelbal2, 1, 2)
		layout.addWidget(self.bal2, 1, 3)
		layout.addWidget(amountlabel, 2, 0)
		layout.addWidget(self.amount, 2, 1)
		layout.addWidget(date, 3, 0)
		layout.addWidget(self.dateedit1, 3, 1)
		
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		layout.addWidget(buttonbox,5,1,1,3)

		buttonbox.accepted.connect(self.Transfer)
		buttonbox.rejected.connect(self.Cancel)

	def date(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit1 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)

	def BalAccount1(self,Obj):
		if Obj=='':
			return False
		self.accnt1=(Obj.split(' - '))[0]	
		self.desc1=(Obj.split(' - '))[1]
		self.Bal(self.desc1,1)
		
	def BalAccount2(self,Obj):
		if Obj=='':
			return False
		self.accnt2=(Obj.split(' - '))[0]
		self.desc2=(Obj.split(' - '))[1]	
		self.Bal(self.desc2,2)	
				
	def Cancel(self):
		self.close()	

	def TextChange(self):
		try:
			amountpayable = (self.amount.text())
			if amountpayable.count('.')==2:
				(self.amount).setText(str(self.display_text))
				return False
			if amountpayable=='' or amountpayable=='.':
				return False

			if amountpayable[-1]!='.':
				amountpayable=(parse_decimal(amountpayable,locale='en_US'))
				amountpayable=(format_decimal(amountpayable,locale='en_US'))
			self.display_text=amountpayable
		
		except Exception as e:
			#print(amountpayable.isalpha())
			if (amountpayable.isalpha())==True:
				(self.amount).setText('')
			else:
				(self.amount).setText(str(self.display_text))	
			return False
		(self.amount).setText(str(self.display_text))


	def Transfer(self):
		dicData={}
		List1=[]
		List2=[]

		
		if self.amount.text()=="" :
			return False
		self.amt=float(parse_decimal(self.amount.text(),locale='en_US'))	
		
		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)

		ref="GJ[AUTO]"
		userdb=open("db/user.json", "r")
		user=json.load(userdb)

		account1=self.account1.currentText()
		account2=self.account2.currentText()
				
		List1.append(account1)
		List1.append(self.amt)
		List1.append('Credit')
		List1.append(ref)
		List1.append('General')
		List1.append('Transfer')
		List1.append(date)
		List1.append(user)

		List2.append(account2)
		List2.append(self.amt)
		List2.append('Debit')
		List2.append(ref)
		List2.append('General')
		List2.append('Transfer')
		List2.append(date)
		List2.append(user)

		dicData[0]=List1
		dicData[1]=List2

		postDic=json.dumps(dicData)
		postDic=base64.b64encode(postDic.encode())
		data = QtCore.QByteArray()
		data.append("action=postjournal&")
		data.append("journal={}".format(postDic.decode("utf-8")))
		url = "http://localhost:5000/journal"
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse1)
		
		#return False
		self.nam.post(req, data)

	def handleResponse1(self, reply):

	    er = reply.error()

	    if er == QtNetwork.QNetworkReply.NoError:

	        bytes_string = reply.readAll()
	        
	        json_ar = json.loads(str(bytes_string, 'utf-8'))
	        #data = json_ar['form']
	        if json_ar['19']=='Success':
	        	journaltype=json_ar['30']
	        	ref=json_ar['25']
	        	date=json_ar['35']
	        	self.MessageBox.setWindowTitle('Transfer Account')
	        	self.MessageBox.setText("")
	        	self.MessageBox.setInformativeText("{amt} was succesfully moved from {acct1} to {acct2} \n with {ref} on {d}. " "\n\nClick Ok to exit.".format(\
	        		amt=format_currency(self.amt,'NGN', locale='en_US'),acct1=self.desc1,acct2=self.desc2,ref=ref,d=date))
	        	self.MessageBox.setIcon(self.MessageBox.Information)
	        	self.MessageBox.setStandardButtons(self.MessageBox.Ok)
	        	self.MessageBox.show()
	        	self.amount.clear()
	        	
	        result = self.MessageBox.exec_()
	        if result==self.MessageBox.Ok:
	        	pass
	        
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', " 	\n {}	 \n 	".format(reply.errorString()))		

	def Bal(self,desc,which):
		data = QtCore.QByteArray()
		data.append("action=balance&")
		data.append("description={}".format(desc))
		url = "http://{}:5000/balance".format(self.ip)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(partial(self.handleResponse,which))
		self.nam.post(req, data)

	def handleResponse(self, which,reply):
	    er = reply.error()
	    if er == QtNetwork.QNetworkReply.NoError:
	        bytes_string = reply.readAll()
	        json_ar = json.loads(str(bytes_string, 'utf-8'))
	        if which==1:
	        	self.bal1.setText(format_currency(float(json_ar['bal']),'NGN', locale='en_US'))
	        if which==2:
	        	self.bal2.setText(format_currency(float(json_ar['bal']),'NGN', locale='en_US'))	
	        return False

	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "\n{} 	\n 	".format(reply.errorString()))	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen =TransferAccount()
	screen.exec_()
	sys.exit(app.exec_())
