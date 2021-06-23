from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def IncomeStatement():
	if request.form.get('action')=='incomestatement':
		date1=request.form.get('date1')
		date2=request.form.get('date2')
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		cursor1 = cursor.execute("SELECT  description FROM journal WHERE (account LIKE ? OR account LIKE ?) AND (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",('1%','2%',date1,date2))
		current_account=cursor1.fetchall()
		incomestatement={}
		expense={}
		revenue={}
		
		for row in current_account:
			
			cursor=conn.cursor()
			cursor2 = cursor.execute("SELECT * FROM journal WHERE description=? AND (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",(row['description'],date1,date2) )
			ledgerData=cursor2.fetchall()
			total_debit=total_credit=0
			for data in ledgerData:
				if (data['debit_credit'])=='Debit':
				    total_debit=total_debit+ data['amount']
				if (data['debit_credit'])=='Credit':
					total_credit=total_credit+ data['amount']

			accounttype=(str(data['account']))[0]
			    
			if accounttype == '1':  
				bal=(total_credit - total_debit)
				revenue[row['description']]=bal
			    
			if accounttype == '2':   
				bal=(total_debit - total_credit)
				expense[row['description']]=bal
				
			
		incomestatement['revenue']=revenue
		incomestatement['expense']=expense
		incomestatement['net']=sum(revenue.values()) - sum(expense.values())
		
		return jsonify(incomestatement)