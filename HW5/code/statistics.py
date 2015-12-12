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
import math
import os

class Statistics:
    def __init__(self, q_id):     # q_id: 1 / 2 / 3
        self.recall = list()      # overall recall
        self.precision = list()   # overall precision
        self.p_at_20 = 0          # p @ k
        self.dcg = list()         # DCG
        self.ndcg = list()        # NDCG
        self.avg_p = 0            # to compute MAP
        self.q_id = q_id
        self.doc_id_as_rank = list()
        self.doc_scores = list()
        self.relevant_docs = set()# set of String ids
    
    def run(self, hw3_path, judge_path, judge_qid):
        self.extract_relevant_doc_ids(judge_path, judge_qid)
        output_dir = 'outputs/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = output_dir + 'table_' + str(self.q_id)
        self.run_top_ranked_results(hw3_path, output_path)
        
    def run_top_ranked_results(self, hw3_path, output_path):
        self.print_statistics()
        results = open(hw3_path, 'r')
        output = open(output_path, 'w')
        hits_so_far = 0
        output.write('Rank\tDocId\tDoc_Score\tRelevance Level\t' + 
            'Precision\tRecall\tNDCG\n')
        print('Rank\tDocId\tDoc_Score\tRelevance Level\t' + 
            'Precision\tRecall\tNDCG')
        for line in results:
            relevance_level = '0'
            content = line.split('\t')
            # content[0] - query id
            # content[1] - Q0
            # content[2] - doc id
            # content[3] - rank
            # content[4] - score
            # content[5] - system name
            self.doc_id_as_rank.append(content[2])
            self.doc_scores.append(content[4])
            if content[2] in self.relevant_docs:
                # relevant level = 1
                hits_so_far += 1
                relevance_level = '1'
                self.avg_p += float(hits_so_far) / float(content[3])
                if int(content[3]) == 1:
                    self.dcg.append(float(1))
                else:
                    self.dcg.append(self.dcg[-1] + 
                        1 / math.log(float(content[3]), 2))
            else:
                # relevance level == 0
                if int(content[3]) == 1:
                    self.dcg.append(float(0))
                else:
                    self.dcg.append(self.dcg[-1])
            self.recall.append(float(hits_so_far)
                / len(self.relevant_docs))
            self.precision.append(float(hits_so_far)
                / float(content[3]))
            ## NDCG:
            if hits_so_far == 0:
                self.ndcg.append(float(0))
            elif int(content[3] == 1):
                self.ndcg.append(float(1))
            else:
                ideal_dcg = float(1)
                for i in range(2, hits_so_far + 1):
                    ideal_dcg += float(1) / math.log(i, 2)
                self.ndcg.append(self.dcg[-1] / ideal_dcg)
            
            output.write(content[3] + '\t' + content[2] + '\t' +
                content[4] + '\t' + relevance_level + '\t' +
                str(self.precision[-1]) + '\t' + 
                str(self.recall[-1]) + '\t' + str(self.ndcg[-1]) + '\n')
            print(content[3] + '\t' + content[2] + '\t' +
                content[4] + '\t' + relevance_level + '\t' +
                str(self.precision[-1]) + '\t' + 
                str(self.recall[-1]) + '\t' + str(self.ndcg[-1]))
        # end of for line
        self.p_at_20 = self.precision[19]
        self.avg_p = self.avg_p / hits_so_far
        output.write('P@20: ' + str(self.p_at_20) + '\n')
        print('P@20: ' + str(self.p_at_20))
        output.write('AVG_P: ' + str(self.avg_p) + '\n')
        print('AVG_P: ' + str(self.avg_p))
        results.close()
        output.close()
    
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
