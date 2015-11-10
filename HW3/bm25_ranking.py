#!/usr/bin/env python
import os
import sys
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
        
    
    def start_ranking(self):
        index = self.indexer.get_index()
        i = 1 # query ID
        for q_dict in self.query.get_queries():
            # this is the for loop to inspect each query
            for doc_pair in index[q_dict.keys()[0]]:
                # this is the for loop to inspect each doc for cur query
                # i.e. for each doc_pair has the first term in the query
                # Inspect if this doc has all query terms
                doc_id = doc_pair[0]
                tf = {q_dict.keys()[0] : doc_pair[1]}
                all_flag = True
                j = 1
                while all_flag and j < len(q_dict):
                    # for each other terms in query
                    for d_p in index[q_dict.keys()[j]]:
                        # for each doc pair in index for cur term
                        if d_p[0] == doc_id:
                            tf[q_dict.keys()[j]] = d_p[1]
                            j += 1
                            break
                    # the inner for loop cannot find the matching doc:
                    all_flag = False
                    
                    
            
            i += 1
    
    
        
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
    #test
    rank = BM25('test.out','queries.txt','')
    print rank.indexer.get_doc_num()
    print rank.query.queries[0]
        
