from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def ViewBalanceSheet():
    if request.form.get('action')=='fetchbalancesheet':
        date=request.form.get('date1')
        print(date)
        conn = sqlite3.connect('db/admin.db')
        conn.row_factory=sqlite3.Row

        cursor=conn.cursor()
        cursor1 = cursor.execute("SELECT DISTINCT description, account FROM journal WHERE DATE(date) <=?  ORDER BY date",(date,))
        current_account=cursor1.fetchall()
        balanceDic={}
        description_list=[]
        total_debit=total_credit=0
        for row in current_account:
            description_list.append(row['description'])

            cursor=conn.cursor()
            cursor2 = cursor.execute("SELECT * FROM journal WHERE description=? AND DATE(date) <=?  ORDER BY date",(row['description'],date) )
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

        balance=[str(format_currency(total_debit,'NGN', locale='en_US')),str(format_currency(total_credit,'NGN', locale='en_US'))]
        balanceDic['bal']=balance           
        balanceDic['description_list']=description_list

        return jsonify(BalanceSheet(balanceDic))
		
def BalanceSheet(balanceDic):

    conn = sqlite3.connect('db/admin.db')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    description=balanceDic['description_list']
    conn.execute("DELETE FROM trialbalance")

    reportgroupDic={}
    cursor = cursor.execute("SELECT reportgroup, account FROM accountdetails")
    reportgroup=cursor.fetchall()
    for item in reportgroup:
        reportgroupDic[(item['account'])]=item['reportgroup']

    
    for row in description:
        if balanceDic[row][0]=='':
            amt=balanceDic[row][1]
            dc='credit'
        if balanceDic[row][1]=='':
            amt=balanceDic[row][0]
            dc='debit'
        acc=balanceDic[row][2]
        reportgroup=reportgroupDic[acc]
        date= ''       
        conn.execute('''INSERT INTO trialbalance (account,description,amount,debit_credit,reportgroup,date) VALUES(?,?,?,?,?,?)'''\
                    ,(acc,row,amt,dc,reportgroup,date))
    conn.commit()
   
    balSheetDic={}
    #Current Assets     
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',310101, 310201,'credit',310101, 310201)).fetchall():
        CashAndCashEquivalents=(item['amount'])
        balSheetDic['CashAndCashEquivalents']=CashAndCashEquivalents
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',310601 , 310604,'credit',310601 , 310604)).fetchall():
        Receivables=(item['amount'])
        balSheetDic['Receivables']=Receivables
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('debit',310801,'credit',310801)).fetchall():
        Prepayments=(item['amount'])
        balSheetDic['Prepayments']=Prepayments
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?) )  AS amount ''',('debit',310501 , 310502,'credit',310501 , 310502)).fetchall():
        Inventories=(item['amount'])
        balSheetDic['Inventories']=Inventories
    #Non-Current Assets 
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?) )  AS amount ''',('debit',311001 , 311002,'credit',311001 , 311002)).fetchall():
        LongTermLoans=(item['amount'])
        balSheetDic['LongTermLoans']=LongTermLoans
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?) )  AS amount ''',('debit',310901 , 310902,'credit',310901 , 310902)).fetchall():
        Investments=(item['amount'])
        balSheetDic['Investments']=Investments
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',320101 , 320110,'credit',320101 , 320110)).fetchall():
        PropertyPlantEquipment=(item['amount']) 
        balSheetDic['PropertyPlantEquipment']=PropertyPlantEquipment
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('debit',320201,'credit',320201)).fetchall():
        InvestmentProperty=(item['amount'])
        balSheetDic['InvestmentProperty']=InvestmentProperty
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('debit',320301,'credit',320301)).fetchall():
        IntangibleAssets=(item['amount'])
        balSheetDic['IntangibleAssets']=IntangibleAssets
    #Current Liabilities
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',410101,'debit',410101)).fetchall():
        Deposits=(item['amount'])
        balSheetDic['Deposits']=Deposits
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',410201,'debit',410201)).fetchall():
        ShortTermLoansDebts=(item['amount'])
        balSheetDic['ShortTermLoansDebts']=ShortTermLoansDebts
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('credit',410301 , 410302,'debit',410301 , 410302)).fetchall():
        UnremittedDeductions=(item['amount'])
        balSheetDic['UnremittedDeductions']=UnremittedDeductions 
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?) )  AS amount ''',('credit',410401 , 410501,'debit',410401 , 410501)).fetchall():
        Payables=(item['amount'])
        balSheetDic['Payables']=Payables
    ShortTermProvisions='NA'
    balSheetDic['NA']=0
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',410601,'debit',410601)).fetchall():
        CurrentPortionofBorrowings=(item['amount']) 
        balSheetDic['CurrentPortionofBorrowings']=CurrentPortionofBorrowings
    #Non-Current Liabilities    
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?) )  AS amount ''',('credit',420101 , 420102,'debit',420101 , 420102)).fetchall():
        PublicFunds=(item['amount'])
        balSheetDic['PublicFunds']=PublicFunds  
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',420201,'debit',420201)).fetchall():
        LongTermProvisions=(item['amount'])
        balSheetDic['LongTermProvisions']=LongTermProvisions
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',420301,'debit',420301)).fetchall():
        LongTermBorrowing=(item['amount'])
        balSheetDic['LongTermBorrowing']=LongTermBorrowing
    #NET ASSETS/EQUITY  
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',430101,'debit',430101)).fetchall():
        CapitalGrant=(item['amount'])
        balSheetDic['CapitalGrant']=CapitalGrant
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',430301,'debit',430301)).fetchall():
        Reserves=(item['amount'])
        balSheetDic['Reserves']=Reserves
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',430201,'debit',430201)).fetchall():
        AccumulatedSurpluses=(item['amount'])
        balSheetDic['AccumulatedSurpluses']=AccumulatedSurpluses  
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('credit',440101 , 440406,'debit',440101 , 440406)).fetchall():
        ACCUMULATED=(item['amount'])
        balSheetDic['ACCUMULATED']=ACCUMULATED    
    MinorityInterest='NA'
    balSheetDic['NA']=0 
    
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup LIKE ? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup LIKE ?) )  AS amount ''',('credit','1%','debit','1%')).fetchall():
        GrossProfit=(item['amount'])
        
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup LIKE ? )) -
            (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup LIKE ?) )  AS amount ''',('debit','2%','credit','2%')).fetchall():
        Expense=(item['amount'])    
        
        RetainedEarnings=((GrossProfit) - (Expense))
    balSheetDic['RetainedEarnings']=RetainedEarnings  

    return balSheetDic