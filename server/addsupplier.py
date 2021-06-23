from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def AddSupplier():

	if request.form.get('action')=='editsupplier':
		conn = sqlite3.connect('db/admin.db')
		cursor=conn.cursor()
		data=request.form.get('supplier')
		sqldata=json.loads(data) 

		name=sqldata[0]
		phone1=sqldata[4]
		address=sqldata[3]
		supplierid=sqldata[10]
		cursor.execute('''UPDATE suppliers SET suppliername=?,address=?,phone1=?  WHERE supplierid=?''',(name,address,phone1,supplierid))
		conn.commit()
		
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
		
		return jsonify(supplierDic)


	if request.form.get('action')=='deletesupplier':
		conn = sqlite3.connect('db/admin.db')
		cursor=conn.cursor()
		supplierid=request.form.get('supplierid')
		cursor.execute('''DELETE FROM suppliers WHERE supplierid=?''',(supplierid,))
		conn.commit()
		return jsonify({'delete':'yes'})

	if request.form.get('action')=='addsupplier':
		conn = sqlite3.connect('db/admin.db')

		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()

		data=request.form.get('supplier')
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
		tax=sqldata[9]

		cursor.execute('''INSERT INTO suppliers(suppliername,contactperson,firstname,address,phone1,phone2,email,info,term,tax)
			VALUES (?,?,?,?,?,?,?,?,?,?) ''',(name,contact,firstname,address,phone1,phone2,mail,info,term,tax))
		conn.commit()
		
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
		
		return jsonify(supplierDic)
