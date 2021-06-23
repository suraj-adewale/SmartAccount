from flask import Flask,request
import threading
from server.addaccount import AddAccount
from server.addsupplier import AddSupplier
from server.addcustomer import AddCustomer
from server.required import RequiredData
from server.postjournal import PostJournal
from server.viewjournal import ViewJournal
from server.fetchledger import ViewLedger
from server.trialbalance import ViewTrialbalance
from server.balancesheet import ViewBalanceSheet
from server.performance import ViewFinPerformance
from server.invoices import InvoiveReport
from server.invoicepayment import InvoivePaymentReport
from server.balance import Balance
from server.backup import BackUp
from server.accountpayble import ViewPayable
from server.incomestatement import IncomeStatement
from server.enquiry import ViewAccountEnquiry

from gevent import monkey,pywsgi
monkey.patch_all()

app= Flask(__name__)

@app.route("/addaccount",methods=["GET","POST"])

def createaccount():
    if request.method=="POST":
        return AddAccount()

@app.route("/addsupplier",methods=["GET","POST"])

def addsupplier():
    if request.method=="POST":
        return AddSupplier() 

@app.route("/addcustomer",methods=["GET","POST"])

def addcustomer():
    if request.method=="POST":
        return AddCustomer()                

@app.route("/requireddata",methods=["GET","POST"])

def required():
    if request.method=="POST":
        return RequiredData()
@app.route("/incomestatement",methods=["GET","POST"])
def income():
    if request.method=="POST":
        return IncomeStatement()           

@app.route("/journal",methods=["GET","POST"])

def postjournal():
    if request.method=="POST":
        return PostJournal()     

@app.route("/fetchjournal",methods=["GET","POST"])

def viewjournal():
    if request.method=="POST":
        return ViewJournal()

@app.route("/fetchledger",methods=["GET","POST"])

def fetchledger():
    if request.method=="POST":
        return ViewLedger()

@app.route("/trialbalance",methods=["GET","POST"])

def trialbalance():
    if request.method=="POST":
        return ViewTrialbalance()

@app.route("/fetchbackup",methods=["GET","POST"])

def backup():
    if request.method=="POST":
        return BackUp()         

@app.route("/balancesheet",methods=["GET","POST"])

def balancesheet():
    if request.method=="POST":
        return ViewBalanceSheet()

@app.route("/finperformance",methods=["GET","POST"])

def finperformance():
    if request.method=="POST":
        return ViewFinPerformance()        

@app.route("/invoices",methods=["GET","POST"])

def invoice():
    if request.method=="POST":
        return InvoiveReport()

@app.route("/invoicepayment",methods=["GET","POST"])

def invoicepayment():
    if request.method=="POST":
        return InvoivePaymentReport()

@app.route("/balance",methods=["GET","POST"])

def balance():
    if request.method=="POST":
        return Balance()

@app.route("/accountspayable",methods=["GET","POST"])

def payable():
    if request.method=="POST":
        return ViewPayable() 

@app.route("/accountsenquiry",methods=["GET","POST"])

def enquiry():
    if request.method=="POST":
        return ViewAccountEnquiry()                                                                  

      


def StartServer():
    
    try:
        http = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        thread=threading.Thread(target=http.serve_forever)
        thread.start()
    except Exception as e:
        print(e)
    
#StartServer()    
    
    


 

'''
from gevent import monkey
monkey.patch_all()
from flask import Flask
from gevent import wsgi

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World'

server = wsgi.WSGIServer(('127.0.0.1', 5000), app)
server.serve_forever()

'''     