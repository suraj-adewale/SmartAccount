from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency
from PyQt5.QtCore import QDate

def ViewJournal():
    if request.form.get('action')=='fetchjournal':
        conn = sqlite3.connect('db/admin.db')
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        if request.form.get('option')=='Edit':
            ref=request.form.get('ref')
            journalDic={}
            cursor = cursor.execute('''SELECT * FROM journal WHERE ref=?''',(ref,))
            data=cursor.fetchall()
            row=0
            for item in data:
                journal_list=[]
                journal_list.append(item['account']+' - '+str(item['description']))
                journal_list.append(item['amount'])
                journal_list.append(item['debit_credit'])
                journal_list.append(item['ref'])
                journal_list.append(item['journaltype'])
                journal_list.append(item['memo'])
                journal_list.append(item['date'])
                journal_list.append(item['journalid'])

                journalDic[row]=journal_list
                row=row+1
            return jsonify(journalDic)

        if request.form.get('option')=='Delete':
            date = QDate()
            currentdate=date.currentDate()
            year=str(currentdate.year())
            day1=str(currentdate.day()) if len(str(currentdate.day()))==2 else '0'+str(currentdate.day())
            month1=str(currentdate.month()) if len(str(currentdate.month()))==2 else '0'+str(currentdate.month())
            date=(year+'-'+month1+'-'+day1)

            ref=request.form.get('ref')
            memo=request.form.get('memo')
            conn.execute('''DELETE FROM journal WHERE ref=?''',(ref,))
            conn.execute('''DELETE FROM invoices WHERE ref=?''',(ref,))
            conn.execute('''DELETE FROM accountpayable WHERE payable=?''',(ref,))

            conn.execute('''UPDATE backup SET date=?,ref=?,description=?,action=?,status=? WHERE ref=?'''\
                         ,(date,ref,memo,'Delete','nobackup',ref))
            conn.commit()
        
        journaltype=request.form.get('journaltype')
        date1=request.form.get('date1')
        date2=request.form.get('date2')
        account=(request.form.get('account'))
        ref=request.form.get('ref')
        if request.form.get('option')=='Delete':
            ref=''

        journaldata={}
       
        if journaltype=='all' and account=='All Accounts':
            cursor = cursor.execute('''SELECT * FROM journal WHERE (DATE(date)>=? AND DATE(date)<=?) AND ref LIKE ? ORDER BY date DESC ''',(date1,date2,"%"+ref))
            #print(journaltype,account,date1,date2,ref)
                   
        elif journaltype=='all' and account is not 'All Accounts':
            cursor = cursor.execute('''SELECT * FROM journal WHERE account=? AND (DATE(date)>=? AND DATE(date)<=?) AND ref LIKE ? ORDER BY date DESC''',(account,date1,date2,"%"+ref))
        
        elif  account=='All Accounts':
            cursor = cursor.execute('''SELECT * FROM journal WHERE journaltype=? AND (DATE(date)>=? AND DATE(date)<=?) AND ref LIKE ? ORDER BY date DESC''',(journaltype,date1,date2,"%"+ref))
                
        elif  account is not 'All Accounts':
            cursor = cursor.execute('''SELECT * FROM journal WHERE account=? AND journaltype=? AND (DATE(date)>=? AND DATE(date)<=?) AND ref LIKE ? ORDER BY date DESC ''',(account,journaltype,date1,date2,"%"+ref))
        else: pass    
               
        data=cursor.fetchall()
        row=totalc=totald=0
        for col in data:
            
            col_list=[]
            col_list.append(str(col['date']))
            col_list.append(str(col['journaltype']))
            col_list.append(str(col['ref']))
            col_list.append(str(col['memo']))
            col_list.append(str(col['account']))
            col_list.append(str(col['description']))
            if (col['debit_credit'])=='Debit':
                totald=totald+col['amount']
                col_list.append(str(format_currency(col['amount'],'', locale='en_US')))
                col_list.append('')
            if (col['debit_credit'])=='Credit':
                totalc=totalc+col['amount']
                col_list.append('')
                col_list.append(str(format_currency(col['amount'],'', locale='en_US')))
            col_list.append(str(col['user']))
            
            journaldata[row]=col_list
            row=row+1
        totald=str(format_currency(totald,'', locale='en_US'))
        totalc=str(format_currency(totalc,'', locale='en_US'))
        total=[totald,totalc]
        journal=[journaldata,total] 
        #print(journal)   
        return jsonify(journal)