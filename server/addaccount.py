from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def AddAccount():
	conn = sqlite3.connect('db/admin.db')

	if request.form.get('action')=='addaccount':

		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()

		data=(request.form.get('account'))
		option=(request.form.get('option'))
		sqldata=json.loads(data)

		accountnumber=sqldata[0]
		acctname=sqldata[1]
		Type=sqldata[2]
		reportgroup=sqldata[3]
		cashflow=sqldata[4]
		balance=sqldata[5]
		cursor.execute('''SELECT count(*) as count FROM accountdetails WHERE\
		account=? OR description=? ''',(accountnumber,acctname))
		data=cursor.fetchone()

		if option=="Delete":
			cursor.execute('''SELECT ref FROM journal WHERE account=? ''',(accountnumber,))
			data=cursor.fetchall()
			for ref in (data):
				cursor.execute('''DELETE  FROM  journal Where  ref=?''',(ref[0],))
			cursor.execute('''DELETE  FROM  accountdetails Where  account=?''',(accountnumber,))
			conn.commit()
			return jsonify({2:"accountdeleted"})
		
		if len(option)>0:
			cursor.execute('''UPDATE  accountdetails SET account=?,description=?,type=?,reportgroup=?,cashflow=?,balance=?
				Where  account=?''',(accountnumber,acctname,Type,reportgroup,cashflow,balance,option))
			conn.commit()

			cursor.execute('''UPDATE  journal SET account=?,description=?
				Where  account=?''',(accountnumber,acctname,option))
			conn.commit()
			return jsonify({2:"accountedited"})

		if data[0]>0:
			return jsonify({2:"accountexists"})
		else:	
			cursor.execute('''INSERT INTO accountdetails(account,description,type,reportgroup,cashflow,balance)
			VALUES (?,?,?,?,?,?) ''',(accountnumber,acctname,Type,reportgroup,cashflow,balance))
			conn.commit()
			return jsonify({2:"accountcreated"})