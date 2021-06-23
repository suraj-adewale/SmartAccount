from flask import Flask,request, jsonify
import threading,json,sqlite3,base64
from babel.numbers import format_currency

def PostJournal():
    if request.form.get('action')=='postjournal':
                  
        journal=(request.form.get('journal'))
        decode=base64.b64decode(journal)
        journal=json.loads(decode.decode("utf-8"))    
        dicKeys=journal.keys()
        dicKeys=sorted(dicKeys)

        conn = sqlite3.connect('db/admin.db')
        journalAuto=(journal['0'][3])
        journaltype=(journal['0'][4])

        if journalAuto=="GJ[AUTO]" or journalAuto=="PMT[AUTO]" or journalAuto=="SLS[AUTO]" or journalAuto=="REC[AUTO]" or journalAuto=="PRC[AUTO]":
            journalAuto=journalAuto.split('[AUTO]')
            cursor=conn.cursor()
            ref1=journalAuto[0]
            cursor.execute('''SELECT ref FROM journal WHERE journaltype=? ORDER BY ref DESC LIMIT 1''',(journaltype,))
            count=cursor.fetchone()
            if count==None:
                ref=ref1+str(100000)  
            else:
                ref2=(count[0]).split(ref1)
                ref=ref1+str(int(ref2[1])+1)
        else:
            ref=(journal['0'][3])

        if request.form.get('option')=='editjournal':
            conn.execute('''DELETE FROM journal WHERE ref=?''',(ref,))
            for index in dicKeys:
                acc_descrip=(journal[index][0])
                acc_descrip_list=acc_descrip.split(' - ')

                acc=int(acc_descrip_list[0])
                desc=acc_descrip_list[1]
                amt=(journal[index][1])
                dc=(journal[index][2])
                jt=(journal[index][4])
                memo=(journal[index][5])
                date=(journal[index][6])
                user=(journal[index][7])
                conn.execute('''INSERT INTO journal (account,description,amount,debit_credit,ref,journaltype,memo,date,user) VALUES(?,?,?,?,?,?,?,?,?)'''\
                         ,(acc,desc,amt,dc,ref,jt,memo,date,user))
             
            conn.execute('''UPDATE backup SET date=?,ref=?,description=?,action=?,status=? WHERE ref=?'''\
                         ,(date,ref,memo,'Update','nobackup',ref))            
            conn.commit()
            conn.close()
            return jsonify({19:'Success',21:'Fail',25:'{}'.format(ref),30:'{}'.format(jt),35:'{}'.format(date)})

        for index in dicKeys:
            acc_descrip=(journal[index][0])
            acc_descrip_list=acc_descrip.split(' - ')

            acc=int(acc_descrip_list[0])
            desc=acc_descrip_list[1]
            amt=(journal[index][1])
            dc=(journal[index][2])
            jt=(journal[index][4])
            memo=(journal[index][5])
            date=(journal[index][6])
            user=(journal[index][7])

            conn.execute('''INSERT INTO journal (account,description,amount,debit_credit,ref,journaltype,memo,date,user) VALUES(?,?,?,?,?,?,?,?,?)'''\
                ,(acc,desc,amt,dc,ref,jt,memo,date,user))
        
        conn.execute('''INSERT INTO backup (date,ref,description,action,status) VALUES(?,?,?,?,?)'''\
                         ,(date,ref,memo,'Insert','nobackup'))

        if request.form.get('payable')=='payable':
            acc_descrip=(journal[index][0])
            acc_descrip_list=acc_descrip.split(' - ')
            acc=int(acc_descrip_list[0])         
            desc=acc_descrip_list[1]
            amt=(journal[index][1])
            dc=(journal[index][2])
        
            jt=(journal[index][4])
            memo=(journal[index][5])
            date=(journal[index][6])
            user=(journal[index][7])
            supplierref=(journal[index][8])
            supplier=(journal[index][9])
            duedate=(journal[index][10])
           
            conn.execute('''INSERT INTO accountpayable (account,description,supplier,amount,ref,payable,amountpaid,date,duedate,status,user) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''\
                ,(acc,desc,supplier,amt,supplierref,ref,0,date,duedate,'Not paid',user))

        if request.form.get('payment')=='payment':
            Payment=journal[index][9]
            for item in Payment:
                amountpaid=Payment[item][0]
                date=Payment[item][1]
                method=Payment[item][2]
                #print(amountpaid,date,method,item)
                try:
                    conn.execute('''UPDATE accountpayable SET amountpaid=amountpaid+?,datepaid=?,method=?,payableref=? WHERE payable=?''',(amountpaid,date,method,ref,item))
                except Exception as e:
                    print(e)

        if request.form.get('invoice')=='invoice':
            data=(journal[index][8])
            rows=sorted(data.keys())
            for row in rows:           
                acc_descrip=(data[row][0])
                acc_descrip_list=acc_descrip.split(' - ')

                acc=int(acc_descrip_list[0])         
                desc=acc_descrip_list[1]
                customerid=(data[row][1])
                customer=(data[row][2])
                address=(data[row][3])
                invoice_no=(data[row][5])
                #invoiceid=(data[row][6])
                date=(data[row][6])
                duedate=(data[row][7])
                salesperson=(data[row][8])
                qty=(data[row][9])
                item=(data[row][10])
                item_desc=(data[row][11])
                unitprice=(data[row][12])
                amnt=(data[row][13])
                status=(data[row][14])
                user=(data[row][16])

                acc_descrip1=(data[row][16])
                acc_descrip_list1=acc_descrip1.split(' - ')

                acc1=int(acc_descrip_list1[0])         
                desc1=acc_descrip_list1[1]

                           
                try:
                    conn.execute('''INSERT INTO invoices (account,description,account1,description1,customerid,customer,address,ref,invoice,date,duedate,salesperson,qty,item,item_desc,unitprice,amount,amountpaid,status,user)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''\
                    ,(acc,desc,acc1,desc1,customerid,customer,address,ref,invoice_no,date,duedate,salesperson,qty,item,item_desc,unitprice,amnt,0,status,user))            
                except Exception as e:
                    print(e)

        if request.form.get('invoicepayment')=='invoicepayment':
            Payment=journal[index][9]
           
            for item in Payment:
                amountpaid=Payment[item][0]
                date=Payment[item][1]
                method=Payment[item][2]
                try:
                    conn.execute('''UPDATE invoices SET amountpaid=amountpaid+?,datepaid=?,method=?,paymentref=? WHERE invoiceid=? ''',(amountpaid,date,method,ref,item))
                except Exception as e:
                    pass
                            
        conn.commit()  
        conn.close()
        return jsonify({19:'Success',21:'Fail',25:'{}'.format(ref),30:'{}'.format(jt),35:'{}'.format(date)})

