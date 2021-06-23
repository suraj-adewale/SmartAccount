from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency
def ViewTrialbalance():
    if request.form.get('action')=='fetchtrialbalance':
        date1=request.form.get('date1')
        date2=request.form.get('date2')
        conn = sqlite3.connect('db/admin.db')
        conn.row_factory=sqlite3.Row

        cursor=conn.cursor()
        cursor1 = cursor.execute("SELECT DISTINCT description, account FROM journal WHERE (DATE(date)>=? AND DATE(date)<=?) ORDER BY account",(date1,date2))
        current_account=cursor1.fetchall()
        balanceDic={}
        description_list=[]
        total_debit=0
        total_credit=0
        for row in current_account:
            description_list.append(row['description'])

            cursor=conn.cursor()
            cursor2 = cursor.execute("SELECT * FROM journal WHERE description=? AND (DATE(date)>=? AND DATE(date)<=?) ORDER BY date"\
                ,(row['description'],date1,date2) )
            ledgerData=cursor2.fetchall()
            
            dataList=[]
            debit=credit=0        
            for data in ledgerData:
		        
                if (data['debit_credit'])=='Debit':
                    debit=debit+ data['amount']
                if (data['debit_credit'])=='Credit':
                    credit=credit+ data['amount']

            if (debit - credit)>0:
                debit_bal=(debit - credit)
                dataList.append(debit_bal)
                dataList.append('')
                total_debit=total_debit+debit_bal
            if (debit - credit)<0:
                credit_bal=abs(debit - credit)
                dataList.append('')
                dataList.append(credit_bal)
                total_credit=total_credit+credit_bal
            if debit == credit:
                credit_bal=abs(debit - credit)
                dataList.append(0)
                dataList.append('')    
            dataList.append(row['account'])                
            balanceDic[row['description']]=dataList

        balance=[str(format_currency(total_debit,'', locale='en_US')),str(format_currency(total_credit,'', locale='en_US'))]
        balanceDic['bal']=balance
        balanceDic['description_list']=description_list
        conn.close()
        return jsonify(balanceDic)   
		     
            
