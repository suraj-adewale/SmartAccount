from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QHBoxLayout,QMessageBox,QLabel,QGridLayout,QApplication,QPushButton,QTableWidget,QWidget,QVBoxLayout,QAbstractItemView
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import pyqtSlot,Qt
from loader import overlay
from functools import partial
import sys,json,base64

class BackUp(QMainWindow):
	def __init__(self, parent=None):
		super(BackUp, self).__init__(parent)

		self.title = 'Back Up'
		self.left = 350
		self.top = 150
		self.width = 700
		self.height = 400
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.Content()
		self.setCentralWidget(self.widget)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
		
	def Content(self):
		usertype=json.load(open("db/usertype.json", "r"))
		if usertype=='Administrator':
			self.ip='localhost'	
		if usertype=='User':
			self.ip=json.load(open("db/ipaddress.json", "r"))
		
		self.refs=[]
		self.indicator=''
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.mainlayout.setContentsMargins(2,20,20,0)
		self.widget.setLayout(self.mainlayout)
		self.table =QTableWidget()
		self.overlay = overlay(self.table)
		self.ConnectServer("http://{}:5000/fetchbackup".format(self.ip),'ref','backupref')	
	
	def BackupList(self):
		Header=['Date','Ref','Description','Action']
		layout=QGridLayout()

		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = self.table.horizontalHeader()
		self.table.setColumnCount(4)

		header.setSectionResizeMode(0, 1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(1, 1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3,  1*(QtWidgets.QHeaderView.Stretch)//2)

		self.mainlayout.addWidget(self.table,10)
		self.mainlayout.addLayout(layout,1)
		self.table.resizeRowsToContents()
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(Header)		

		self.backupAll=QPushButton('Backup Data Now')
		self.backupAll.clicked.connect(partial(self.BackUpNow,self.refs,'backupdataall'))
		self.backupAll.setStyleSheet('font-weight: bold;font-size:14px; min-width: 140px;height:40px; margin:2px;border-radius: 6px;color: green;border:none;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
							 stop: 0 #f6f7fa, stop: 1 #00c6ff);')
		layout.setColumnStretch(0, 1)
		layout.addWidget(self.backupAll,0,1)

	def BackUpNow(self,ref,backup):
		self.ref1=ref
		self.ConnectServer("http://{}:5000/fetchbackup".format(self.ip),ref,backup)		

	def ConnectServer(self,url,ref,option):
		self.overlay.setVisible(True)
		data = QtCore.QByteArray()
		data.append("action=fetchbackup&")
		data.append("ref={}&".format(ref))
		data.append("option={}&".format(option))
		url = url

		self.req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		self.req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse)
		self.nam.post(self.req, data)

	#@pyqtSlot(bytes)
	def handleResponse(self, reply):
		er = reply.error()	
		if er == QtNetwork.QNetworkReply.NoError:
			bytes_string = reply.readAll()
			data = json.loads(str(bytes_string, 'utf-8'))
								
			if data['key']=='online_response':
				if type(self.ref1)!=list:# isinstance(self.ref1, list):
					self.ref1=[self.ref1]
					#print(data,self.ref1)
					self.ConnectServer("http://{}:5000/fetchbackup".format(self.ip),self.ref1,'online_response')
			
			if data['key']=='backupdata':
				postDic=json.dumps(data['data'])
				postDic=base64.b64encode(postDic.encode())
				self.ConnectServer('http://www.sadeltech.com.ng/smartaccount/backup.php',postDic.decode("utf-8"),'online')
				 
			if data['key']=='backupdataall':
				postDic=json.dumps(data['data'])
				postDic=base64.b64encode(postDic.encode())
				self.ConnectServer('http://www.sadeltech.com.ng/smartaccount/backup.php',postDic.decode("utf-8"),'online')
			
			if data['key']=='backupref' and len(data['data'])>0:
				data=data['data']
				rowNumber=len(data)
					
				self.BackupList()	
				self.table.setRowCount(rowNumber) 		
				for row in sorted(data):
					for col in range(4):
						if col==3:
							self.refs.append(data[row][1])
							self.btn=QPushButton(data[(row)][col])
							self.btn.setStyleSheet('font-weight: bold;margin:2px 12px;border-radius: 6px;border:none;font-size:15px;')
							#self.btn.clicked.connect(partial(self.BackUpNow, data[row][1],'backupdata'))
							self.table.setCellWidget(int(row),col, self.btn)
						else:
							item=QTableWidgetItem(data[row][col])
							self.table.setItem(int(row),col, item)
				
			else:
				pass

			self.overlay.setVisible(False)	
		else:
			self.overlay.setVisible(False)
			QMessageBox.critical(self, 'Connection Error ', "\n  Please check your internet connection	\n  ")
			return 'server_error'				
	

	def resizeEvent(self,event):
		self.overlay.resize(event.size())
		event.accept()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = BackUp()
	ex.show()
	sys.exit(app.exec_())
