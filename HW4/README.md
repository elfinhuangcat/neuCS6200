# HW4 - CS6200 Information Retrieval
_Yaxin Huang_

## How to Run the HW4.jar:
1. In your Terminal, cd to this directory.
2. Run the following command to index and retrieve documents:
   ```
   $ java -jar HW4.jar arg0 arg1 arg2
   ```
   where:    
  * **arg0** full path of the index directory (if it does not exist, the program will create one)
  * **arg1** full path to the CACM document directory, OR **-i**, which represents that no files need to be added to the index
  * **arg2** full path to the query file

   For example, the command can be:
   ```
   $ java -jar HW4.jar /home/username/Desktop/HW4/index \
     /home/username/Desktop/HW4/cacm /home/username/Desktop/HW4/queries
   ```
   OR
   ``` 
   $ java -jar HW4.jar /home/username/Desktop/HW4/index \
     -i /home/username/Desktop/HW4/queries
   ```
   (if the files have been added to the index)

## What's in This Repo
* [cacm](cacm/) - the folder containg all documents. (Not sumbitted in assignment)
* [HW4_Project](HW4_Project/) - the project folder, you can find the source codes from src/.
* [required_outputs](required_outputs/)
  * [comparison_table](required_outputs/comparison_table) - the table comparing the hits of HW3 and HW4
  * List_Q(n) - 4 files listing the top 100 results of 4 queries    
    [List_Q1](required_outputs/List_Q1)    
    [List_Q2](required_outputs/List_Q2)    
    [List_Q3](required_outputs/List_Q3)    
    [List_Q4](required_outputs/List_Q4)    
  * [outputs](required_outputs/outputs) - the standard outputs. I ran the jar and redirected the outputs to this file.
  * [TermFrequency.txt](required_outputs/TermFrequency.txt) - the sorted list of terms and term frequencies
  * [ZipfianCurve.png](required_outputs/ZipfianCurve.png) - the curve showing the relationship between rank and probability of occurrence
* [HW4.jar](HW4.jar) - the java executable
* [plot_zip.py](plot_zip.py) - the python code to plot the curve. It takes the "TermFrequency.txt" (which is in the same dir as the script) as input and plots the graph.
* [queries](queries) - the file containg all the queries. One query per line.
* [README.txt](README.txt) - the README in txt format

## The comparison table of HW3 and HW4
|query     |     total#_docs_retrieved_using_Lucene-hw4   |    _using_your_indexer_with_BM25-hw3  |
|:---------:|:------------------------------------------:|:---------------------------------:|
|  q1      |                    440                       |                871          |
|  q2      |                    1579                      |               1632          |
|  q3      |                    272                       |               1386          |
|  q4      |                    1529                      |               1540          |


## Assignment Requirement
For this homework, you need to download and setup [Lucene](https://lucene.apache.org/), an open source information retrieval library. Lucene is widely used in both academic and commercial search engine applications. Solr and ElasticSearch are both based on the Lucene libraries.    
In order to make things easier for you, we are providing you with a the basic code (see attachement) that can serve as a starting point to create your search engine. This code is based on Lucene Version 4.7.2 (see attached files, or go to [https://archive.apache.org/dist/lucene/java/4.7.2/](https://archive.apache.org/dist/lucene/java/4.7.2/)) and is written in Java. However, it is up to you to choose the implementation of your preference.    
Once you download Lucene, the setup is pretty straightforward. You need to create a new Java project and add the following three jars into your project’s list of referenced libraries: 1) lucene-core-VERSION.jar, 2) lucene-queryparser-VERSION.jar, and 3) lucene-analyzers-common-VERSION.jar. Where VERSION is to be substituted with the version of Lucene that you downloaded. For example, in the provided example, we have version 4.7.2, therefore, the first jar file would be lucene-core-4.7.2.jar. Make sure that the system requirements for that version are met.    
You will need to go through Lucene’s documentation (and the provided code) to perform the following:    
* Index the [raw (unpre-processed) CACM corpus](http://www.search-engines-book.com/collections/) using Lucene. Make sure to use “SimpleAnalyzer” as your analyzer.
* Build a list of (unique term, term_frequency) pairs over the entire collection. Sort by frequency.
* Plot the Zipfian curve based on the list generated in (2) (you do not need Lucene to perform this. You may use any platform/software of your choosing to generate the plot)
* Perform search for the queries below. You need to return the top 100 results for each query. Use the default document scoring/ranking function provided by Lucene.
  - portable operating systems
  - code optimization for space efficiency
  - parallel algorithms
  - parallel processor in information retrieval
* Compare the total number of matches in 4 to that obtained in hw3

What to submit:
* ReadMe.txt
* Your source code for indexing and retrieval
* A sorted (by frequency) list of (term, term_freq pairs)
* A plot of the resulting Zipfian curve
* Four lists (one per query) each containing at MOST 100 docIDs ranked by score (optional: provide a text snippet of 200 chars along the DocID).
* A table comparing the total number of documents retrieved per query using Lucene’s scoring function vs. using your search engine (index with BM25) from the previous assignment

