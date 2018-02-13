
# Libraries and Enviroments
1. Python 3.6.3
2. Anaconda 4.3.33 (or numpy 1.14.0 and pandas 0.22.0)

# Where to run program:

**[Repo Root path]/run.sh**
![Alt text](./src/pictures/run.png)

# Repo directory structure

the only different is that I add **donation-analytics.py** file to origin Insight Repo.

The directory structure:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── donation-analytics.py
    ├── input
    │   └── percentile.txt
    │   └── itcont.txt
    ├── output
    |   └── repeat_donors.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
                ├── input
                │   └── percentile.txt
                │   └── itcont.txt
                |__ output
                   └── repeat_donors.txt
   
 # Testing the directory structure and output format
 
 run test command  **<[donation-analytics]>/insight_testsuite/run_tests.sh **
 and the results show the program pass the test case. 
 ![Alt text](./src/pictures/test_1_results.png)
  
  
 then check the output file：repeat_donors.txt
 ![Alt text](./src/pictures/repeat_donors.png)
 

