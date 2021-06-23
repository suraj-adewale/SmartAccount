from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def ViewLedger():
	if request.form.get('action')=='fetchledger':
		date1=request.form.get('date1')
		date2=request.form.get('date2')
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		cursor1 = cursor.execute("SELECT DISTINCT description FROM journal WHERE (DATE(date)>=? AND DATE(date)<=?) ORDER BY account",(date1,date2))
		current_account=cursor1.fetchall()
		GeneralLedgerDic={}
		description_list=[]
		for row in current_account:
		    description_list.append(row['description'])

		    cursor=conn.cursor()
		    cursor2 = cursor.execute("SELECT * FROM journal WHERE description=? AND (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",(row['description'],date1,date2) )
		    ledgerData=cursor2.fetchall()
		    ledgerList=[]
		    total_debit=total_credit=0
		    for data in ledgerData:
		        dataList=[]
		        dataList.append(data['date'])
		        dataList.append(data['memo'])
		        dataList.append(data['ref'])
		        #dataList.append(data['account'])
		        if (data['debit_credit'])=='Debit':
		            dataList.append(str(format_currency(data['amount'],'', locale='en_US')))
		            dataList.append('')
		            total_debit=total_debit+ data['amount']
		        if (data['debit_credit'])=='Credit':
		            dataList.append('')
		            dataList.append(str(format_currency(data['amount'],'', locale='en_US')))
		            total_credit=total_credit+ data['amount']

		        accounttype=(str(data['account']))[0]
		        
		        if accounttype== '1':   
		            bal=(total_credit - total_debit)
		        if accounttype== '2':   
		            bal=(total_debit - total_credit)
		        if accounttype== '3':   
		            bal=(total_debit - total_credit)
		        if accounttype== '4':   
		            bal=(total_credit - total_debit)            

		        dataList.append(str(format_currency(bal,'', locale='en_US')))
		        dataList.append(data['account'])
		        ledgerList.append(dataList)
		    GeneralLedgerDic[row['description']]=ledgerList
		GeneralLedgerDic['description_list']=description_list   
		return jsonify(GeneralLedgerDic)