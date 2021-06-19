from PyQt5.QtWidgets import QPushButton,QListWidget,QDialogButtonBox,QDialog,QAbstractItemView,QTableWidget,QTextEdit,QLabel,QCompleter,QTableWidgetItem,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPainter
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys, json, base64
from babel.numbers import format_currency,parse_number,format_number,parse_decimal,format_decimal

class ImageWidget(QWidget):

    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
    	painter = QPainter(self)
    	painter.drawPixmap(0, 0, self.picture)

class AddJournal(QDialog):
	def __init__(self,journalwidget,edit_data,d1,d2, parent=None):
		super(AddJournal, self).__init__(parent)
		self.title = 'Add Journal'
		self.left = (self.x()+400)
		self.top = (self.x()+150)
		self.width = 550
		self.height = 500
		self.journalwidget=journalwidget
		self.edit_data=edit_data
		self.d1=d1
		self.d2=d2
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)

		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))

		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
		self.addJournalContent()
		self.setLayout(self.mainlayout)
		#self.setCentralWidget(self.widget)
		#self.exec_()	

	def addJournalContent(self):
		
		self.widget=QWidget()
		
		self.widgetDic={}
				
		self.balance=self.comborow=0
		self.row=10
		self.display_text=''

		self.rowCounts=self.row

		self.MessageBox=QMessageBox()
		
		requireddata=open("db/accounts.json", "r")
		self.requireddata=json.load(requireddata)

		self.amt_placeholder=format_currency(0,'NGN', locale='en_US')

		self.journaltypelist=["","General","Payments","Sales","Receipts","Purchases"]
		self.journalAuto=["","GJ[AUTO]","PMT[AUTO]","SLS[AUTO]","REC[AUTO]","PRC[AUTO]"]

		self.mainlayout=QVBoxLayout()
		labellayout=QVBoxLayout()
		gridLayout=QGridLayout()
		gridLayout.setHorizontalSpacing(300)
		tablelayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)

		self.mainlayout.addLayout(labellayout,1)
		self.mainlayout.addLayout(gridLayout,2)
		self.mainlayout.addLayout(tablelayout,5)

		labellayout.addWidget(QLabel("Journal Entry\nFor a manual journal entry enter the details of the transactions and then allocate the amount to\naccounts."))
		
		#distro_install_command = {'Debian': 'apt-get'}
		#del distro_install_command['Debian']
		#print(distro_install_command)

		datelabel=QLabel("Date:")
		journallabel=QLabel("Journal:")
		reflabel=QLabel("Reference:")
		journalmemolabel=QLabel("Journal memo:")

		currentTabdb=open("db/journaltabs.json", "r")
		self.currenttab=json.load(currentTabdb)

		self.date()
		self.comboboxjournaltype = QComboBox()
		self.comboboxjournaltype.setObjectName('comboboxjournaltype')
		self.comboboxjournaltype.addItems(self.journaltypelist)
		
		self.reflineedit=QLineEdit()
		self.reflineedit.setToolTip("If needed, change this number to another unique value.")
		
		self.memo=QTextEdit()
		self.memo.setToolTip("Enter the transactions discription.")

		self.memo.setMaximumHeight(50)
		
		self.comboboxjournaltype.currentTextChanged.connect(self.comboboxjournaltype_changed)

		gridLayout.addWidget(datelabel,0,0)
		gridLayout.addWidget(self.dateedit1,0,1)
		gridLayout.addWidget(journallabel,1,0)
		gridLayout.addWidget(self.comboboxjournaltype,1,1)
		gridLayout.addWidget(reflabel,2,0)
		gridLayout.addWidget(self.reflineedit,2,1)
		gridLayout.addWidget(journalmemolabel,3,0)
		gridLayout.addWidget(self.memo,3,1)

		self.addJournalTable()
		tablelayout.addWidget(QLabel("Accounts Allocation"))
		tablelayout.addLayout(self.tablelayout)

		dclayout=QGridLayout()
		#dclayout.setHorizontalSpacing(0)
		tablelayout.addLayout(dclayout)
		
		self.totalcredit=QLabel()
		self.totaldebit=QLabel()
		
		dclayout.addWidget(QLabel(''),0,0,0,7)
		dclayout.addWidget(QLabel('<b>Debit:</b>'),0,7)
		dclayout.addWidget(self.totaldebit,0,8)
		dclayout.addWidget(QLabel('<b>Credit:</b>'),1,7)
		dclayout.addWidget(self.totalcredit,1,8)

		self.balencelabel=QLineEdit()
		tablelayout.addWidget(self.balencelabel,1)
		#tablelayout.addSeparator()
		buttongridLayout=QGridLayout()
		tablelayout.addLayout(buttongridLayout)
		self.templatebutton=QPushButton()
		recordbutton=QPushButton("Record")
		cancelbutton=QPushButton("Cancel")
		helpbutton=QPushButton("Help")

		try:
			self.template=json.load(open("db/adjournal_template.json","r"))
			self.templatebutton.setText("Use Template {}".format(len(self.template)))
		except Exception as e:
			json.dump({},open("db/adjournal_template.json", "w"))
			self.template={}

		if len(self.template)==0:
			self.templatebutton.setDisabled(True)
			self.templatebutton.setText("Use Template {}".format(len(self.template)))

		self.templatebutton.clicked.connect(self.Template)
		recordbutton.clicked.connect(self.PostData)
		cancelbutton.clicked.connect(self.Cancel_button)

		buttongridLayout.addWidget(self.templatebutton,0,0,0,2)
		buttongridLayout.addWidget(QLabel(),0,2)
		buttongridLayout.addWidget(QLabel(),0,3)
		buttongridLayout.addWidget(recordbutton,0,4)
		buttongridLayout.addWidget(cancelbutton,0,5)
		buttongridLayout.addWidget(helpbutton,0,6)
		self.journalType()
		self.AddData()
	
	def AddData(self):
		if self.edit_data !={}:
			edit_data=self.edit_data["0"]

			date=edit_data[6]
			self.ref=edit_data[3]
			self.journaltype=edit_data[4]
			memo=edit_data[5]

			year=(date.split('-'))[0]
			month=(date.split('-'))[1]
			day=(date.split('-'))[2]

			self.dateedit1.setDate(QDate(int(year),int(month),int(day)))
			self.comboboxjournaltype.setCurrentText(self.journaltype)
			self.memo.setText(memo)
			self.reflineedit.setText(self.ref)

			self.comborow=len(self.edit_data)
			self.UpdateRows(self.edit_data)
			self.text_changed_function()
			
			if self.comborow>10:
				self.rowCounts=(self.comborow+5)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()

	def date(self):
		date = QDate()
		currentdate=date.currentDate()
		self.dateedit1 = QDateEdit()
		self.setObjectName("dateedit")
		self.dateedit1.setDate(currentdate)
		self.dateedit1.setDisplayFormat('dd/MM/yyyy')
		self.dateedit1.setCalendarPopup(True)

	def journalType(self):
		#self.currenttab=self.currenttab+1
		self.comboboxjournaltype.setCurrentText(self.journaltypelist[self.currenttab])
		index=self.comboboxjournaltype.currentIndex()
		self.memo.setText(self.journaltypelist[index])
		self.autoref=self.journalAuto[index]
		self.reflineedit.setText(self.autoref)
		

	def addJournalTable(self):
		JournalHeader=["Account ","			Amount   		","    DR/CR     ",""]
		self.tablelayout=QVBoxLayout()
		self.table =QTableWidget()
		self.table.setColumnCount(4)     #Set three columns
		self.table.setRowCount(self.row)
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		#self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = self.table.horizontalHeader()       
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1,1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

		self.tablelayout.addWidget(self.table)
				
		self.table.clicked.connect(self.AddJournals)
		
		self.table.resizeRowsToContents()
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(JournalHeader)
		
		self.table.horizontalHeaderItem(0).setToolTip("Click on any row to add an account")
		self.table.horizontalHeaderItem(1).setToolTip("Type amount here")
		self.table.horizontalHeaderItem(2).setToolTip("Choose either Debit or Credit")
		self.table.horizontalHeaderItem(3).setToolTip("Click to delete a row")
			
	def comboboxjournaltype_changed(self,index):

		self.autoref=self.journalAuto[self.journaltypelist.index(index)]
		self.reflineedit.setText(self.autoref)
		self.memo.setText(self.journaltypelist[self.journaltypelist.index(index)])
	
	def AddJournals(self,item):
		self.templatebutton.setEnabled(True)
		self.templatebutton.setText("Save As Template...")
		currRow=(item.row())
				
		if item.column()==0:
			
			self.AddTableCell()
									
			Dr_=Cr_=0
			for key in self.widgetDic:
				
				if (self.widgetDic[key][2]).currentText()=='Debit' and (self.widgetDic[key][1]).text() is not '':
					
					Dr_=Dr_+float(parse_decimal((self.widgetDic[key][1]).text(), locale='en_US'))
					 	
				if (self.widgetDic[key][2]).currentText()=='Credit' and (self.widgetDic[key][1]).text() is not '':
					
					Cr_=Cr_+float(parse_decimal((self.widgetDic[key][1]).text(), locale='en_US'))
										
			self.balance=abs(Dr_- Cr_)
	
			if Dr_ > Cr_:
				(self.widgetDic[self.comborow-1][2]).setCurrentText('Credit')
				(self.widgetDic[self.comborow-1][1]).setText(format_number(self.balance, locale='en_US'))
			
			if  Cr_ > Dr_ :
				(self.widgetDic[self.comborow-1][2]).setCurrentText('Debit')
				(self.widgetDic[self.comborow-1][1]).setText(format_number(self.balance, locale='en_US'))	
					
			if self.balance is not abs(Dr_- Cr_):
				bal=format_currency(self.balance,'NGN', locale='en_US')
				self.balencelabel.setText('   Amount not yet applied to an account (out of balance):  {}'.format(bal))
			
			
			self.text_changed_function()
		
		if item.column()==3:
			self.DeleteRow(currRow)
			
	def AddTableCell(self):
		AccountsList=self.requireddata
		AccountsList.sort()
		comboboxAccount=QComboBox()
		comboboxAccount.setEditable(True)
		amount=QLineEdit()
		amount.setPlaceholderText(self.amt_placeholder)

		completer = QCompleter(AccountsList)
		comboboxAccount.setCompleter(completer)
		debit_credit = QComboBox()
		comboboxAccount.setObjectName('comboboxAccount')

		comboboxAccount.addItem('')	
		comboboxAccount.addItems(AccountsList)
		debit_credit.addItems(["Debit","Credit"])

		image = ImageWidget('image/icon/clear.png', self)
        

		if self.comborow not in self.widgetDic:
			widgetList=[]
			widgetList.append(comboboxAccount)
			widgetList.append(amount)
			widgetList.append(debit_credit)
			self.widgetDic[self.comborow]=widgetList
			(self.widgetDic[self.comborow][1]).textChanged.connect(self.text_changed_function)
			(self.widgetDic[self.comborow][2]).currentTextChanged.connect(self.text_changed_function)
		
			self.table.setCellWidget(self.comborow,0,comboboxAccount)
			self.table.setCellWidget(self.comborow,1,amount)
			self.table.setCellWidget(self.comborow,2, debit_credit)
			#self.table.setItem(self.comborow, 3, QTableWidgetItem('    X'))
			self.table.setCellWidget(self.comborow, 3, image)

			self.comborow=self.comborow+1
						
		
		if self.comborow==self.rowCounts:
			self.rowCounts+5
			self.rowCounts=(self.rowCounts+5)
			self.table.setRowCount(self.rowCounts)
			self.table.resizeRowsToContents()

	def DeleteRow(self,row):

		if row in self.widgetDic.keys():

			self.widgetDic.pop(row)
			journaldata={}
			index=0
			for key in sorted(self.widgetDic):
				data_list=[]
				for col in range(3):
					if col==0:	
						data_list.append((self.widgetDic[key][0]).currentText())
					if col==1:	
						data_list.append((self.widgetDic[key][1]).text())
					if col==2:	
						data_list.append((self.widgetDic[key][2]).currentText())		
				journaldata[index]=data_list
				index=index+1
				
			self.UpdateRows(journaldata)
			
			self.comborow=self.comborow-1
			if self.rowCounts>10:
				self.rowCounts=(self.rowCounts-1)
				self.table.setRowCount(self.rowCounts)
				self.table.resizeRowsToContents()

			self.text_changed_function()

		self.template=json.load(open("db/adjournal_template.json","r"))	
		if len(self.template)==0 and len(self.widgetDic)==0:
			self.templatebutton.setText("Use Template {}".format(len(self.template)))
			self.templatebutton.setDisabled(True)
		elif len(self.template)>0 and len(self.widgetDic)==0:
			self.templatebutton.setText("Use Template {}".format(len(self.template)))
			self.templatebutton.setEnabled(True)		
		
		
	def UpdateRows(self,journaldata):
		self.table.clearContents()	
		self.widgetDic={}
		#print(self.rowCounts)
		if len(journaldata)<=10:
			self.table.setRowCount(10)
			self.table.resizeRowsToContents()
		else:
			self.table.setRowCount(len(journaldata))
			self.table.resizeRowsToContents()	
        
		for keys in sorted(journaldata):
			try:
				widgetList=[]
				account=QComboBox()#self.widgetDic[keys][0]
				amount=QLineEdit()#self.widgetDic[keys][1]
				dc=QComboBox()#self.widgetDic[keys][2]					
				account.setEditable(True)
				AccountsList=self.requireddata
				AccountsList.sort()
				account.addItem('')
				account.addItems(AccountsList)
				dc.addItems(["Debit","Credit"])

				completer = QCompleter(AccountsList)
				account.setCompleter(completer)

				amount.setPlaceholderText(self.amt_placeholder)

				amount.textChanged.connect(self.text_changed_function)
				dc.currentTextChanged.connect(self.text_changed_function)
	
				account.setCurrentText(journaldata[keys][0])
				amount.setText(str(journaldata[keys][1]))
				dc.setCurrentText(journaldata[keys][2])
				
				self.table.setCellWidget(int(keys),0,account)
				self.table.setCellWidget(int(keys),1,amount)
				self.table.setCellWidget(int(keys),2, dc)
				image = ImageWidget('image/icon/clear.png', self)
				self.table.setCellWidget(int(keys), 3, image)

				widgetList.append(account)
				widgetList.append(amount)
				widgetList.append(dc)
				
				self.widgetDic[int(keys)]=widgetList
				
			except Exception as e:
				raise(e)
	
		
	def text_changed_function(self):
		Debit_bal=Credit_bal=0
		for row in self.widgetDic:	
			if ((self.widgetDic[row][1]).text())=='':
				return False
			try:
				amt=((self.widgetDic[row][1]).text())
				format_amt='{:,}'.format(int(amt.replace(',','')))
			except Exception as e:
				#print(e)
				amt=((self.widgetDic[row][1]).text())
				format_amt=amt	
	
			(self.widgetDic[row][1]).setText(str(format_amt))	
			try:
				if (self.widgetDic[row][2]).currentText()=='Debit':
			 		Debit_bal=Debit_bal+(parse_decimal(amt, locale='en_US'))
				if (self.widgetDic[row][2]).currentText()=='Credit':
			 		Credit_bal=Credit_bal+(parse_decimal(amt, locale='en_US'))
			except Exception as e:
				List=list(amt)
				del List[-1]
				(self.widgetDic[row][1]).setText(str(','.join(List)).replace(',',''))
						
			
		if abs(Debit_bal-Credit_bal) > 0.0:
			bal=format_currency(abs(Debit_bal-Credit_bal),'NGN', locale='en_US')
			self.balencelabel.setText('Amount not yet applied to an account (out of balance): {}'.format(bal))
		else:
			self.balencelabel.setText('  ')

		self.totaldebit.setText('<b>'+format_currency((Debit_bal),'NGN', locale='en_US')+'</b>')
		self.totalcredit.setText('<b>'+format_currency((Credit_bal),'NGN', locale='en_US')+'</b>')
		
	def comboboxAccount_changed(self,row):
		pass	
	
	def Template(self):
		text=self.templatebutton.text()
		if text=="Save As Template...":
			self.NewTemplate()
		if text=="Use Template {}".format(len(self.template)):
			self.ViewTemplate()	
	
	def ViewTemplate(self):
		self.dialog=QDialog(self)
		layout = QGridLayout()
		self.dialog.setWindowTitle("Templates")
		self.dialog.setLayout(layout)
		self.listwidget = QListWidget()
		layout.addWidget(self.listwidget)
		row=0
		for keyname in self.template:
			self.listwidget.insertItem(row, keyname)
			row=row+1
		self.listwidget.clicked.connect(self.TemplateList)

		self.delbtn=QPushButton("Delete Template")
		self.delbtn.clicked.connect(self.DeleteTemplate)
		layout.addWidget(self.delbtn)
		self.delbtn.setDisabled(True)
		self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		self.buttonbox.accepted.connect(self.Load)
		self.buttonbox.rejected.connect(self.dialog.close)
		self.buttonbox.setDisabled(True)
		layout.addWidget(self.buttonbox)
		self.dialog.exec_()

	

	def DeleteTemplate(self):
		
		item = (self.listwidget.currentItem()).text()
		self.template.pop(item)
		self.listwidget.clear()
		row=0
		for keyname in self.template:
			self.listwidget.insertItem(row, keyname)
			row=row+1
		self.listwidget.clicked.connect(self.TemplateList)
		
		json.dump(self.template,open("db/adjournal_template.json", "w"))
		self.templatebutton.setText("Use Template {}".format(len(self.template)))
		if len(self.template)==0:
			self.templatebutton.setDisabled(True)
			self.delbtn.setDisabled(True)
			self.buttonbox.setDisabled(True)
		
	def Load(self):
		item = (self.listwidget.currentItem()).text()
		data=self.template[item]
		self.edit_data = (data)
		self.AddData()
		self.dialog.close

	def TemplateList(self, qmodelindex):
		self.delbtn.setEnabled(True)
		self.buttonbox.setEnabled(True)
		item = (self.listwidget.currentItem()).text()
		

	def NewTemplate(self):
				
		self.dialog=QDialog(self)
		self.dialog.setWindowTitle("New Template")
		layout=QVBoxLayout()
		self.dialog.setLayout(layout)
		self.templatename=QLineEdit()
		self.templatename.setPlaceholderText("Type name...")

		layout.addWidget(self.templatename)
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Help)
		layout.addWidget(buttonbox)

		buttonbox.accepted.connect(self.SaveTemplate)
		buttonbox.rejected.connect(self.dialog.close)

		self.dialog.exec_()

	def SaveTemplate(self):
		self.SaveRecord()
		name=self.templatename.text()
		if self.postDic=={}:
			return False
		if name=="":
			return False
		date = QDate()
		currentdate=date.currentDate()
		year=currentdate.year()
		month=currentdate.month()
		day=currentdate.day()
		date=(str(day)+'-'+str(month)+'-'+str(year))
		keyname=name+'  '+date
		try:
			template=json.load(open("db/adjournal_template.json","r"))
			if keyname in template:
				QMessageBox.critical(self, '', "\nThe Template name '{}' already exists, Do you want \nto replace it? 	\n".format(name))
				QMessageBox.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel|QMessageBox.Help)
		except Exception as e:
			template={}

		template[keyname]=(self.postDic)
		json.dump(template,open("db/adjournal_template.json", "w"))	
		self.dialog.close()

	def Cancel_button(self):
		self.close()
		if self.journalwidget=='':
			return False
		journaltypelist=['all',"General","Payments","Sales","Receipts","Purchases"]	
		self.journalwidget.TabTable(self.journalwidget.tabs.currentIndex())
		self.journalwidget.JournalData(journaltypelist[self.currenttab],self.d1,self.d2,'No','')
		
	
	def closeEvent(self, event):
		self.Cancel_button()

	def PostData(self):
		self.SaveRecord()
		if self.error_count==0:
			self.PostJournal()			
	
	def SaveRecord(self):
		AccountsList=self.requireddata	
		self.error_count=0
		self.postDic={}
		date1=self.dateedit1.date()
		year1=str(date1.year())
		day1=str(date1.day()) if len(str(date1.day()))==2 else '0'+str(date1.day())
		month1=str(date1.month()) if len(str(date1.month()))==2 else '0'+str(date1.month())
		date=(year1+'-'+month1+'-'+day1)

		user=json.load(open("db/user.json", "r"))

		journaltype=(self.comboboxjournaltype.currentText())
		ref=(self.reflineedit.text())
		memo=(self.memo.toPlainText())

		if journaltype=="":
			QMessageBox.critical(self, '', "\nPlease select Journal type 	\n")
			self.error_count+=1
			return False
			
		Account=amount=dc=0

		rows=len(self.widgetDic)
		cols=3
		Credit_bal=Debit_bal=0
		for row in range(rows):
			postList=[]
			for col in range(cols):
				if col==0:
					Account=(self.widgetDic[row][col]).currentText()
					if Account =="":
						self.error_count+=1
						QMessageBox.critical(self, 'Account Error', "Account name cannot be empty at row %s, kindly\nselect an account from accounts dropdown list.\n"%(row+1))
						return False
					if Account not in AccountsList:
						self.error_count+=1
						QMessageBox.critical(self, 'Account Error', "The account name \"%s\" is not recognized!.	\n"%Account)
						return False
						
					postList.append(Account)
				if col==1:
		
					amount=(self.widgetDic[row][col]).text()
					if amount=='' or Account=='':
						self.MessageBox.setWindowTitle('Post Journal')
						self.MessageBox.setText("")
						self.MessageBox.setInformativeText("Empty field at row number {}\n".format(row+1))
						self.MessageBox.setIcon(self.MessageBox.Critical)
						self.MessageBox.setStandardButtons(self.MessageBox.Close)
						self.MessageBox.show()
						self.error_count+=1
						return False
					amount=float(parse_decimal(amount,locale='en_US'))	
					postList.append(amount)
				if col==2:
					dc=(self.widgetDic[row][col]).currentText()
					postList.append(dc)

					if dc=='Debit':
						Debit_bal=Debit_bal+float(amount)
					if dc=='Credit':
						Credit_bal=Credit_bal+float(amount)	
				
			postList.append(ref)
			postList.append(journaltype)
			postList.append(memo)
			postList.append(date)
			postList.append(user)
			
			self.postDic[row]=postList

		if self.postDic=={}:
			self.error_count+=1
			return False	
		if abs(Debit_bal-Credit_bal)>0.00001:
			bal=format_currency(abs(Debit_bal-Credit_bal),'NGN', locale='en_US')
			self.balencelabel.setText('Amount not yet applied to an account (out of balance): {}'.format(bal))
			self.error_count+=1
			return False
		self.balencelabel.setText('')
		

	def PostJournal(self):
		self.postDic=json.dumps(self.postDic)
		self.postDic=base64.b64encode(self.postDic.encode())
	
		data = QtCore.QByteArray()
		if self.edit_data !={}:
			data.append("option=editjournal&")

		data.append("action=postjournal&")
		data.append("journal={}".format(self.postDic.decode("utf-8")))
		url = "http://{}:5000/journal".format(self.ip)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse)
		
		#return False
		self.nam.post(req, data)

	def handleResponse(self, reply):

	    er = reply.error()

	    if er == QtNetwork.QNetworkReply.NoError:
	        bytes_string = reply.readAll()
	        
	        json_ar = json.loads(str(bytes_string, 'utf-8'))
	        #data = json_ar['form']
	        if json_ar['19']=='Success':
	        	journaltype=json_ar['30']
	        	ref=json_ar['25']
	        	date=json_ar['35']
	        	self.MessageBox.setWindowTitle('Post Journal')
	        	self.MessageBox.setText("")
	        	self.MessageBox.setInformativeText("{j} Journal with Ref: {r} was succesfully posted\non {d}. " "\n\nClick Ok to exit.".format(j=journaltype,r=ref,d=date))
	        	self.MessageBox.setIcon(self.MessageBox.Information)
	        	self.MessageBox.setStandardButtons(self.MessageBox.Ok)
	        	self.MessageBox.show()
	        	#self.table.clearContents()
	        result = self.MessageBox.exec_()
	        if result==self.MessageBox.Ok:
	        	pass
	        
	    else:
	        QMessageBox.critical(self, 'Database Connection', "\n{} 	\n".format(reply.errorString()))      

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AddJournal('',{},'','')
	ex.show()
	sys.exit(app.exec_())