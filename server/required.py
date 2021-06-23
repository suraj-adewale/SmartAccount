from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

DATA={}
def RequiredData():
	if request.form.get('action')=='required':

		SelectAccounts()
		SelectReportCode()	
		SuppliersData()
		PaySuppliersData()
		InvoicePaymemtData()
		CashAccounts()
		PayableData()
		InvoiceData()
		Invoice()
		Chart()
		AccountPayableData()
		Backup()


		return jsonify(DATA)

def Backup():
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	backup={}
	cursor = cursor.execute('''SELECT * FROM backup WHERE status=? ORDER BY date  ''',('nobackup',))
	data=cursor.fetchall()
	row=0
	for item in data:
	    data_list=[]
	    data_list.append(item['date'])
	    data_list.append(item['ref'])
	    data_list.append(item['description'])
	    data_list.append(item['action'])
	    backup[row]=data_list
	    row=row+1
	DATA['backup']=backup
     
def SelectAccounts():
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	accounts=[]
	cursor = cursor.execute("SELECT account, description FROM accountdetails")
	current_account=cursor.fetchall()
	for row in current_account:
		accounts.append(str(row['account']+" - "+row['description']))
	DATA['accounts']=accounts

def SelectReportCode():
	reportcode=[]
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	cursor = cursor.execute("SELECT code, name FROM reportgroup")
	current_reportcode=cursor.fetchall()
	for row in current_reportcode:
		reportcode.append(str(row['code']+" - "+row['name']))
	DATA['selectreportcode']=reportcode	

def SuppliersData():
	supplierDic={}
	key=0
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	cursor = cursor.execute("SELECT supplierid,suppliername,address, phone1 FROM suppliers")
	suppliers=cursor.fetchall()
	for items in suppliers:
		supplierList=[]
		cursor = cursor.execute("SELECT (total(amount) - total(amountpaid)) AS payable, duedate FROM accountpayable WHERE supplier=?",(items["suppliername"],))
		supplier=cursor.fetchall()
		for item in supplier:
			supplierList.append(items["suppliername"])
			supplierList.append(item["payable"])
			supplierList.append(item["duedate"])
			supplierList.append(items["phone1"])
			supplierList.append(items["address"])
			supplierList.append(items["supplierid"])
		supplierDic[key]=supplierList
		key=key+1
	DATA['suppliersdata']=supplierDic		

def PaySuppliersData():
	paysupplierDic={}
	key=0
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	cursor = cursor.execute("SELECT suppliername FROM suppliers")
	suppliers=cursor.fetchall()
	for item in suppliers:
		cursor=conn.cursor()
		cursor = cursor.execute("SELECT * FROM accountpayable WHERE supplier=?",(item["suppliername"],))
		supplier=cursor.fetchall()
		suppliersList=[]
		for items in supplier:
			supplierList=[]
			supplierList.append(items["supplier"])
			supplierList.append(items["date"])
			supplierList.append(items["duedate"])
			supplierList.append(items["payable"])
			supplierList.append(items["amount"])
			supplierList.append(float(items["amount"])-float(items["amountpaid"]))
			suppliersList.append(supplierList)
		paysupplierDic[item["suppliername"]]=suppliersList
			
	DATA['paysuppliersdata']=paysupplierDic

def InvoicePaymemtData():
	payInvoiceDic={}
	key=0
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	cursor = cursor.execute("SELECT customerid,phone1,customername FROM customers")
	customers=cursor.fetchall()
	for item in customers:
		cursor=conn.cursor()
		cursor = cursor.execute("SELECT * FROM invoices WHERE customerid=? ORDER BY ref, date DESC",(item["customerid"],))
		customer=cursor.fetchall()
		customersList=[]
		for items in customer:
			customerList=[]
			customerList.append(items["customer"])
			customerList.append(items["date"])
			customerList.append(items["duedate"])
			customerList.append(items["ref"])
			customerList.append(items["amount"])
			customerList.append(float(items["amount"])-float(items["amountpaid"]))
			customerList.append(items["invoiceid"])
			customerList.append(items["account"]+' - '+items["description"])
			customersList.append(customerList)
		payInvoiceDic[item["customername"]]=customersList
	DATA['invoicepaymentdata']=payInvoiceDic

def CashAccounts():
	cashaccountDic={}
	key=0
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	for data in cursor.execute('''SELECT balance, account, description from accountdetails WHERE  reportgroup>=? AND reportgroup<=? ''',(310101,310201)).fetchall():
		bal=(data['balance'])
		if bal==None or bal=='':
			bal=0
		cursor1=cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (description=? )) - (SELECT total(amount)\
				 	FROM journal WHERE debit_credit=? AND (description=?) )  AS amount ''',('Debit',data['description'],'Credit',data['description']))
		cash=cursor1.fetchall()
		cashaccountList=[]
		for item in cash:
			cashaccountList.append(data['account'])
			cashaccountList.append(data['description'])
			cashaccountList.append((float(bal)+item['amount']))
		cashaccountDic[key]=cashaccountList
		key=key+1
	DATA['cashaccounts']=cashaccountDic

def PayableData():
	payableDic={}
	key=0
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	for data in cursor.execute('''SELECT balance, account, description from accountdetails WHERE  reportgroup>=? AND reportgroup<=? ''',(410401 , 410501)).fetchall():
		bal=(data['balance'])
		if bal==None or bal=='':
			bal=0
		cursor1=cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (description=? )) - (SELECT total(amount)\
				 	FROM journal WHERE debit_credit=? AND (description=?) )  AS amount ''',('Credit',data['description'],'Debit',data['description']))
		payableList=[]
		payable=cursor1.fetchall()
		for item in payable:
			payableList.append(data['description'])
			payableList.append(-(float(bal)+item['amount'])) if abs(float(bal)+item['amount'])>0 else payableList.append((float(bal)+item['amount']))
			payableList.append(data['account']+" - "+data['description'])
		payableDic[key]=payableList	
		key=key+1	
	DATA['payabledata']=payableDic

