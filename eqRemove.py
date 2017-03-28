import csv

with open('impossible_dependencies2.csv','rb') as f:
	with open('kappa_scores_updated.csv','rb') as p:
		with open('kappa_scores.csv','w') as w:
			impReader = list(csv.reader(f))
			reader = list(csv.reader(p))
			writer = csv.writer(w)
			writer.writerow(reader[0])

			count = 1
			for row in reader[1:]:
				row_start = row[:5]
				deps = [col for col in row[5:] if col != '']
				bad_deps = [col for col in impReader[count] if col != '']
				for dep in bad_deps:
					print dep
					if dep in deps:
						deps.remove(dep)
				new_row = row_start + deps
				writer.writerow(new_row)
				count += 1

