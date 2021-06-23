from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def AddCustomer():

	if request.form.get('action')=='editcustomer':
		conn = sqlite3.connect('db/admin.db')
		cursor=conn.cursor()
		data=request.form.get('customer')
		sqldata=json.loads(data) 

		name=sqldata[0]
		phone1=sqldata[4]
		address=sqldata[3]
		customerid=sqldata[9]
		cursor.execute('''UPDATE customers SET customername=?,address=?,phone1=?  WHERE customerid=?''',(name,address,phone1,customerid))
		conn.commit()
		
		customersDic={}
		key=0
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
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
		return jsonify(customersDic)

	if request.form.get('action')=='deletecustomer':
		conn = sqlite3.connect('db/admin.db')
		cursor=conn.cursor()
		customerid=request.form.get('customerid')
		cursor.execute('''DELETE FROM customers WHERE customerid=?''',(customerid,))
		conn.commit()

		return jsonify({'delete':'yes'})

	if request.form.get('action')=='addcustomer':
		conn = sqlite3.connect('db/admin.db')

		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()

		data=request.form.get('customer')
		sqldata=json.loads(data) 

		name=sqldata[0]
		contact=sqldata[1]
		firstname=sqldata[2]
		address=sqldata[3]
		phone1=sqldata[4]
		phone2=sqldata[5]
		mail=sqldata[6]
		info=sqldata[7]
		term=sqldata[8]

		cursor.execute('''INSERT INTO customers(customername,contactperson,firstname,address,phone1,phone2,email,info,term)
		VALUES (?,?,?,?,?,?,?,?,?) ''',(name,contact,firstname,address,phone1,phone2,mail,info,term))
		conn.commit()
		
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
		return jsonify(customersDic)