def InvoiceData():
	invoicedataDic={}
	key=0
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	for ref in cursor.execute('''SELECT DISTINCT ref FROM invoices ORDER BY ref, date DESC''').fetchall():
		for data in cursor.execute('''SELECT date,duedate,status,customer,invoice,ref,total(amount) AS amount, total(amountpaid) AS paid from invoices WHERE ref=? ''',(ref['ref'],)).fetchall():
			accountpayableList=[]
			accountpayableList.append(data['date'])
			accountpayableList.append(data['duedate'])
			accountpayableList.append(data['ref'])
			accountpayableList.append(data['invoice'])
			accountpayableList.append(data['customer'])
			accountpayableList.append(data['amount'])
	
			due=float(data['amount'])-data['paid']
			accountpayableList.append(due)
			if due==0.0:
				accountpayableList.append('Paid')	
			
			if data['paid']==0.0:
				accountpayableList.append(data['status'])
			if due>0.0 and data['paid']>0.0 :
				accountpayableList.append('Part payment')

		invoicedataDic[key]=accountpayableList
		key=key+1		
	DATA['invoicedata']=invoicedataDic

def Invoice():
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	data={}
	revenueDic={}
	key=0
	cursor = cursor.execute("SELECT account,description FROM accountdetails  WHERE type=?",("Revenue",))
	revenue=cursor.fetchall()
	for account in revenue:
		accountlist=[]
		accountlist.append(account['account'])
		accountlist.append(account['description'])
		accountlist.append(account['account']+" - "+account['description'])
		revenueDic[key]=accountlist
		key=key+1
	data['revenueaccounts']=revenueDic

	customersDic={}
	key=0
	cursor = cursor.execute("SELECT * FROM customers")
	Customers=cursor.fetchall()
	for items in Customers:
		customerList=[]
		cursor = cursor.execute("SELECT (total(amount) - total(amountpaid)) AS balance,salesperson,invoice, \
			duedate FROM invoices WHERE customerid=? ORDER BY duedate DESC ",(items["customerid"],))
		customer=cursor.fetchall()
		for item in customer:
			customerList.append(items["customername"])
			customerList.append(item["balance"])
			customerList.append(item["duedate"])
			customerList.append(item["invoice"])
			customerList.append(item["salesperson"])
			customerList.append("Default")
			customerList.append(items["phone1"])
			customerList.append(items["address"])
			customerList.append(items["customerid"])
		customersDic[key]=customerList
		key=key+1
	data['customerdata']=customersDic

	cursor.execute("SELECT invoice FROM invoices ORDER BY invoice DESC LIMIT 1")
	count=cursor.fetchone()
	if count==None:
		invoiceno=str(10000)
	else:
		invoice=(count['invoice'])
		invoiceno=str(int(invoice)+1)
	data['invoiceno']=invoiceno


	key=0
	receivableDic={}
	cursor=conn.cursor()
	cursor = cursor.execute("SELECT account,description  FROM  accountdetails WHERE type=? AND (reportgroup>=? AND reportgroup<=?)",('Asset',310601 , 310604))
	receivable=cursor.fetchall()
	for account in receivable:
		accountlist=[]
		accountlist.append(account['account'])
		accountlist.append(account['description'])
		accountlist.append(account['account']+" - "+account['description'])
		receivableDic[key]=accountlist
		key=key+1	
	data['receivableaccounts']=receivableDic
	DATA['addinvoice']=data

