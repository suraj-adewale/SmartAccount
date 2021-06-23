from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def Balance():
	conn = sqlite3.connect('db/admin.db')

	if request.form.get('action')=='balance':

		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()

		desc=(request.form.get('description'))
		 

		cursor=cursor.execute('''SELECT (SELECT total(amount)  FROM journal WHERE debit_credit=? AND (description=? )) - (SELECT total(amount)\
			 	FROM journal WHERE debit_credit=? AND (description=?) )  AS amount ''',('Debit',desc,'Credit',desc))
		amount=cursor.fetchall()
		return jsonify({'bal':'{}'.format(amount[0][0])})