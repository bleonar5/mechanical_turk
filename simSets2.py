import csv
from itertools import chain, combinations


basic_adjs = {}



DEBUG = True

def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_subsets(s, k):
    '''
    Yield all subsets of size k from set (or list) s
    s -- a set or list (any iterable will suffice)
    k -- an integer > 0
    '''
    s = list(s)
    n = len(s)
    for k_set in k_subsets_i(n, k):
        yield set([s[i] for i in k_set])

def fleiss_kappa(ratings, n, k):
    '''
    Computes the Fleiss' kappa measure for assessing the reliability of 
    agreement between a fixed number n of raters when assigning categorical
    ratings to a number of items.
    
    Args:
        ratings: a list of (item, category)-ratings
        n: number of raters
        k: number of categories
    Returns:
        the Fleiss' kappa score
    
    See also:
        http://en.wikipedia.org/wiki/Fleiss'_kappa
    '''
    items = set()
    categories = set()
    n_ij = {}
    
    for i, c in ratings:
        items.add(i)
        categories.add(c)
        n_ij[(i,c)] = n_ij.get((i,c), 0) + 1
    
    N = len(items)
    
    p_j = {}
    for c in categories:
        p_j[c] = sum(n_ij.get((i,c), 0) for i in items) / (1.0*n*N)
    
    P_i = {}
    for i in items:
        P_i[i] = (sum(n_ij.get((i,c), 0)**2 for c in categories)-n) / (n*(n-1.0))
    
    P_bar = sum(P_i.itervalues()) / (1.0*N)
    P_e_bar = sum(p_j[c]**2 for c in categories)
    
    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    
    return kappa

def computeKappa(mat):
    """ Computes the Kappa value
        @param n Number of rating per subjects (number of human raters)
        @param mat Matrix[subjects][categories]
        @return The Kappa value """
    n = checkEachLineCount(mat)   # PRE : every line count must be equal to n
    N = len(mat)
    k = len(mat[0])
    
    if DEBUG:
        print n, "raters."
        print N, "subjects."
        print k, "categories."
    
    # Computing p[]
    p = [0.0] * k
    for j in xrange(k):
        p[j] = 0.0
        for i in xrange(N):
            p[j] += mat[i][j]
        p[j] /= N*n
    if DEBUG: print "p =", p
    
    # Computing P[]    
    P = [0.0] * N
    for i in xrange(N):
        P[i] = 0.0
        for j in xrange(k):
            P[i] += mat[i][j] * mat[i][j]
        P[i] = (P[i] - n) / (n * (n - 1))
    if DEBUG: print "P =", P
    
    # Computing Pbar
    Pbar = sum(P) / N
    if DEBUG: print "Pbar =", Pbar
    
    # Computing PbarE
    PbarE = 0.0
    for pj in p:
        PbarE += pj * pj
    if DEBUG: print "PbarE =", PbarE
    
    kappa = (Pbar - PbarE) / (1 - PbarE)
    if DEBUG: print "kappa =", kappa
    
    return kappa

def checkEachLineCount(mat):
    """ Assert that each line has a constant number of ratings
        @param mat The matrix checked
        @return The number of ratings
        @throws AssertionError If lines contain different number of ratings """
    n = sum(mat[0])
    
    #assert all(sum(line) == n for line in mat[1:]), "Line count != %d (n value)." % n
    return n

with open("final_stims.csv",'r') as f:
	stimReader = list(csv.reader(f))
	for row in stimReader:
		basic_adjs['_'.join(row[1].split('_')[:2])] = [adj.split('/')[0] for adj in row[2:] if adj != '']
		#print [adj.split('/')[0] for adj in row[2:] if adj != '']



