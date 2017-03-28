import csv
import copy

def find_ordering(order, words):
	
	print order
	#print words
	if len(words) == 0:
		print 'this happened'
		print order
		return order
	this_word = words.pop()
	for i in range(21):
		order_copy = order.copy()
		order_copy[this_word] = i
		#print order_copy
		if check_deps(order):
			print 'pass'
			return find_ordering(order_copy,copy.deepcopy(words))
	




def check_deps(order):
	print order
	works = True
	for dep in attr_dic[attr]:
		if " = " in dep:
			if dep.split(' = ')[0] != dep.split(' = ')[1]:
				works = False
		if ' > ' in dep:
			if dep.split(' > ')[0] <= dep.split(' > ')[1]:
				works = False
		if ' < ' in dep:
			if dep.split(' < ')[0] >= dep.split(' < ')[1]:
				works = False
	#print 'true
	return works

#def check_order(tups,)
with open('submissions.csv','rb') as p:
	with open("attribute_orderings.csv",'rb') as f:
		reader = list(csv.reader(f))
		preader = list(csv.reader(p))





		attr_dic = {}

		for row in reader[1:]:

			dep_dic = {}
			attr_dic[row[0]] = row[1:]
			'''

			for col in row[1:]:
				if '=' in col:
					first = col.split(' = ')[0]
					second = col.split(' = ')[1]
					if dep_dic.has_key(first):
						dep_dic[first][1].append(second)
					else:
						dep_dic[first] = [[],[second],[]]
				if '>' in col:
					first = col.split(' > ')[0]
					second = col.split(' > ')[1]
					if dep_dic.has_key(first):
						dep_dic[first][2].append(second)
					else:
						dep_dic[first]  = [[],[],[second]]
				if '<' in col:
					first = col.split(' < ')[0]
					second = col.split(' < ')[1]
					if dep_dic.has_key(first):
						dep_dic[first][0].append(second)
					else:
						dep_dic[first] = [[second],[],[]]

			ordering = {}

			all_words = attr_dic[row[0]].keys()

			#ordering = find_ordering(ordering,attr_dic[row[0]].keys(),[])
			
			attrs = [row[0] for row in reader]


			'''

		attrs = [row[0] for row in reader[1:]]
		for attr in attrs:
			tups = [row[4:] for row in preader[1:] if row[3] == attr]
			min_problems_deps = []
			min_problem_words =[]
			min_val_dic = {}
			min_row = 0
			count = 0
			order = ''
			for row in tups:
				problem_deps = []
				problem_words = []

				this_works = True
				val_dic = {}
				#print row
				for col in row:
					if col == '':
						break
					val_dic[col.split(" : ")[0]] = col.split(" : ")[1]
				for dep in attr_dic[attr]:
					if ' = ' in dep:
						if val_dic[dep.split(' = ')[0]] != val_dic[dep.split(' = ')[1]]:
							problem_words.append(dep.split(' = ')[0])
							problem_words.append(dep.split(' = ')[1])
							this_works = False
							problem_deps.append(dep)
					if ' < ' in dep:
						if val_dic[dep.split(' < ')[0]] >= val_dic[dep.split(' < ')[1]]:
							problem_words.append(dep.split(' < ')[0])
							problem_words.append(dep.split(' < ')[1])
							this_works = False
							problem_deps.append(dep)
					if ' > ' in dep:
						if val_dic[dep.split(' > ')[0]] <= val_dic[dep.split(' > ')[1]]:
							problem_words.append(dep.split(' > ')[0])
							problem_words.append(dep.split(' > ')[1])
							this_works = False
							problem_deps.append(dep)
				problem_words = list(set(problem_words))
				if len(min_problems_deps) == 0:
					min_problems_deps = problem_deps
					min_row = count
					min_problem_words = problem_words
					min_val_dic = val_dic
				if len(problem_deps) < len(min_problems_deps):
					min_problems_deps = problem_deps
					min_row = count
					min_problem_words = problem_words
					min_val_dic = val_dic

				if this_works:
					print 'this works'
					order = row
				count += 1
			if order == '':
				print 'attr: ' + attr + ' has no valid ordering'
				print min_problems_deps
				for word in min_problem_words:
					min_val_dic.pop(word,None)
				print find_ordering(min_val_dic,min_problem_words)












