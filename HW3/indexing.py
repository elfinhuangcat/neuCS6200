#!/usr/bin/env python
import os
import sys
"""
output index file format:
l1 num of doc \n
l2 doc ids, sep by ' ', \n
l3 doc dls, sep by ' ', \n
l4 and later:
term doc1 f_doc1 doc2 f_doc2 ... \n
"""

class InvertIndex():
    def __init__(self):
        self.invert_index = dict() #index
        self.ids = list()          #store doc Ids
        self.dl = list()           #store doc lengths
        self.num_of_docs = 0       #number of documents in collection
        
    def get_index(self):
        return self.invert_index
    def get_doc_id(self):
        return self.ids
    def get_dl(self):
        return self.dl
    def get_doc_num(self):
        return self.num_of_docs
        
    def start_build_index(self, input_file_path):
        """
        Input: document collection
        This method reads the documents and builds an inverted
        index for this collection.
        """
        if not os.path.isfile(input_file_path):
            print("ERROR - input file not exist.")
            sys.exit(1)
        collection = open(input_file_path)
        cur_id = None
        temp_fq_dict = None # to store the terms dict for a doc
        temp_dl = None # to store the current doc's dl
        for line in collection:
            if line.startswith('\n'):
                continue
            if line.startswith('#'):
                ## Clear all the items in the dict that belong to the 
                ## previous doc:
                self.trans_to_index(temp_fq_dict, cur_id)
                temp_fq_dict = dict()
                ## Append dl of the previous doc:
                if not (temp_dl == None):
                    self.dl.append(temp_dl)
                temp_dl = 0
                cur_id = line[1:].strip()
                self.ids.append(cur_id)
                self.num_of_docs += 1
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
        """
        Output: index file
        This method encodes the self.invert_index and other statistics
        into the output_file_path
        """
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
        
    def decode_index_file(self, index_file):
        """
        Input: index file
        This method decodes the index file and store the index in 
        self.invert_index
        """
        if not os.path.isfile(index_file):
            print("ERROR - input file not exist.")
            sys.exit(1)
        index_f = open(index_file, 'r')
        # read the total number of docs:
        self.num_of_docs = int(index_f.readline())
        # read the ids of docs:
        self.decode_id_line(index_f.readline())
        # read the dls:
        self.decode_dl_line(index_f.readline())
        # read the inverted index:
        self.decode_index(index_f)
        index_f.close()
        
        
        
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
    
    def decode_id_line(self, line):
        """
        @param: line - a line with '\n', sep by ' '
        Effect: stores the ids as a list in self.ids
        """
        self.ids = line[:-1].split(' ')
    def decode_dl_line(self, line):
        """ similar to decode_id_line()"""
        self.dl = list()
        strings = line[:-1].split(' ')
        for item in strings:
            self.dl.append(int(item))
    
    def decode_index(self, index_f):
        """
        @param: the file object of the index file
        Effect: decodes and stores the inverted index
                into self.invert_index
        """
        self.invert_index = dict()
        for line in index_f:
            arr = line[:-1].split(' ')
            self.invert_index[arr[0]] = list()
            i = 2
            while i < len(arr):
                self.invert_index[arr[0]].append(
                    (arr[i-1], int(arr[i])))
                i += 2

## MAIN
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR - you should invoke the indexer by: ")
        print("        indexer input-file output-file")
        sys.exit(1)
    indexer = InvertIndex()
    indexer.start_build_index(sys.argv[1])
    indexer.output_index(sys.argv[2])
    """
    ## before decoding:
    print("num of doc: " + str(indexer.num_of_docs))
    print("length of dls: " + str(len(indexer.dl)))
    print("num of terms: " + str(len(indexer.invert_index)))
    print("last term details: term - " + indexer.invert_index.keys()[-1])
    print("value: " + str(indexer.invert_index[indexer.invert_index.keys()[-1]]))

    ## test decoding:
    print("DECODING .. .")
    indexer.decode_index_file(sys.argv[2])
    print("num of doc: " + str(indexer.num_of_docs))
    print("length of dls: " + str(len(indexer.dl)))
    print("num of terms: " + str(len(indexer.invert_index)))
    print("last term details: term - " + indexer.invert_index.keys()[-1])
    print("value: " + str(indexer.invert_index[indexer.invert_index.keys()[-1]]))
    """

