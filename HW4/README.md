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
