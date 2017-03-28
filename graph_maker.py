import matplotlib.pyplot as plt 
import pygraphviz as pgv
import networkx as nx 
from networkx import *
import csv
from itertools import chain, combinations
from networkx.drawing.nx_agraph import graphviz_layout

def find_all_equal(node):
	#collects a set of all words that are explicitly and implicitly equal to the given word
	equal = set([node])
	for x in range(len(deps)):
		for dep in deps:
			if '=' in dep:
				left = dep.split(' = ')[0]
				right = dep.split(' = ')[1]
				if left in list(equal) or right in list(equal):
					#print left
					#print right
					equal.add(left)
					equal.add(right)
				#print '---'
	#print equal
	return equal

def create_graph (attr,edges):
	G = nx.DiGraph()
	#G = nx.to_agraph(G)pgv
	G.add_edges_from(edges)
	edges_list = list(G.edges_iter())
	#Remove all redundant edges
	for edge in edges_list:
		if (edge[0],edge[1],{'weight':1}) in edges:
			#print 'pass'
			pass
		#print edge
		G.remove_edge(*edge)
		if nx.has_path(G,edge[0],edge[1]):
			continue
		else:
			G.add_edge(edge[0],edge[1],{'weight':0})


	for cycle in nx.simple_cycles(G):
		if G.has_edge(cycle[-2],cycle[-1]):
			G.remove_edge(cycle[-2],cycle[-1])

	Graph = pgv.AGraph(directed=True)
	for edge in G.edges_iter():
		#print edge
		Graph.add_edge(edge[0],edge[1])
	Graph.write('graphs_with_eqs/dots/' +attr+'.dot')
	Graph.layout(prog='dot')
	#print Graph=
	Graph.draw('graphs_with_eqs/pngs/'+attr+'.png')
	#plt.show()


with open('kappa_scores.csv','rb') as f:
	reader = list(csv.reader(f))

	for row in reader[1:]:
		print row
		edges = []
		edge = ()
		deps = row[6:]

		#For each '>' dependency, find the maximal set of adjectives where every adjective included is equal to another in the set
		for dep in deps:
			if '>' in dep:
				node_set = sorted(find_all_equal(dep.split(' > ')[0]))

				other_node_set = sorted(find_all_equal(dep.split(' > ')[1]))

				if (str(other_node_set),str(node_set),{'weight':0}) not in edges:
					edges.append((str(node_set),str(other_node_set),{'weight':0}))
				else:
					left_count = 0
					right_count = 0
					for adj in list(node_set):
						for other_adj in list(other_node_set):
							if adj + ' > ' + other_adj in deps:
								left_count += 1

					for adj in list(other_node_set):
						for other_adj in list(node_set):
							if adj + ' > ' + other_adj in deps:
								right_count += 1

					if left_count >= right_count:
						edges.append((str(node_set),str(other_node_set),{'weight':0}))
					else:
						edges.append((str(other_node_set),str(node_set),{'weight':0}))
		#edges_dic[row[0].split('_')[0]] = edges
		create_graph(row[0].split('_')[0],edges)

			#edges.append(edge)
			#eq_edges.append(eq_edge)
			#print edges


	'''
	for dep in deps:
		if '=' in dep:
			if dep.split(' = ')[0] == node:
				left = dep.split(' = ')[0]
				right = dep.split(' = ')[1]
				equal.add(right)
				eq_deps =[d for d in deps if '=' in d]
				other_eqs = [d for d in eq_deps if (d.split(' = ')[0] == right and d.split(' = ')[1] not in list(equal)) or (d.split(' = ')[0] not in list(equal) and d.split(' = ')[1] == right)]
				if len(other_eqs) != 0:
					equal = equal + find_all_equal(dep.split(' = ')[1])
					
				#for more_dep in deps:
					
					if '=' in more_dep:
						if more_dep.split(' = ')[0] == dep.split(' = ')[1] and more_dep.split(' = ')[1] != dep.split(' = ')[0]:
							equal.add(more_dep.split(' = ')[1])
						if more_dep.split(' = ')[1] == dep.split(' = ')[1] and more_dep.split(' = ')[0] != dep.split(' = ')[0]:
							equal.add(more_dep.split(' = ')[0])
				
			if dep.split(' = ')[1] == node:
				left = dep.split(' = ')[0]
				right = dep.split(' = ')[1]
				equal.add(dep.split(' = ')[0])
				eq_deps =[d for d in deps if '=' in d]
				other_eqs = [d for d in eq_deps if (d.split(' = ')[0] == left and d.split(' = ')[1] not in list(equal)) or (d.split(' = ')[0] not in list(equal) and d.split(' = ')[1] == left)]
				if len(other_eqs) != 0:
					equal = equal + find_all_equal(dep.split(' = ')[0])
				
				for more_dep in deps:
					if '=' in more_dep:
						if more_dep.split(' = ')[0] == dep.split(' = ')[0] and more_dep.split(' = ')[1] != dep.split(' = ')[1]:
							equal.add(more_dep.split(' = ')[1])
						if more_dep.split(' = ')[1] == dep.split(' = ')[0] and more_dep.split(' = ')[0] != dep.split(' = ')[1]:
							equal.add(more_dep.split(' = ')[0])
				
	'''







