from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency
from PyQt5.QtCore import QDate

def BackUp():
    if request.form.get('action')=='fetchbackup':
        conn = sqlite3.connect('db/admin.db')
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        if request.form.get('option')=='online_response':
            ref1=request.form.get('ref') 
            for ref in eval(ref1):
                #print(ref)
                conn.execute('''UPDATE backup SET status=? WHERE ref=?''',('backup',ref)) 
            conn.commit()

            backup={}
            cursor = cursor.execute('''SELECT * FROM backup WHERE status=? ORDER BY date  ''',('nobackup',))
            data=cursor.fetchall()
            row=0
            for item in data:
                data_list=[]
                data_list.append(item['date'])
                data_list.append(item['ref'])
                data_list.append(item['description'])
                data_list.append(item['action'])
                backup[row]=data_list
                row=row+1
            return jsonify({'key':'backupref','data':backup})

        if request.form.get('option')=='backupref':
            backup={}
            cursor = cursor.execute('''SELECT * FROM backup WHERE status=? ORDER BY date  ''',('nobackup',))
            data=cursor.fetchall()
            row=0
            for item in data:
                data_list=[]
                data_list.append(item['date'])
                data_list.append(item['ref'])
                data_list.append(item['description'])
                data_list.append(item['action'])
                backup[row]=data_list
                row=row+1
            return jsonify({'key':'backupref','data':backup})    

        if request.form.get('option')=='backupdata':
            ref=request.form.get('ref') 
            backup={}
            cursor = cursor.execute('''SELECT journal.account AS account,journal.description AS description,journal.amount AS amount,journal.debit_credit AS debit_credit,
                journal.ref AS ref, journal.journaltype AS journaltype, journal.memo AS memo,journal.date AS date, journal.user AS user, journal.invoiceid AS invoiceid,backup.status
                AS backup,backup.action AS action FROM journal  INNER JOIN backup ON journal.ref=backup.ref  WHERE journal.ref=? AND backup.status=?''',(ref,'nobackup'))
            data=cursor.fetchall()
            row=0
            for item in data:
                journal_list=[]
                journal_list.append(item['account'])
                journal_list.append(item['description'])
                journal_list.append(item['amount'])
                journal_list.append(item['debit_credit'])
                journal_list.append(item['ref'])
                journal_list.append(item['journaltype'])
                journal_list.append(item['memo'])
                journal_list.append(item['date'])
                journal_list.append(item['user'])
                journal_list.append(item['invoiceid'])
                journal_list.append(item['action'])
                journal_list.append(item['backup'])

                backup[row]=journal_list
                row=row+1
            return jsonify({'key':'backupdata','data':backup})

        if request.form.get('option')=='backupdataall':
            refs=request.form.get('ref')
            backup={}
            row=0
            for ref in eval(refs):
                cursor = cursor.execute('''SELECT journal.account AS account,journal.description AS description,journal.amount AS amount,journal.debit_credit AS debit_credit,
                    journal.ref AS ref, journal.journaltype AS journaltype, journal.memo AS memo,journal.date AS date, journal.user AS user, journal.invoiceid AS invoiceid,backup.status
                    AS backup,backup.action AS action FROM journal  INNER JOIN backup ON journal.ref=backup.ref  WHERE journal.ref=? AND backup.status=?''',(ref,'nobackup'))
                data=cursor.fetchall()
                for item in data:
                    journal_list=[]
                    journal_list.append(item['account'])
                    journal_list.append(item['description'])
                    journal_list.append(item['amount'])
                    journal_list.append(item['debit_credit'])
                    journal_list.append(item['ref'])
                    journal_list.append(item['journaltype'])
                    journal_list.append(item['memo'])
                    journal_list.append(item['date'])
                    journal_list.append(item['user'])
                    journal_list.append(item['invoiceid'])
                    journal_list.append(item['action'])
                    journal_list.append(item['backup'])

                    backup[row]=journal_list
                    row=row+1
            return jsonify({'key':'backupdataall','data':backup})           