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
            
            ## result_list: to store the scores of documents
            ## for this query
            ## Each element is: (doc_id, score)
            result_list = list()
            for ctr in range(0, len(self.indexer.get_doc_id())):
                # init the score as 0
                result_list.append((self.indexer.get_doc_id()[ctr], 0))
            
            for term in q_dict:
                for doc_pair in self.indexer.get_index()[term]:
                    score_part = self.bm25(q_dict, doc_pair, term)
                    result_list[int(doc_pair[0])-1] = (
                        doc_pair[0],
                        result_list[int(doc_pair[0])-1][1] + score_part)
                    
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
    
    def bm25(self, q_dict, doc_pair, term):
        """
        @param q_dict - {term : qf}
        @param doc_pair - (doc_id, f)
        @param term
        Returns the document score (part)
        """
        k = self.K1 * ((1 - self.B) + self.B *
            float(self.indexer.get_dl()[int(doc_pair[0])-1]) / 
            self.AVDL)
        ni = len(self.indexer.get_index()[term])
        fi = doc_pair[1]
        qfi = q_dict[term]
        
        term_1 = math.log((self.indexer.get_doc_num() - ni + 0.5) /
            (ni + 0.5))
        term_2 = float(self.K1 + 1) * fi / (k + fi)
        term_3 = float(self.K2 + 1) * qfi / (self.K2 + qfi)

        return (term_1 * term_2 * term_3)        
    
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
        sys.exit(1)
    if int(sys.argv[3]) <= 0:
        print("ERROR - document results per query limit should " +
            "larger than 0")
        sys.exit(1)
    ranker = BM25(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    ranker.start_ranking()
        
