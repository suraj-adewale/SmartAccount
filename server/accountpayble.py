from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def ViewPayable():
	if request.form.get('action')=='accountspayable':
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		date1=request.form.get('date1')
		date2=request.form.get('date2')
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
			for paid in cursor.execute('''SELECT total(amountpaid) AS paid  from accountpayable WHERE payable=? AND (DATE(date)>=? AND DATE(date)<=?)''',(data['payable'],date1,date2)).fetchall():
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
		return jsonify(accountpayableDic)