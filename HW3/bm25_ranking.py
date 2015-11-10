#!/usr/bin/env python
import os
import sys
import math
import operator
import indexing

""" output format:
query_id Q0 doc_id rank BM25_score system_name

output to standout
"""

class BM25():
    def __init__(self, index_file, query_file, lim_out):
        """
        @param index_file - path to index file
        @param query_file - path to query_file
        @param lim_out - the maximum number of document results
        """
        self.SYSTEM_NAME = "bm25_rank_system"
        self.K1 = 1.2
        self.B = 0.75
        self.K2 = 100
        self.LIM_OUT = lim_out
        self.indexer = indexing.InvertIndex()
        self.indexer.decode_index_file(index_file)
        self.query = Query(query_file)
        self.AVDL = float(sum(self.indexer.get_dl())) / len(
            self.indexer.get_dl())
    
    def start_ranking(self):
        index = self.indexer.get_index()
        i = 1 # query ID
        for q_dict in self.query.get_queries():
            # this is the for loop to inspect each query
            
            ## result_list: to store the scores and ranks of documents
            ## for this query
            ## Each element is: (doc_id, score)
            result_list = list()
            
            iters = list()
            for term in q_dict:
                # store the iterator for each index[term]
                iters.append(iter(self.indexer.get_index()[term]))
            doc_pairs = list()
            for iterator in iters:
                doc_pairs.append(iterator.next())
            
            while True:
                try:
                    if self.doc_id_equal_in_pairs(doc_pairs):
                        # work on bm25 because a doc containing all
                        # the terms in query is found.
                        result_list.append((
                            doc_pairs[0][0],                # doc id
                            self.bm25(q_dict, doc_pairs)))  # score
                        # all move forward
                        doc_pairs = list()
                        for iterator in iters:
                            doc_pairs.append(iterator.next())
                    else:
                        ind = self.index_of_lowest_id_in_pairs(doc_pairs)
                        doc_pairs[ind] = iters[ind].next()                        
                except StopIteration:
                    break
            # rank the result_list by score and output the top LIM ones
            sorted_list = sorted(result_list, 
                key=operator.itemgetter(1), 
                reverse = True)
            sep = '\t'
            for rank in range (1, self.LIM_OUT + 1):
                if rank > len(sorted_list):
                    break
                print(str(i) + sep + "Q0" + sep +
                    sorted_list[rank-1][0] +        # doc ID
                    sep + str(rank) + sep + 
                    str(sorted_list[rank-1][1]) +   # score
                    sep + self.SYSTEM_NAME)
            i += 1 # update query ID
    
    def bm25(self, q_dict, doc_pairs):
        """
        @param doc_pairs - a list of (doc_id, term frequency)
                           where the doc_id are same
        Returns the document score
        """
        k = self.K1 * ((1 - self.B) + self.B *
            float(self.indexer.get_dl()[int(doc_pairs[0][0])-1]) / 
            self.AVDL)
        score = 0
        i = 0 # index of term
        for term in q_dict:
            ni = len(self.indexer.get_index()[term])
            fi = doc_pairs[i][1]
            qfi = q_dict[term]
            
            add_1 = math.log(self.indexer.get_doc_num() - ni + 0.5)
            add_2 = math.log((self.K1 + 1) * float(fi))
            add_3 = math.log((self.K2 + 1) * float(qfi))
            sub_1 = math.log(ni + 0.5)
            sub_2 = math.log(k + float(fi))
            sub_3 = math.log(self.K2 + float(qfi))

            score += add_1 + add_2 + add_3 - sub_1 - sub_2 - sub_3
            i += 1
        return score
        
    
    def doc_id_equal_in_pairs(self, doc_pairs):
        """
        @param doc_pairs - a list of (doc_id, term frequency)
        """
        doc_id = doc_pairs[0][0]
        for i in range(1, len(doc_pairs)):
            if doc_id != doc_pairs[i][0]:
                return False
        return True
    
    def index_of_lowest_id_in_pairs(self, doc_pairs):
        """
        @param doc_pairs - a list of (doc_id, term frequency)
        """
        lowest_id = doc_pairs[0][0]
        index = 0
        for i in range(1, len(doc_pairs)):
            if int(doc_pairs[i][0]) < int(lowest_id):
                lowest_id = doc_pairs[i][0]
                index = i
        return index
        
    # methods for debugging:
    def print_doc_pairs(self, doc_pairs):
        """
        @param doc_pairs - a list of (doc_id, term frequency)
        """
        print "DOC PAIRS:"
        for pair in doc_pairs:
            print "(" + pair[0] + ", " + str(pair[1]) + ") ",
        print('\n')
        
class Query():
    def __init__(self, query_file):
        """
        self.queries is a LIST of DICTIONARIES.
        Each dict is:
        q_term : q_term_frequency(count)
        """
        if not os.path.isfile(query_file):
            print("ERROR - query file not exist.")
            exit(1)
        self.queries = list()
        i = 0
        with open(query_file, 'r') as f:
            for line in f:
                self.queries.append(dict())
                arr = line[:-1].split(' ') # remove '\n'
                for term in arr:
                    if blank(term):
                        continue
                    if term not in self.queries[i]:
                        self.queries[i][term] = 1
                    else:
                        self.queries[i][term] += 1
                i += 1
    def get_queries(self):
        return self.queries

### utility methods:    
def blank(string):
    if (string == '' or 
        string == ' ' or 
        string == '\n' or
        string == '\t'):
        return True
    else:
        return False
        

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("ERROR - you should invoke the bm25 ranker by: ")
        print("        bm25 index.out queries.txt limit_out")
    ranker = BM25(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    ranker.start_ranking()
        
