# CS6200 Information Retrieval - HW5
_Yaxin Huang_

## How to Run the Codes
1. In your Terminal, cd to this directory, and cd to the [code](code/) directory.
2. Run the following script to get all outputs by entering these commands:
```
$ chmod 755 run
$ ./run
```
3. All the generated outputs are under [code/outputs](code/outputs) directory.
  - [q1_hw3_result.eval](code/outputs/q1_hw3_result.eval) HW3 query 1 results
  - [q2_hw3_result.eval](code/outputs/q2_hw3_result.eval) HW3 query 2 results
  - [q3_hw3_result.eval](code/outputs/q3_hw3_result.eval) HW3 query 3 results
  - [table_1](code/outputs/table_1) The required statistics for query 1
  - [table_2](code/outputs/table_2) The required statistics for query 2
  - [table_3](code/outputs/table_3) The required statistics for query 3

## What's Inside the Repo
* [README.md](README.md)
* [code](code/)
  - [outputs](code/outputs) described in the last section
  - [cacm.rel](code/cacm.rel) the judgement file
  - [results.eval](code/results.eval) results generated in HW3
  - [run](code/run) the script to run the python codes authomatically
  - [statistics.py](code/statistics.py) the python module to compute statistics
  - [transform_hw3.py](code/transform_hw3.py) the python module to extract needed HW3 results to [outputs](code/outputs) directory

## Results
* The result tables for three queries can be found in [outputs](code/outputs) directory.
* Query 1 P@20: 0.15
* Query 2 P@20: 0.25
* Query 3 P@20: 0.45
* MAP: (0.599431818182 + 0.3120861678 + 0.622468078061) / 3 = 0.5113286880143333

## Assignment Description
**Goal: To evaluate retrieval effectiveness**    
After having built your search engine, performed indexing and retrieval. It is now time to evaluate how well the search engine did at finding pertinent documents in response to queries. There exist several effectiveness measure to quantify this performance, such as Precision, Recall, Mean Reciprocal Rank (MRR), and Discounted Cumulative Gain (DCG) for instance.    
You may choose to evaluate any of the following search engine: (1) your search engine (HW3) OR (2) Lucene-based (HW4) – (you may use Elasticsearch instead if you prefer).    
Implement the following using the programming language of your choice:    

1. Precision
2. Recall
3. P@K, where K = 20
4. Normalized Discounted Cumulative Gain (NDCG)
5. Mean Average Precision (MAP)

The relevance judgements for the CACM test collections are available [here](http://www.search-engines-book.com/collections/)    
The queries of interest are a subset of those in HW3 and HW4 (see below). Therefore, you can simply use the results obtained in either homework. CACM query IDs are provided below between parentheses (ID)    
* portable operating systems (12)
* code optimization for space efficiency (13)
* parallel algorithms (19)

The relevance judgements are interpreted as follows:
```
Q_ID    Q0   DOC_ID   d

Q_ID: Query ID (in this case, you have 12, 13, and 19)

Q0: To be ignored

DOC_ID: A unique document ID, basically the name of the HTML file

d: A digit representing relevance level, where 0 means non-relevant and 1 means relevant
```

For example: `4 Q0 CACM-3128 1` is interpreted as: The document whose ID is `CACM-3128` is RELEVANT to the query whose ID is `4`    

**What to hand in:**    

1. Your source code for implementing the measure 1 through 5 and a README file
2. A table with the following columns and values:
  - Rank
  - Document ID
  - Document score
  - Relevance level
  - Precision
  - Recall
  - NDCG
  You need 1 table per query (3 tables in total)
3. Values of P@20 and MAP

