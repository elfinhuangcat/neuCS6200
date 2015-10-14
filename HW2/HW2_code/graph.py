#! /usr/bin/python2
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
        # init graph
        self.in_graph = dict()
        self.node_num = 0

        input_graph = open(filepath, 'r')
        for line in input_graph:
            self.node_num += 1
            arr = line.split(' ')
            arr[-1] = arr[-1][:-1] # Remove the '\n'
            if arr[0] not in self.in_graph.keys():
                self.in_graph[arr[0]] = set(arr[1:]) # to avoid duplicate
            else:
                self.in_graph[arr[0]] = self.in_graph[arr[0]] | set(arr[1:]) #union
        input_graph.close()

        # init sink node set, i.e. pages that have no out links
        # init the number of out-links (without duplicates) from page q
        self.out_graph = dict.fromkeys(self.in_graph.keys())
        self.__init_out_graph()
        self.sink_node = set()
        self.__init_sink_nodes()
        
    def __init_out_graph(self):
        """
        Initialize out_graph: key is the page P, values are
        the pages that P points to.
        """
        for key in self.out_graph.keys():
            self.out_graph[key] = set()
        for key in self.in_graph.keys():
            for page in self.in_graph[key]:
                self.out_graph[page].add(key)

    def __init_sink_nodes(self):
        for key in self.out_graph.keys():
            if len(self.out_graph[key]) == 0:
                self.sink_node.add(key)

    def print_graph(self,choice):
        """ Choice = 0: print in graph; Choice = 1: print out graph"""
        if choice == 0:
            print("The graph showing incoming links for each page:")
            for key in self.in_graph.keys():
                print str(key) + ":  ",
                for page in self.in_graph[key]:
                    print str(page) + ' ',
                print
        else:
            print("The graph showing outgoing links for each page:")
            for key in self.out_graph.keys():
                print str(key) + ":  ",
                for page in self.out_graph[key]:
                    print str(page) + ' ',
                print

    def print_graph_info(self):
        print "Num of nodes = " + str(self.node_num)
        self.print_graph(0)
        self.print_graph(1)
        print "Sink node set: " + str(self.sink_node)


if __name__ == '__main__':
    graph = Graph("graph")
    graph.print_graph_info()
