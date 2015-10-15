#! /usr/bin/python2
from graph import *
import copy

D = 0.85 # damping factor
def page_rank(filepath):
	graph = Graph(filepath)
	# initial page rank vector:
	pr_dict = dict.fromkeys(graph.get_in_graph().keys())
	for key in pr_dict.keys():
		pr_dict[key] = 1 / float(graph.get_node_num())
	new_pr_dict = copy.copy(pr_dict)
	i = 0
    while i < 10:
		i += 1
		sink_pr = 0
		for page in graph.get_sink_nodes():
			sink_pr += pr_dict[key]
		for p in graph.get_in_graph().keys():
			new_pr_dict[p] = (1 - D)/graph.get_node_num()
			new_pr_dict[p] += D * sink_pr / graph.get_node_num()
			if len(graph.get_out_graph()[q]) > 0:
				for q in graph.get_in_graph()[p]:
					new_pr_dict[p] += D * pr_dict[q] / len(graph.get_out_graph()[q]
		for page in graph.get_in_graph().keys():
			pr_dict[page] = new_pr_dict[page]
	return pr_dict
				
def print_pagerank_vector(pr_dict):
	print("Page rank vector:")
	for page in pr_dict.keys():
		print(str(page) + ": " + str(pr_dict[page]))
	print("Sum of page rank values: " + sum(pr_dict.values()))

if __name__ == '__main__':
	page_rank("graph")
