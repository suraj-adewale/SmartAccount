from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def InvoiveReport():
	
	if request.form.get('action')=='edit_invoices':
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		InvoiceDic={}
		data={}
		data1={}
		ref=request.form.get('ref')
		sql = cursor.execute("SELECT * FROM invoices WHERE ref=?",(ref,))
		array=sql.fetchall()
		key=0
		for row in array:
			List=[]
			List1=[]
			List.append(row['account'])
			List.append(row['description'])
			List.append(row['account']+' - '+row['description'])
			List.append(row['account1'])
			List.append(row['description1'])
			List.append(row['account1']+' - '+row['description1'])
			List.append(row['customer'])
			List.append(row['address'])
			List.append(row['ref'])
			List.append(row['invoice'])
			List.append(row['date'])
			List.append(row['salesperson'])
			List.append(row['method'])
			List.append(row['status'])
			
			List1.append(row['qty'])
			List1.append(row['item'])
			List1.append(row['item_desc'])
			List1.append(row['unitprice'])
			List1.append(row['tax'])
			List1.append(row['amount'])
			
			data[key]=List
			data1[key]=List1
			key=key+1

		InvoiceDic[0]=data
		InvoiceDic[1]=data1	
		return jsonify(InvoiceDic)		

	if request.form.get('action')=='invoices':
		date1=request.form.get('date1')
		date2=request.form.get('date2')
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		sql = cursor.execute("SELECT * FROM invoices WHERE (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",(date1,date2))
		array=sql.fetchall()
		InvoiceDic={}
		
		key=0
		totalamount=[]
		amount=0
		for row in array:
			List=[]
			List.append(row['date'])
			List.append(row['invoice'])
			List.append(row['customer'])
			List.append(row['salesperson'])
			if float(row['amount'])<=float(row['amountpaid']):
				List.append('Paid')
			elif(float(row['amountpaid']))>0.0 and float(row['amount'])>float(row['amountpaid']) :
				List.append('Partially paid')
			elif float(row['amountpaid'])==0.0 :
				List.append(row['status'])
			List.append(format_currency(0,'NGN', locale='en_US'))
			List.append(format_currency(float(row['amount']),'NGN', locale='en_US'))
			InvoiceDic[key]=List
			amount=amount+float(row['amount'])
			key=key+1
		data={}	
		totalamount.append(format_currency(0,'NGN', locale='en_US'))	
		totalamount.append(format_currency(float(amount),'NGN', locale='en_US'))	
		data['invoicedata']=InvoiceDic
		data['total']=totalamount   
		return jsonify(data)