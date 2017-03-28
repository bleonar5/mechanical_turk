with open('stimuli.csv','w') as f:
	writer = csv.writer(f)

	for atr in attributes:
		li = [atr.name()]
		for syn in attributes[atr]:
			li.append(syn.lemmas()[0].name() + '/' + syn.lemmas()[0].key())
			
		writer.writerow(li)

	for row in reader:
		attr = row[0]
		for col in row[1:]:
			cursor.execute('''INSERT INTO adjectives(id,adj,val,attr) VALUES(?,?,?,?)''', (col.split('/')[1],col.split('/')[0],randint(0,10),attr))
			print attr
