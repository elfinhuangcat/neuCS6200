#! /usr/bin/python2
from graph import *

def page_rank(filepath):
    graph = Graph(filepath)
    
    # initial page rank vector:
    pr_vec = [1 / float(graph.node_num)]
    
    while not is_converge(pr_vec, prev_pr_vec):

    




if __name__ == '__main__':
    page_rank("graph")
