"""import json,sqlite3,base64

conn = sqlite3.connect('db/admin.db')
		
Dic={}
conn.row_factory=sqlite3.Row

cursor=conn.cursor()
cursor=cursor.execute('''SELECT DISTINCT ref,date,memo FROM journal ''')
result=cursor.fetchall()


for row in result:
	 conn.execute('''INSERT INTO backup (date,ref,description,action,status) VALUES(?,?,?,?,?)'''\
                         ,(row['date'],row['ref'],row['memo'],'Insert','nobackup'))

conn.commit()

"""