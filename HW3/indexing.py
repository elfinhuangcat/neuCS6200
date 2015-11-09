#!/usr/bin/env python
import os

class InvertIndex():
    def __init__(self):
        self.invert_index = dict() #index
        self.ids = list()          #store doc Ids
        self.dl = list()           #store doc lengths
        self.num_of_docs = 0       #number of documents in collection
    def start_build_index(self, input_file_path):
        if not os.path.isfile(input_file_path):
            print("ERROR - input file not exist.")
            exit(1)
        collection = open(input_file_path)
        cur_id = None
        temp_fq_dict = None # to store the terms dict for a doc
        temp_dl = None # to store the current doc's dl
        for line in collection:
            if line.startswith('\n'):
                continue
            if line.startswith('#'):
                cur_id = line[1:].strip()
                self.ids.append(cur_id)
                self.num_of_docs += 1
                ## Clear all the items in the dict that belong to the 
                ## previous doc:
                self.trans_to_index(temp_fq_dict, cur_id)
                temp_fq_dict = dict()
                ## Append dl of the previous doc:
                if not (temp_dl == None):
                    self.dl.append(temp_dl)
                temp_dl = 0
                continue
            # Otherwise these are tokens belonging to cur_id doc
            tokens = self.tokenize(line)
            temp_dl += len(tokens)
            for token in tokens:
                if token in temp_fq_dict:
                    temp_fq_dict[token] += 1
                else:
                    temp_fq_dict[token] = 1
        ## Clear all the items in the dict that belong to the 
        ## last doc:
        self.trans_to_index(temp_fq_dict, cur_id)
        collection.close()
        ## Append dl of the previous doc:
        self.dl.append(temp_dl)
        
    def output_index(self, output_file_path):
        outfile = open(output_file_path, 'w')
        # Number of docs in the collection:
        outfile.write(str(self.num_of_docs) + '\n')
        # Document IDs:
        for i in range(0, len(self.ids)-1):
            outfile.write(str(self.ids[i]) + ' ')
        outfile.write(str(self.ids[-1]) + '\n')
        # Document lengths:
        for i in range(0, len(self.dl)-1):
            outfile.write(str(self.dl[i]) + ' ')
        outfile.write(str(self.dl[-1]) + '\n')
        # The index:
        # term doc1 f_doc1 doc2 f_doc2 ... \n
        for term in self.invert_index:
            outfile.write(term + ' ')
            for i in range(0, len(self.invert_index[term]) - 1):
                outfile.write(str(self.invert_index[term][i][0]) + ' '
                    + str(self.invert_index[term][i][1]) + ' ')
            outfile.write(str(self.invert_index[term][-1][0]) + ' '
                + str(self.invert_index[term][-1][1]) + '\n')
        outfile.close()
        
    def tokenize(self, line):
        tokens = line.split(' ')
        tokens[-1] = tokens[-1][:-1] # remove the '\n'
        new_tokens = list()
        for token in tokens:
            if token != '' and (not token.isdigit()):
                new_tokens.append(token)
        del tokens
        return new_tokens
    
    def trans_to_index(self, temp_fq_dict, cur_id):
        if temp_fq_dict != None:
            for term in temp_fq_dict:
                if term in self.invert_index:
                    self.invert_index[term].append(
                        (cur_id, temp_fq_dict[term]))
                else:
                    self.invert_index[term] = [(cur_id, 
                        temp_fq_dict[term])]

if __name__ == '__main__':
    # Test code:
    index = InvertIndex()
    index.start_build_index('tccorpus.txt')
    index.output_index('test.out')
    print("doc num: " + str(index.num_of_docs))
    print("len of dl: " + str(len(index.dl)))
