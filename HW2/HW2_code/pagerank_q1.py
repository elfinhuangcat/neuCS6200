#! /usr/bin/python2

from graph_mod import *
import copy

D = 0.85
OUTPUT_DIR = "outputs/"


def page_rank(filepath, iteration):
    graph = Graph(filepath)
    #initial page rank vector:
    pr_dict = dict.fromkeys(graph.get_in_graph())
    for key in pr_dict:
        pr_dict[key] = 1 / float(graph.get_node_num())
    new_pr_dict = copy.copy(pr_dict)
    i = 0
    
    while i < iteration:
        i += 1
        sink_pr = 0
        for page in graph.get_sink_nodes():
            sink_pr += pr_dict[page]
        for p in graph.get_in_graph():
            new_pr_dict[p] = (1 - D)/graph.get_node_num()
            new_pr_dict[p] += D * sink_pr / graph.get_node_num()
            for q in graph.get_in_graph()[p]:
                if graph.get_out_count()[q] > 0:
                    new_pr_dict[p] += (D * pr_dict[q] 
                                       / graph.get_out_count()[q])
        for page in graph.get_in_graph():
            pr_dict[page] = new_pr_dict[page]
    return pr_dict
    
def print_pagerank_vector(pr_dict):
    print("Page rank vector:")
    for page in pr_dict:
        print(str(page) + ": " + str(pr_dict[page]))
    print("Sum of page rank values: " + str(sum(pr_dict.values())))
    
def output_pagerank_vector(pr_dict, filename):
    log = open((OUTPUT_DIR + filename), 'w')
    for key in pr_dict.keys():
        log.write(key + " " + str(pr_dict[key]) + "\n")
    log.close()

if __name__ == "__main__":
    print("1 iteration:")
    pr_dict = page_rank("graphs/six_node_graph", 1)
    print_pagerank_vector(pr_dict)
    output_pagerank_vector(pr_dict, "q1_1_iteration")
    
    print("\n10 iterations:")
    pr_dict = page_rank("graphs/six_node_graph", 10)
    print_pagerank_vector(pr_dict)
    output_pagerank_vector(pr_dict, "q1_10_iteration")
    
    print("\n100 iterations:")
    pr_dict = page_rank("graphs/six_node_graph", 100)
    print_pagerank_vector(pr_dict)
    output_pagerank_vector(pr_dict, "q1_100_iteration")
