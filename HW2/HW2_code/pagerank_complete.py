#! /usr/bin/python2
from graph_mod import *
import copy
import math
import time
D = 0.85 # Damping factor
PERP_COMPARE = 4 # How many records of perplexity are to be compared

class PageRank:
    def __init__(self, filepath):
        # the Graph:
        self.graph = Graph(filepath)
        # the PageRank vector:
        self.pr_dict = dict.fromkeys(self.graph.get_in_graph())
        for key in self.pr_dict: # uniform value
            self.pr_dict[key] = 1 / float(self.graph.get_node_num())
        # perplexity history list:
        self.perp_hist = list()
        # compute the first perplexity:
        self.perp_hist.append(perplexity(self.pr_dict.values()))
        
    def get_graph(self):
        return self.graph
    def get_pr_dict(self):
        return self.pr_dict
    def get_perp_hist(self):
        return self.perp_hist
    
    def page_rank(self):
        new_pr_dict = copy.copy(self.pr_dict)
        while not self.converge():
            sink_pr = 0
            for page in self.graph.get_sink_nodes():
                sink_pr += self.pr_dict[key]
            for p in self.graph.get_in_graph():
                new_pr_dict[p] = (1 - D) / self.graph.get_node_num()
                new_pr_dict[p] += D * sink_pr / self.graph.get_node_num()
                for q in self.graph.get_in_graph()[p]:
                    if self.graph.get_out_count()[q] > 0:
                        new_pr_dict[p] += (D * self.pr_dict[q]
                            / self.graph.get_out_count()[q])
            for page in self.graph.get_in_graph():
                self.pr_dict[page] = new_pr_dict[page]
            # compute perplexity:
            self.perp_hist.append(perplexity(self.pr_dict.values()))
    
    def converge(self):
        """ Returns True if it converges. Otherwise False."""
        if len(self.perp_hist) < PERP_COMPARE:
            return False
        else:
            diff_list = list()
            for i in range(0, PERP_COMPARE-1):
                diff_list.append(abs(self.perp_hist[-1-i] 
                                     - self.perp_hist[-2-i]))
            print str(diff_list)
            return all_below(diff_list, 1)
    
    def print_pagerank_vector(self):
        print("Page rank vector:")
        for key in self.pr_dict:
            print(str(key) + ": " + str(self.pr_dict))
        print("Sum of pagerank values: " 
              + str(sum(self.pr_dict.values())))
            
### END OF CLASS PAGERANK

def perplexity(prob_list):
    exp = 0
    for prob in prob_list:
        exp += prob *  math.log(prob, 2)
    return (2 ** (-exp))

def all_below(value_list, below_num):
    """
    value_list: a list of values
    below_num: the list of values are required to be less than this num
    Returns True if all these values are less than below_num
    """
    for value in value_list:
        if value >= below_num:
            return False
    return True

if __name__ == '__main__':
    start_time = time.time()
    pg = PageRank("graphs/wt2g_inlinks.txt")
    pg.page_rank()
    pg.print_pagerank_vector()
    print("Iterations: " + str(len(pg.get_perp_hist())))
    end_time = time.time()
    print("Time in seconds: " + str(end_time - start_time))
