#! /usr/bin/python2
from graph_mod import *
import copy
import math
import time
import os
import operator
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
                sink_pr += self.pr_dict[page]
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
            print "Perp Change: " + str(diff_list)
            return all_below(diff_list, 1)
    
    def print_pagerank_vector(self):
        print("Page rank vector:")
        for key in self.pr_dict:
            print(str(key) + ": " + str(self.pr_dict))
        print("Sum of pagerank values: " 
              + str(sum(self.pr_dict.values())))
              
    def output_perplexity(self, filepath):
        perp_file = open(filepath, 'w')
        for perp in self.perp_hist:
            perp_file.write(str(perp) + "\n")
        perp_file.close()
        
    def output_top_50_pagerank(self, filepath):
        # sort the pages according to page rank
        sorted_pr = sorted(self.pr_dict.items(), 
                           key = operator.itemgetter(1), reverse = True)
        pg_file = open(filepath, 'w')
        """
        for pair in sorted_pr:
             pg_file.write(str(pair[0]) + "\t" + 
                           str(pair[1]) + "\n")
        """
        for i in range(0,50):
            pg_file.write(str(sorted_pr[i][0]) + "\t" + 
                          str(sorted_pr[i][1]) + "\n")

        pg_file.close()
    
    def output_top_50_inlink(self, filepath):
        # count inlinks:
        inlink_dict = dict.fromkeys(self.graph.get_in_graph())
        for key in self.graph.get_in_graph():
            inlink_dict[key] = len(self.graph.get_in_graph()[key])
        sorted_inlink = sorted(inlink_dict.items(), 
                               key = operator.itemgetter(1), 
                               reverse = True)
        del inlink_dict
        inlink_file = open(filepath, 'w')
        for i in range(0,50):
            inlink_file.write(str(sorted_inlink[i][0]) + "\t" +
                              str(sorted_inlink[i][1]) + "\n")
        inlink_file.close()
        
    def output_info(self, filepath):
        # proportion of pages with no inlinks:
        no_inlink = 0
        for page in self.graph.get_in_graph():
            if len(self.graph.get_in_graph()[page]) == 0:
                no_inlink += 1
        
        # proportion of pages with no outlinks:
        no_outlink = 0
        for page in self.graph.get_out_count():
            if self.graph.get_out_count()[page] == 0:
                no_outlink += 1
        
        # the proportion of pages whose PageRank is less than 
        # their initial, uniform values.
        init_pr = 1 / float(self.graph.get_node_num())
        less_than_unif = 0
        for page in self.pr_dict:
            if self.pr_dict[page] < init_pr:
                less_than_unif += 1
        
        # output:
        info_file = open(filepath, 'w')
        node_num = self.graph.get_node_num()
        info_file.write("Proportion of pages with no in-links: " +
                        str(float(no_inlink) / node_num) + '\n')
        info_file.write("Proportion of pages with no out-links: " +
                        str(float(no_outlink) / node_num) + '\n')
        info_file.write("The proportion of pages whose PageRank " +
                        "is less than their initial, uniform " + 
                        "values: " +
                        str(float(less_than_unif) / node_num) + '\n')
        info_file.close()

    def output_all_results(self):
        outputs_dir = "outputs/q2/"
        if not os.path.exists(outputs_dir):
            os.makedirs(outputs_dir)
        self.output_perplexity(outputs_dir + "perplexity")
        self.output_top_50_pagerank(outputs_dir + "top50_pagerank")
        self.output_top_50_inlink(outputs_dir + "top50_inlink")
        self.output_info(outputs_dir + "info")
            
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
    filepath = raw_input("Please enter the path to the graph file, " + 
                         "e.g. graphs/graph:")
    
    start_time = time.time()
    pg = PageRank(filepath)
    pg.page_rank()
    pg.output_all_results()
    print("Iterations: " + str(len(pg.get_perp_hist())))
    end_time = time.time()
    print("Time in seconds: " + str(end_time - start_time))
