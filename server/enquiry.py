from flask import Flask,request, jsonify
import threading,json,sqlite3,base64
from babel.numbers import format_currency

def ViewAccountEnquiry():
	if request.form.get('action')=='accountsenquiry':
		date1=request.form.get('date1')
		date_=request.form.get('date2')

		decode=base64.b64decode(date_)
		date_=json.loads(decode.decode("utf-8"))
		date2=date_[0]
		accdesc=date_[1]
		
		acc_descrip_list=accdesc.split(' - ')
		acc=str(acc_descrip_list[0])
		desc=acc_descrip_list[1]

		GeneralLedgerDic={}
		description_list=[]
		description_list.append(desc)
		conn = sqlite3.connect('db/admin.db')
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		cursor = cursor.execute("SELECT * FROM journal WHERE description=? AND (DATE(date)>=? AND DATE(date)<=?) ORDER BY date",(desc,date1,date2) )
		ledgerData=cursor.fetchall()
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

		GeneralLedgerDic[desc]=ledgerList
	GeneralLedgerDic['description_list']=description_list   
	return jsonify(GeneralLedgerDic)