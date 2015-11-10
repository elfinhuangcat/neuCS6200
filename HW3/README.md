## CS6200 Information Retrieval
_Author: Yaxin Huang huang.yax@husky.neu.edu_ [wiki for BM25 algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)

### How to Run the Code
1. In your CCIS Linux machine, open the Terminal and cd to this directory (the dir containing this README file)
2. In order to enable the shell scripts to run, enter the following commands:
    ```
    chmod 755 indexer
    chmod 755 bm25
    ```
3. Build the index by using the command in following format:
    ```
    ./indexer [input_file_path] [index_output_path]
    ```
    where the file with the path ```input_file_path``` should already exist and the index built will be output to the file with path ```index_output_path```
    For example:
    ```
    ./indexer tccorpus.txt index.out
    ```
4. To start ranking the documents with queries stored in a file, use the command in following format:
    ```
    ./bm25 [index_output_path] [query_file_path] [limit_of_docs_per_query] > [result_output_path]
    ```
    where the file with path ```index_output_path```(index file) and ```query_file_path```(queries file) should exist. ```limit_of_docs_per_query``` is an integer larger than 0.
    For example:
    ```
    ./bm25 index.out queries.txt 100 > results.eval
    ```
    will output the result to the ```results.eval``` in this repo.
5. The result file consists of lines like: 
    ```
    query_id Q0 doc_id rank BM25_score bm25_rank_system
    ```

### Files in Repo
- [bm25](bm25): shell script to run the ranking algorithm
- [indexer](indexer): shell script to run the the indexing process
- [indexing.py](indexing.py): module providing methods to index and decode an index from index.out file
- [bm25_ranking.py](bm25_ranking.py): module providing methods to implement the BM25 ranking algorithm for multiple queries
- [tccorpus.txt](tccorpus.txt): input file
- [queries.txt](queries.txt): queries file
- [results.eval](results.eval): the ranking results for the queries in the [queries.txt](queries.txt) file with 100 document results limit per query
- [index.out](index.out): the index stored in disk
- [README.md](README.md): this file


### Implementation Description
There are two major classes that provides data structure and methods to solve the problem:    

1. **class InvertIndex**:
    ```python
    class InvertIndex():
        def __init__():
            ## major class members:
            # a data structure which is a python dictionary like 
            # {word : [(docid, tf), (docid, tf)], ...} 
            self.invert_index
            # an array storing the length of documents
            self.dl
        ## major methods:
        # builds the index and stores the index and other statistics 
        # in class members
        def start_build_index(input_file_path) 
        
        # outputs the built index and other statistics to a 
        # file specified in the param
        def output_index(index_output_path)
        
        # decodes the index file and store information 
        # in the class members
        def decode_index_file(index_output_path)
    ```

2. **class BM25**
    ```python
    class BM25():
        def __init__():
            ## major class members:
            # index of class InvertIndex
            self.indexer
            # list of python dictionaries, where each dict is 
            # like {term: query_term_freq, ...}
            self.query
        ## major methods:
        # starts the ranking process, invoke helper functions if needed
        def start_ranking():
            for each query in queires:
                for each term in query:
                    for each document in inverted_index[term]:
                        add bm25(document, query, term) to the
                        score of document (which is initialized as 0)
        # given the needed information, computes part of the 
        # BM25 score and returns it
        def bm25(doc, query.info, term):
            """
            Because the BM25 score is a summation over 'something',
            here we can compute part of the BM25 score because it only
            requires info about current query term we are inspecting
            and the current document information in invert_index[term]
            
            Note that the parameters such as k1, k2, b are known.
            """
            returns something(doc, query.info, term)
    ```


### Assignment Description
1. **Indexing and Retrieval** - implement a small search engine and the main steps are:
    * Read in the already stemmed document collection provided in the file [tccorpus.txt](tccorpus.txt) inside tccorpus.zip. This is an early standard collection of abstracts from the Communications of the ACM.
    * Build a simple inverted indexer that reads the corpus and writes the index. You should invoke it with    
      ```
      indexer tccorpus.txt index.out
      ```    
    * Implement the BM25 ranking algorithm, and write a program to provide a ranked list of documents for a file with one or more queries. You should pass parameters for the index file, the query file, and the maximum number of document results, and return documents on the standard output, like so:
      ```
      bm25 index.out queries.txt 100 > results.eval
      ```    
    * Submit the output from this run, with the top 100 document IDs and their BM25 scores for each test query according to the following format:
      ```
      query_id Q0 doc_id rank BM25_score system_name
      ```    
      The string Q0 is a literal used by the standard TREC evaluation script. You can use any space-free token for your system_name.
    * Also, submit your code, instructions for compiling it, and a short report describing your implementation.

2. **Tokenized Document Collection**
    * The provided [tccorpus.txt](tccorpus.txt) file is in the format:
      - A # followed by a document ID
      - Lines below the document ID line contain stemmed words from the document.
    * For example:
      ```
      # 1
      this is a tokenzied line for document 1
      this is also a line of document 1
      # 2
      from here lines for document 2 begin
      ...
      ...
      # 3
      ...
      ```
    * For tokenization, simply break the character sequence at any run of whitespace (space, newline, etc.).
    * Also, because this each document ends with a list of numerical cross references, you can, for this assignment, ignore any tokens that contain only the digits 0-9.

3. **Building an Inverted Index** - The following data structures are required for BM25 computation:
    * Term frequencies (tf) are stored in inverted lists: ```word -> (docid, tf), (docid, tf), ...```
    * For this assignment, you don't need to consider term positions within documents.
    * Store the number of tokens in each document in a separate data structure.
    * You may employ any concrete data structures convenient for the programming language you are using, as long as you can write them to disk and read them back in when you want to run some queries.

4. **BM25 Ranking**
    * Retrieve all inverted lists corresponding to terms in a query.
    * Compute BM25 scores for documents in the lists.
    * Make a score list for documents in the inverted lists.
    * Accumulate scores for each term in a query on the score list.
    * Assume that no relevance information is available.
    * For parameters, use ```k1=1.2, b=0.75, k2=100```.
    * Sort the documents by the BM25 scores.

5. **Test Queries** - Use the following stemmed test queries, also provided in the file [queries.txt](queries.txt):

Query ID      | Query Text
:-------------: | :-------------:
1  | portabl oper system
2  | code optim for space effici
3  | parallel algorithm
4  | distribut comput strctur and algorithm
5  | appli stochast process
6  | perform evalu and model of comput system
7  | parallel processor in inform retriev
