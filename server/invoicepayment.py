from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def InvoivePaymentReport():
	if request.form.get('action')=='invoicepayment':
		date1=request.form.get('date1')
		date2=request.form.get('date2')
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		sql = cursor.execute("SELECT * FROM invoices WHERE (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",(date1,date2))
		array=sql.fetchall()
		data={}	
		InvoiceDic={}
		
		key=0
		totalamount=[]
		amount=0
		for row in array:
			
			if float(row['amountpaid'])>0:
				List=[]
				List.append(row['date'])
				List.append(row['invoice'])
				List.append(row['customer'])
				List.append(row['method'])
				List.append(row['ref'])
				List.append(format_currency(float(row['amountpaid']),'NGN', locale='en_US'))
			
				InvoiceDic[key]=List
				amount=amount+float(row['amountpaid'])
				key=key+1
		List=[]
		List.append('')
		List.append('')
		List.append('')
		List.append('')
		List.append('')
		List.append('')
		InvoiceDic[key]=List
		key=key+1
		methods=["Cash","Check","Credit Card","Bank Deposit","Other"]
		subtotal={}
		for method in methods:
			sql = cursor.execute("SELECT total(amountpaid) AS subtotal FROM invoices WHERE method=? AND (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",(method,date1,date2))
			array=sql.fetchall()
			for sub in array:
				
				if sub['subtotal']>0.0:
					List=[]
					List.append('Subtotal')
					List.append(method)
					List.append('')
					List.append('')
					List.append('')
					List.append(format_currency(float(sub['subtotal']),'NGN', locale='en_US'))
					InvoiceDic[key]=List
					key=key+1
					subtotal[method]=format_currency(float(sub['subtotal']),'NGN', locale='en_US')
		List=[]
		List.append('Total')
		List.append('')
		List.append('')
		List.append('')
		List.append('')
		List.append(format_currency(float(amount),'NGN', locale='en_US'))
		InvoiceDic[key]=List

		totalamount.append(format_currency(0,'NGN', locale='en_US'))	
		totalamount.append(format_currency(float(amount),'NGN', locale='en_US'))	
		data['invoicepaymentdata']=InvoiceDic
		data['total']=totalamount			

		data['subtotal']=subtotal			


		return jsonify(data)