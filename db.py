import csv
import sqlite3 as sql
from random import randint

with open('final_stims.csv','rb') as f:
	reader = csv.reader(f)
	db = sql.connect('adjs.db')
	cursor = db.cursor()
	#cursor.execute('''
	#	CREATE TABLE adjectives(adj TEXT, adjid TEXT,val INTEGER, def TEXT, attr TEXT, attrdef TEXT)
	#''')

	li = [0,1,19,20]
	
	for row in reader:
		print row
		attr = row[0]
		count = 0
		for col in row[2:]:
			print col
			cursor.execute('''INSERT INTO adjectives(adj,adjid,val,def,attr,attrdef) VALUES(?,?,?,?,?,?)''', (col.split('/')[0],col.split('/')[1],li[count % 4],col.split('/')[2], row[1].split('_')[0] +'_'+ row[1].split('_')[1],row[1].split('_')[2]))
			count += 1
			print attr
	db.commit()
