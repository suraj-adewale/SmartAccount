from flask import Flask,request, jsonify
import threading,json,sqlite3
from babel.numbers import format_currency

def ViewFinPerformance():
    if request.form.get('action')=='fetchfinperformance':
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
   
    FinPerformance={}
    #Current Assets     
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? AND reportgroup=?) )  AS amount ''',('credit',110101, 110103,'debit',110101, 110103)).fetchall():
        StatutoryRevenue=(item['amount'])
        FinPerformance['StatutoryRevenue']=StatutoryRevenue

    for item in cursor.execute('''SELECT (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',110102, 'debit',110102)).fetchall():
        GovernmentShareofVAT=(item['amount'])
        FinPerformance['GovernmentShareofVAT']=GovernmentShareofVAT

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=?) )  AS amount ''',('credit',120101,'debit',120101)).fetchall():
        TaxRevenue=(item['amount'])
        FinPerformance['TaxRevenue']=TaxRevenue

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? OR reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? OR reportgroup=?) )  AS amount ''',('credit',120201 , 120210,120213,'debit',120201 , 120210,120213)).fetchall():
        NonTaxRevenues=(item['amount'])
        FinPerformance['NonTaxRevenues']=NonTaxRevenues
    #Non-Current Assets 
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('credit',120211,'debit',120211)).fetchall():
        InvestmentIncome=(item['amount'])
        FinPerformance['InvestmentIncome']=InvestmentIncome

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('credit',120212,'debit',120212)).fetchall():
        InterestEarned=(item['amount'])
        FinPerformance['InterestEarned']=InterestEarned    

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('credit',130101 , 130204,'debit',130101 , 130204)).fetchall():
        AidGrants=(item['amount'])
        FinPerformance['AidGrants']=AidGrants

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('credit',140401 , 140402,'debit',140401 , 140402)).fetchall():
        DebtForgiveness=(item['amount'])
        FinPerformance['140401 - 140402']=DebtForgiveness 

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('credit',140701,'debit',140701)).fetchall():
        OtherRevenues=(item['amount'])
        FinPerformance['OtherRevenues']=OtherRevenues

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('credit',150101,'debit',150101)).fetchall():
        TransferfromotherGovernmentEntities=(item['amount'])
        FinPerformance['TransferfromotherGovernmentEntities']=TransferfromotherGovernmentEntities           

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',210101 , 210202,'credit',210101, 210202)).fetchall():
        SalariesWages=(item['amount']) 
        FinPerformance['SalariesWages']=SalariesWages

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('debit',210301,'credit',210301)).fetchall():
        SocialBenefits=(item['amount'])
        FinPerformance['SocialBenefits']=SocialBenefits    


    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? OR reportgroup=? OR reportgroup=?) ) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? OR reportgroup=? OR reportgroup=?) )  AS amount ''',('debit',220201, 220208, 220210, 230501,'credit',220201, 220208, 220210, 230501)).fetchall():
        OverheadCost=(item['amount'])
        FinPerformance['OverheadCost']=OverheadCost

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',220401, 220402,'credit',220401, 220402)).fetchall():
        GrantsContributions=(item['amount'])
        FinPerformance['GrantsContributions']=GrantsContributions 

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?))  AS amount ''',('debit',220501, 220502,'credit',220501, 220502)).fetchall():
        Subsidies=(item['amount']) 
        FinPerformance['Subsidies']=Subsidies   


    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',240101, 240201,'credit',240101, 240201)).fetchall():
        DepreciationCharges=(item['amount'])
        FinPerformance['DepreciationCharges']=DepreciationCharges
    #Current Liabilities
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? )) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',260101, 260301,'credit',260101, 260301)).fetchall():
        ImpairmentCharges=(item['amount'])
        FinPerformance['ImpairmentCharges']=ImpairmentCharges

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('debit',250101,'credit',250101)).fetchall():
        AmortizationCharges=(item['amount'])
        FinPerformance['AmortizationCharges']=AmortizationCharges 

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?)) -
        (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup=? OR reportgroup=?))  AS amount ''',('debit',270101, 270102,'credit',270101, 270102)).fetchall():
        BadDebtsCharges=(item['amount']) 
        FinPerformance['BadDebtsCharges']=BadDebtsCharges

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('debit',220209,'credit',220209)).fetchall():
        PublicDebtCharges=(item['amount'])
        FinPerformance['PublicDebtCharges']=PublicDebtCharges

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? )) -
        (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',220701, 220801,'credit',220701, 220801)).fetchall():
        TransfertootherGovernmentEntities=(item['amount'])
        FinPerformance['TransfertootherGovernmentEntities']=TransfertootherGovernmentEntities

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?  OR reportgroup>=? AND reportgroup<=?)) -
        (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? OR reportgroup>=? AND reportgroup<=?) )  AS amount ''',('debit',40501, 140503, 140801, 140901,'credit',40501, 140503, 140801, 140901)).fetchall():
        GainLossonDisposalofAsset1=(item['amount'])
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=?  )) -
        (SELECT total(amount) FROM trialbalance WHERE debit_credit=? AND (reportgroup>=? AND reportgroup<=? ) )  AS amount ''',('debit',280101, 280105,'credit',280101, 280105)).fetchall():
        GainLossonDisposalofAsset2=(item['amount'])     
    GainLossonDisposalofAsset = GainLossonDisposalofAsset1 - GainLossonDisposalofAsset2
    FinPerformance['GainLossonDisposalofAsset'] = GainLossonDisposalofAsset


    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('debit',141001,'credit',141001)).fetchall():
        GainLossonForeignExchangeTransaction1=(item['amount'])
        FinPerformance['141001'] = GainLossonForeignExchangeTransaction1
    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('debit',220901,'credit',220901)).fetchall():
        GainLossonForeignExchangeTransaction2=(item['amount'])  
    GainLossonForeignExchangeTransaction = GainLossonForeignExchangeTransaction1 - GainLossonForeignExchangeTransaction2       
    FinPerformance['GainLossonForeignExchangeTransaction'] = GainLossonForeignExchangeTransaction


    FinPerformance['NA']=''

    for item in cursor.execute('''SELECT (SELECT total(amount)  FROM trialbalance WHERE debit_credit=? AND (reportgroup=?)) -
        (SELECT total(amount)   FROM trialbalance WHERE debit_credit=? AND (reportgroup=? ) )  AS amount ''',('debit',140601,'credit',140601)).fetchall():
        MinorityInterestShare=(item['amount'])
        FinPerformance['MinorityInterestShare']=MinorityInterestShare


    return FinPerformance