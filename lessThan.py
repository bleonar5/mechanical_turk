import csv

'''
with open('kappa_scores.csv','rb') as f:
	with open('kappa_scores_updated.csv','w') as p:
		reader = list(csv.reader(f))
		writer = csv.writer(p)

		writer.writerow(reader[0])

		for row in reader[1:]:
			deps = row[6:]
			new_deps = []

			for dep in deps:
				if '=' in dep or '>' in dep:
					new_deps.append(dep)
				if '<' in dep:
					new_dep = dep.split(' < ')[1] + ' > ' + dep.split(' < ')[0]
					new_deps.append(new_dep)
			writer.writerow(row[:6] + new_deps)
'''
with open('impossible_dependencies2.csv','w') as p:
	with open('kappa_scores.csv','rb') as f:
		#writer = csv.writer(p)
		#writer.writerow(['attribute','kappa score','number of adjectives','number of impossible dependencies','problem_dependencies'])
		#imp_reader = list(csv.reader(p))
		deps_list= []
		reader = list(csv.reader(f))
		count = 1
		for row in reader[1:]:
			print '----'
			deps = row[6:]
			count +=1
			old_deps = list(deps)
			words = row[5].translate(None,'\'')[1:-1].split(', ')
			#print words
			#this_deps = deps[:]
			problem_deps = []

			for word in words:
				#print word
				eqs = [dep.split(' = ')[1] for dep in deps if '=' in dep and dep.split(' = ')[0] == word]
				#print eqs
				for eq in eqs:
					if eq == word:
						continue
					this_deps = deps[:]
					for dep in this_deps:
						which = 0
						if '=' in dep:
							if dep.split(' = ')[0] == dep.split(' = ')[1]:
								#print dep
								#print 'IT HAPPENS HERE'
								continue
							#print word

							if word == dep.split(' = ')[0] and word != dep.split(' = ')[1]:
								#print 'YESYESYES'
								new_dep = eq + ' = ' + dep.split(' = ')[1]
								#opp_new_dep = dep.split(' = ')[1] + ' = ' + eq
								if new_dep not in deps and new_dep.split(' = ')[0] != new_dep.split(' = ')[1]:
									deps.append(new_dep)
									print '---'
									print dep
									print new_dep
									print '---'
									#problem_deps.append(dep)
							if dep.split(' = ')[1] == word and word != dep.split(' = ')[0]:
								#print 'YESYESYES'
								new_dep = dep.split(' = ')[0] + ' = ' + eq
								#opp_new_dep = eq + ' = ' + dep.split(' = ')[0]
								if new_dep not in deps and new_dep.split(' = ')[0] != new_dep.split(' = ')[1]:
									deps.append(new_dep)
									print '---'
									print dep
									print new_dep
									print '---'
									#problem_deps.append(dep)
						if '>' in dep:
							if dep.split(' > ')[0] == word:
								#print 'YESYESYES'
								new_dep = eq + ' > ' + dep.split(' > ')[1]
								if new_dep not in deps:
									#deps.append(new_dep)
									print '---'
									print dep
									print new_dep
									print '---'
									if new_dep.split(' > ')[0] == new_dep.split(' > ')[1]:
										if eq + ' = ' + word not in problem_deps:
											problem_deps.append(word + ' = ' + eq)
									else:
										deps.append(new_dep)
							if dep.split(' > ')[1] == word:
								#print 'YESYESYES'
								new_dep = dep.split(' > ')[0] + ' > ' + eq
								if new_dep not in deps:
									#deps.append(new_dep)
									print '---'
									print dep
									print new_dep
									print '---'
									if new_dep.split(' > ')[0] == new_dep.split(' > ')[1]:
										if eq + ' = ' + word not in problem_deps:
											problem_deps.append(word + ' = ' + eq)
									else:
										deps.append(new_dep)
			impossible_deps = []
			for dep in deps:
				if '>' in dep:
					if dep.split(' > ')[0] == dep.split(' > ')[1]:
						print dep + " IMPOSSIBLE"
						impossible_deps.append(dep)
			print set(deps) - set(old_deps)
			deps_list.append(deps)

			#print '----'

			#writer.writerow(problem_deps)
			#writer.writerow([row[0],row[2],len(words),len(impossible_deps)] + list(set(problem_deps)))


			for iWord in row[5]:
				for jWord in row[5]:

					if iWord + ' = ' + jWord in row[6:] and iWord + ' > ' + jWord in deps:
						print iWord + ' and ' + jWord + ' incompatible'

with open('kappa_scores.csv','w') as f:
	writer = csv.writer(f)
	writer.writerow(reader[0])
	for i in range(len(reader[1:])):
		writer.writerow(reader[i][:5] + list(set(deps_list[i]) + set(reader[i][6:])))