with open("simsetData.csv",'r') as f:
	with open("kappa_scores.csv",'w') as w:
		with open("submissions.csv",'w') as p:
			pwriter = csv.writer(p)

			sponsReader = list(csv.reader(f))
			pwriter.writerow(['WorkerId','AssignmentId','Approved?','attribute','answer'])
			writer = csv.writer(w)

			input_adjs = {}
			input_rows = {}

			for row in sponsReader[1:]:
				relations = {}
				li = []
				tups = row[4:]
				if row[2] == 'approved':
					if input_adjs.has_key(row[3]):
						input_adjs[row[3]].append(tups)
						input_rows[row[3]].append(row)
					else:
						input_adjs[row[3]] = [tups]
						input_rows[row[3]] = [row]

			attr_list = [(key,input_adjs[key]) for key in input_adjs.keys()] #if len(input_adjs[key]) > 1]

			writer.writerow(['Attribute','Interpretation','Kappa (n=5)','# of submissions','Average # added','Average # removed','shared_adjectives','shared_dependencies'])

			added = []
			removed = []

			for attr_tup in attr_list:
				result = set([adj.split(' : ')[0] for adj in attr_tup[1][0]])
				for s in attr_tup[1][1:]:
					result.intersection_update([adj.split(' : ')[0] for adj in s if adj != ''])

				adj_list = list(result)
				for tup in attr_tup[1]:
					current_adjs = [t.split(' : ')[0] for t in tup]
					current_set = set(current_adjs)
				#print attr_tup
					adjs_set = set(basic_adjs[attr_tup[0]])

					added.append(len(current_set - adjs_set))

					removed.append(len(adjs_set - current_set))
				#print attr_tup[0]
				#print adjs_set -result

				dict_list = []

				for e in attr_tup[1]:
					dic = {}
					for el in e:
						print el
						if ':' in el:
							dic[el.split(' : ')[0]] = int(el.split(' : ')[1])
					dict_list.append(dic)

				similar_count = 0
				total_count = 0

				comp_list = []
				#print adj_list
				mat= [[],[],[]]
				count = 0
				max_fleiss = 0
				indexes = [x for x in xrange(len(dict_list))]
				mat_li = []
				dep_list = []
				shared_deps = []
				max_deps = []
				max_three_set = []
				total_mat_li = []
				'''
				for iAdj in adj_list:
						for jAdj in adj_list[adj_list.index(iAdj) + 1:]:
							comp = ''
							dep_list.append(iAdj + ':' +jAdj)
							for x in xrange(len(dict_list)):
								#print str(dic[iAdj]) + ' ' + str(dic[jAdj])
								if dict_list[x][iAdj] > dict_list[x][jAdj]:
									#mat[x].append(1)
									total_mat_li.append((iAdj + ':' + jAdj,1))
								else:
									if dict_list[x][iAdj] == dict_list[x][jAdj]:
										#mat[x].append(0)
										total_mat_li.append((iAdj + ':' + jAdj,0))
									else:
										#mat[x].append(-1)
										total_mat_li.append((iAdj + ':' + jAdj,-1))
				'''

				for three_set in k_subsets(indexes,5):
					wIDs = [input_rows[attr_tup[0]][index][0] for index in three_set]
					if len(set(wIDs)) != len(wIDs):
						continue

					three_set = list(three_set)
					print adj_list
					if len(adj_list) < 5:
						continue
					for iAdj in adj_list:
						for jAdj in adj_list[adj_list.index(iAdj) + 1:]:
							comp = ''
							
							for x in xrange(5):
								#print str(dic[iAdj]) + ' ' + str(dic[jAdj])
								if dict_list[three_set[x]][iAdj] > dict_list[three_set[x]][jAdj]:
									#mat[x].append(1)
									mat_li.append((iAdj + ':' + jAdj,1))
									dep_list.append(iAdj + ':' +jAdj)
								else:
									if dict_list[three_set[x]][iAdj] == dict_list[three_set[x]][jAdj]:
										#mat[x].append(0)
										mat_li.append((iAdj + ':' + jAdj,0))
										dep_list.append(iAdj + ':' +jAdj)
									else:
										#mat[x].append(-1)
										mat_li.append((jAdj + ':' + iAdj,1))
										dep_list.append(jAdj + ':' +iAdj)
							count += 1
					#print mat_li
					#fleiss = computeKappa(mat)
					for dep in dep_list:
						for x in [-1,0,1]:
							if len([tup for tup in mat_li if tup[0] == dep and tup[1] == x]) >= 3:
								if x== 0:
									sign = ' = '
								if x == 1:
									sign = ' > '
								shared_deps.append(dep.split(':')[0] + sign + dep.split(':')[1])


					try:
						fleiss = fleiss_kappa(mat_li,5,2)
					except:
						fleiss = 0
					try:
						total_fleiss = fleiss_kappa(total_mat_li,len(dict_list),3)
					except:
						total_fleiss = 0
					print 'Fleiss '+ str(fleiss) + ' for:'
					for t in three_set:
						print [(adj,dict_list[t][adj]) for adj in adj_list]
					if fleiss > max_fleiss:
						max_fleiss = fleiss
						max_deps = shared_deps
						max_three_set = three_set
					print mat
					mat = [[],[],[]]
					dep_list = []
					mat_li = []
					shared_deps = []
				for index in max_three_set:
					pwriter.writerow(input_rows[attr_tup[0]][index])

				interpretation = ''
				if max_fleiss >= 0.81:
					interpretation = 'Almost Perfect Agreement'
				if max_fleiss < 0.81 and max_fleiss >= 0.61:
					interpretation = 'Substantial Agreement'
				if max_fleiss < 0.61 and max_fleiss >= 0.41:
					interpretation = 'Moderate Agreement'
				if max_fleiss < 0.41 and max_fleiss >= 0.21:
					interpretation = 'Fair Agreement'
				if max_fleiss <0.21 and max_fleiss >= 0:
					interpretation = 'Slight Agreement'
				if max_fleiss < 0:
					interpretation = 'Poor Agreement'
							
				if len(max_deps) != 0:
					writer.writerow([attr_tup[0],interpretation,max_fleiss,len(dict_list),sum(added)/float(len(added)),sum(removed)/float(len(removed)),list(result)] + comp_list + max_deps)
				added = []
				removed = []