def Chart():
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	assetsList=[]
	incomeList=[]
	liabilityList=[]
	equityList=[]
	expenseList=[]

	#DATA={}
	mainDic={}

	cursor = cursor.execute("SELECT * FROM accountdetails ORDER BY account")
	account=cursor.fetchall()

	total=[]
	totalasset=totalrevenue=totalliability=totalequity=totalexpense=0
	
	for row in account:
		if row['type']=='Asset':
			assets=[]
			
			for bal in cursor.execute('''SELECT total(balance) AS bal from accountdetails WHERE account=? ''',(row['account'],)).fetchall():
				bal_amount=bal['bal']
			for item in cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (account=? )) - (SELECT total(amount)\
			 	FROM journal WHERE debit_credit=? AND (account=?) )  AS amount ''',('Debit',row['account'],'Credit',row['account'])).fetchall():
			
				assets.append(row['account'])
				assets.append(row['description'])
				assets.append(format_currency(item['amount']+bal_amount,'', locale='en_US'))
				assets.append(row['type'])
				assets.append(row['reportgroup'])
				totalasset=totalasset+item['amount']+bal_amount
				assetsList.append(assets)
				
			mainDic['assets']=assetsList

		if row['type']=='Revenue':
			income=[]
			for bal in cursor.execute('''SELECT total(balance) bal from accountdetails WHERE account=? ''',(row['account'],)).fetchall():
				bal_amount=bal['bal']
			for item in cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (account=? )) - (SELECT total(amount)\
			 	FROM journal WHERE debit_credit=? AND (account=?) )  AS amount ''',('Credit',row['account'],'Debit',row['account'])).fetchall():
			
				income.append(row['account'])
				income.append(row['description'])
				income.append(format_currency(item['amount']+bal_amount,'', locale='en_US'))
				income.append(row['type'])
				income.append(row['reportgroup'])
				totalrevenue=totalrevenue+item['amount']+bal_amount
				incomeList.append(income)
				
			mainDic['income']=incomeList

		if row['type']=='Expense':
			expense=[]
			for bal in cursor.execute('''SELECT total(balance) bal from accountdetails WHERE account=? ''',(row['account'],)).fetchall():
				bal_amount=bal['bal']
			for item in cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (account=? )) - (SELECT total(amount)\
			 	FROM journal WHERE debit_credit=? AND (account=?) )  AS amount ''',('Debit',row['account'],'Credit',row['account'])).fetchall():
			
				expense.append(row['account'])
				expense.append(row['description'])
				expense.append(format_currency(item['amount']+bal_amount,'', locale='en_US'))
				expense.append(row['type'])
				expense.append(row['reportgroup'])
				totalexpense=totalexpense+item['amount']+bal_amount
				expenseList.append(expense)
				
			mainDic['expense']=expenseList	

		if row['type']=='Liability':
			liability=[]
			for bal in cursor.execute('''SELECT total(balance) bal from accountdetails WHERE account=? ''',(row['account'],)).fetchall():
				bal_amount=bal['bal']
			for item in cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (account=? )) - (SELECT total(amount)\
			 	FROM journal WHERE debit_credit=? AND (account=?) )  AS amount ''',('Credit',row['account'],'Debit',row['account'])).fetchall():
			
				liability.append(row['account'])
				liability.append(row['description'])
				liability.append(format_currency(item['amount']+bal_amount,'', locale='en_US'))
				liability.append(row['type'])
				liability.append(row['reportgroup'])
				totalliability=totalliability+item['amount']+bal_amount
				liabilityList.append(liability)
				
			mainDic['liability']=liabilityList	

		if row['type']=='Equity':
			equity=[]
			for bal in cursor.execute('''SELECT total(balance) bal from accountdetails WHERE account=? ''',(row['account'],)).fetchall():
				bal_amount=bal['bal']
			for item in cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (account=? )) - (SELECT total(amount)\
			 	FROM journal WHERE debit_credit=? AND (account=?) )  AS amount ''',('Credit',row['account'],'Debit',row['account'])).fetchall():
			
				equity.append(row['account'])
				equity.append(row['description'])
				equity.append(format_currency(item['amount']+bal_amount,'', locale='en_US'))
				equity.append(row['type'])
				equity.append(row['reportgroup'])
				totalequity=totalequity+item['amount']+bal_amount
				equityList.append(equity)
				
			mainDic['equity']=equityList


	total.append(format_currency(totalrevenue,'', locale='en_US'))
	total.append(format_currency(totalexpense,'', locale='en_US'))
	total.append(format_currency(totalasset,'', locale='en_US'))
	total.append(format_currency(totalliability,'', locale='en_US'))
	total.append(format_currency(totalequity,'', locale='en_US'))
	
	mainDic['total']=total		
	DATA['viewchart']=mainDic

def AccountPayableData():
	conn = sqlite3.connect('db/admin.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	
	accountpayableDic={}
	key=0
	cursor=conn.cursor()
	for data in cursor.execute('''SELECT * from accountpayable ORDER BY payable DESC''').fetchall():
		accountpayableList=[]
		accountpayableList.append(data['date'])
		accountpayableList.append(data['duedate'])
		accountpayableList.append(data['ref'])
		accountpayableList.append(data['payable'])
		accountpayableList.append(data['supplier'])
		accountpayableList.append(data['amount'])
		for paid in cursor.execute('''SELECT total(amountpaid) AS paid  from accountpayable WHERE payable=?''',(data['payable'],)).fetchall():
			due=float(data['amount'])-paid['paid']
			accountpayableList.append(due)
		if due==0.0:
			accountpayableList.append('Paid')	
		
		if paid['paid']==0.0:
			accountpayableList.append(data['status'])
		if due>0.0 and paid['paid']>0.0 :
			accountpayableList.append('Part payment')
		accountpayableList.append(data['payableref'])
		accountpayableDic[key]=accountpayableList
		key=key+1		
	DATA['accountpayable']=accountpayableDic	


	#DATA['19']='Success'
