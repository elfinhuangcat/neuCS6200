#! /usr/bin/python2
import time
"""
What we need to compute the PageRank:
// P is the set of all pages; |P| = N
// S is the set of sink nodes, i.e., pages that have no out links
// M(p) is the set (without duplicates) of pages that link to page p
// L(q) is the number of out-links (without duplicates) from page q
// d is the PageRank damping/teleportation factor; use d = 0.85 as a fairly typical value
"""
class Graph:
    def __init__(self, filepath):
        # init in-link graph:
        self.in_graph = dict()

        input_graph = open(filepath, 'r')
        for line in input_graph:
            arr = line.split(' ')
            arr[-1] = arr[-1][:-1] # Remove the '\n'
            if arr[0] not in self.in_graph:
                self.in_graph[arr[0]] = set(arr[1:]) # to avoid duplicate
            else:
                self.in_graph[arr[0]] = self.in_graph[arr[0]] | set(arr[1:])
            # Check if all pages are already in the dict.keys():
            for page in arr[1:]:
                if page not in self.in_graph.keys():
                    self.in_graph[page] = set()
        input_graph.close()
        print "Finish in_graph construction."
        
        # graph nodes number:
        self.node_num = len(self.in_graph.keys())

        # init sink node set, i.e. pages that have no out links
        # init the number of out-links (without duplicates) from page q
        self.out_count = dict.fromkeys(self.in_graph.keys())
        self.__init_out_count()
        self.sink_node = set()
        self.__init_sink_nodes()
        self.source_node = set()
        self.__init_source_nodes()
        
    def __init_out_count(self):
        """
        Initialize out_count: key is the page P, value is 
        the number of pages that P points to.
        """
        for key in self.out_count:
            self.out_count[key] = set()
        for key in self.in_graph:
            for page in self.in_graph[key]:
                self.out_count[page].add(key)
        for key in self.out_count: # turn it into counts
            self.out_count[key] = len(self.out_count[key])

    def __init_sink_nodes(self):
        for key in self.out_count:
            if self.out_count[key] == 0:
                self.sink_node.add(key)
    
    def __init_source_nodes(self):
        for key in self.in_graph:
            if len(self.in_graph[key]) == 0:
                self.source_node.add(key)

    def print_in_graph(self):
        print("The graph showing incoming links for each page:")
        for key in self.in_graph.keys():
            print str(key) + ":  ",
            for page in self.in_graph[key]:
                print str(page) + ' ',
            print

    def print_graph_info(self):
        print "Num of nodes = " + str(self.node_num)
        self.print_in_graph()
        print "Sink node set: " + str(self.sink_node)
        print "Source node set: " + str(self.source_node)

    def get_node_num(self):
        return self.node_num
    def get_in_graph(self):
        return self.in_graph
    def get_out_count(self):
        return self.out_count
    def get_sink_nodes(self):
        return self.sink_node
    def get_source_nodes(self):
        return self.source_node


if __name__ == '__main__':
    start_time = time.time()
    graph = Graph("graphs/wt2g_inlinks.txt")
    graph.print_graph_info()
    end_time = time.time()
    print "Elapsed time : " + str(end_time - start_time)
