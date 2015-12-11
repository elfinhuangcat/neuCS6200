#!/usr/bin/env python
"""
This module takes the arguments:
<path-to-hw3-results-for-one-query>
<query-id-hw3>
<path-to-cacm.rel>
<query-id-cacm>

And prints the statistics required to standard output.
"""
import sys

class Statistics:
    def __init__(self, q_id):# q_id: 1 / 2 / 3
        self.recall = 0      # overall recall
        self.precision = 0   # overall precision
        self.p_at_20 = 0     # p @ k
        self.ndcg = 0        # NDCG
        self.mean_avg_p = 0  # MAP
        self.q_id = q_id
        self.relevant_docs = set()
    
    def run(self, hw3_path, judge_path, judge_qid):
        self.extract_relevant_doc_ids(judge_path, judge_qid)
    
    """
    judge_path - path to cacm.rel
    judge_qid  - query id to extract (cacm qid) [String]
    """
    def extract_relevant_doc_ids(self, judge_path, judge_qid):
        judge = open(judge_path, 'r')
        for line in judge:
            content = line.split(' ')
            if content[0] == judge_qid:
                doc_id = content[2][5:]
                print("relevant id: " + doc_id)
                self.relevant_docs.add(doc_id)
        judge.close()
    
    def print_statistics(self):
        print("Statistics for Query " + str(self.q_id))
        
        
if __name__ == '__main__':
    # sys.argv[0] - ignore
    # sys.argv[1] - <path-to-hw3-results-for-one-query>
    # sys.argv[2] - <query-id-hw3>
    # sys.argv[3] - <path-to-cacm.rel>
    # sys.argv[4] - <query-id-cacm>
    if len(sys.argv) != 5:
        print("ERROR - please read the input params requirement")
        exit(1)
    analysis = Statistics(sys.argv[2])
    analysis.run(sys.argv[1], sys.argv[3], sys.argv[4])
