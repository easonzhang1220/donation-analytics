# coding: utf-8
import numpy as np
import pandas as pd
import datetime

###### Global Prarameters ######

# For this data challenge there should a Database for store valid doners,it could be any kinds of Database 
# products, like Oracle, DB2, MySQL,SQLite... OR for convience, we could using Pandas DataFrame instand.

# histor_Data used for storing Valided donors and also for varifying weather the new record is repeat donor.

history_Data = pd.DataFrame([],columns =['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT', 'TRANSACTION_AMT','OTHER_ID'])

# To similating streaming processing,the input txt file would be read line by line. and this program as coding 
# mainly by Python /Pandas,and it using Pandas Series structure to store each line data, and we download the HEAD FILE from 
# FEC website(https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml)

head_columns = ['CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM','TRANSACTION_TP', 
                'ENTITY_TP','NAME', 'CITY', 'STATE', 'ZIP_CODE','EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 
                'TRANSACTION_AMT','OTHER_ID', 'TRAN_ID', 'FILE_NUM', 'MEMO_CD','MEMO_TEXT', 'SUB_ID']

# the the columns array can be instand by following:
# head_columns = pd.read_csv('../input/indiv_header_file.csv').columns.values

###### Functions ######

# Because we are only interested in individual contributions, we only want records that have the field, OTHER_ID, 
# set to empty. If the OTHER_ID field contains any other value, you should completely ignore and skip the entire record.

# Other situations you can completely ignore and skip an entire record:

#     If TRANSACTION_DT is an invalid date (e.g., empty, malformed)
#     If ZIP_CODE is an invalid zip code (i.e., empty, fewer than five digits)
#     If the NAME is an invalid name (e.g., empty, malformed)
#     If any lines in the input file contains empty cells in the CMTE_ID or TRANSACTION_AMT fields

def line_pre_check(line):
        try:
            datetime.datetime.strptime(line.TRANSACTION_DT, '%m%d%Y')
        except:
            return False 
       
        if (line.CMTE_ID == '' 
        or line.TRANSACTION_AMT == '' 
        or line.OTHER_ID != '' 
        or len(line.ZIP_CODE) < 5 
        or line.NAME == ""):
            return False
    
        return True


# For the purposes of this challenge, if a donor had previously contributed to any recipient listed in the 
# itcont.txt file in any prior calendar year, that donor is considered a repeat donor. Also, for the purposes 
# of this challenge, you can assume two contributions are from the same donor if the names and zip codes are identical.

def repeat_donor(line):
    # Search the prevoir year records for the same donor(treat the Donor the same one for the same NAME and ZIP_CORD )
    name_mask = history_Data['NAME'] == line.NAME
    zipcode_mask = history_Data['ZIP_CODE'] == line.ZIP_CODE[:5]
    year_mask = history_Data['TRANSACTION_DT'] < line.TRANSACTION_DT[-4:]
    mask_results = history_Data[name_mask & zipcode_mask & year_mask]
    
    # if the the search results have record, it's repeat dornor. return True
    if mask_results.shape[0] > 0:
        return True
    else:
        return False


# while there are many fields in the file that may be interesting, below are the ones that you’ll need to 
# complete this challenge:

    # CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution
    # NAME: name of the donor
    # ZIP_CODE: zip code of the contributor (we only want the first five digits/characters)
    # TRANSACTION_DT: date of the transaction
    # TRANSACTION_AMT: amount of the transaction
    # OTHER_ID: a field that denotes whether contribution came from a person or an entity
    
# Only choose above columns when append record to history_Data

def add_to_history(line):
    history_Data.loc[len(history_Data)] ={'CMTE_ID':line.CMTE_ID,
                                          'NAME':line.NAME,
                                          'ZIP_CODE':line.ZIP_CODE[:5],
                                          'TRANSACTION_DT':line.TRANSACTION_DT[-4:],
                                          'TRANSACTION_AMT':line.TRANSACTION_AMT,
                                          'OTHER_ID':line.OTHER_ID}


# For this challenge, we are asking you to take a file listing individual campaign contributions for multiple years, 
# determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, 
# repeat_donors.txt.
# For each recipient, zip code and calendar year, calculate these three values for contributions coming from repeat donors

# total dollars received
# total number of contributions received
# donation amount in a given percentile

# percentile.txt, holds a single value -- the percentile value (1-100) that your program will be asked to calculate.


def contribution_from_repeat_donors(line):
    #first 3 output values
    recipient_mask = history_Data['CMTE_ID'] == line.CMTE_ID
    zipcode_mask = history_Data['ZIP_CODE'] == line.ZIP_CODE[:5]
    year_mask = history_Data['TRANSACTION_DT'] == line.TRANSACTION_DT[-4:]

    # get the a list of 'TRANSACTION_AMT' after apply the above filters
    repeat_donors = history_Data[recipient_mask & zipcode_mask & year_mask]['TRANSACTION_AMT']
    repeat_donors_contributions = list(map(int, list(repeat_donors)))
  
    #caculating percentile data:
    percentile = pd.read_csv('./input/percentile.txt',header = None).values[0][0]

    #For the percentile computation use the **nearest-rank method** by numpy.percentile function 
    #with parameter interpolation='nearest'
    percentile_amount = np.percentile(repeat_donors_contributions,percentile,interpolation='nearest')
    #Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and 
    #round anything from $.50 and up to the next dollar)
    if percentile_amount == 0.5:
        percentile_amount = 1
    else:
        percentile_amount = round(percentile_amount)
        
    #combine the output line:
    output = line.CMTE_ID + '|' + line.ZIP_CODE[:5] + '|' + line.TRANSACTION_DT[-4:] + '|' + str(percentile_amount) + '|' + str(sum(repeat_donors_contributions)) + '|' + str(len(repeat_donors_contributions))
    print("Append \"%s\" to repeat_donors.txt file." %output)
    
    # Write output line to output file 
    File = open('./output/repeat_donors.txt','a')
    File.write(output + "\n")  
    File.close()

    
###### the main() function of the program ######   
    
def main():
    file = open('./input/itcont.txt')

    for line in file:
            line = pd.Series(line.split('|'),index = head_columns)     

    # the first step is to check the format of each line, Valid Donor if Return TRUE, Ignored if return False
            if line_pre_check(line) is not True:
                #print("This line is not valid input, ignored, read next line.")
                continue

    # For repeat donor(She/He is have records for preview calander year),we need do:
    #     * put the record to history_Data
    #     * caculating the statistic and write to output file
    # For other valid donor, only put the record to history_Data

            if repeat_donor(line) is True:
                add_to_history(line)
                #print("Find a Repeat Donor") 
                contribution_from_repeat_donors(line)         
            else:
                add_to_history(line)
                #print('Not a Repeat Donor, add to history_Data database.')

    #force the file closed
    file.close()


if __name__ == "__main__":
    main()

