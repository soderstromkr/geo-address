import pandas as pd 
import re
from tqdm import tqdm


def split_address(df,column_name):
   
    "Module takes Web of Science addresses \
     with the format '[Author(s)]Address' \
     and returns unique addresses with a \
     multiplier that accounts for the \
     number of authors for each unique \
     address. \
     \
     df : Pandas dataframe, with WoS data \
     column_name : str, name of column with address data" 

    data = []

    df = df.dropna(subset=column_name).reset_index()

    for row in (pbar := tqdm(range(len(df.index)))):

        pbar.set_description('Processing row {}'.format(row))

        #Processing addresses
        #Preparing and separating       
        multiplier=[]
        #find Author names in brackets
        author_names = re.findall('\[.*?\]', df[column_name].loc[row])
        #find addresses outside of brackets
        addresses = re.findall('(.*?)\[.*?\]', df[column_name].loc[row])[1:]
        #join last address, lost in previous step
        addresses.append(df[column_name][row].split(';')[-1].split(']')[-1])

        DI = df['DOI'].loc[row]
        Year = df['Year'].loc[row]


        #Collecting authors and addresses
        num_authors = len(author_names)
        num_addresses = len(addresses)

        addresses = str(addresses)

        #appending multiplier
        for i in range(num_authors):
            
            multiplier.append(author_names[i].count(';')+1)

                
        data.append([author_names,addresses,multiplier,num_addresses, DI, Year])

    df = pd.DataFrame(data, columns=['Author_names','Addresses','Multiplier','Num_Addresses', 'DOI', 'Year']) 

    #cleanup
    df['Addresses'] = df.Addresses.str.replace(
    '[','',regex=True).str.replace(
    ']','',regex=True).str.replace(
    "'","",regex=True).str.replace(
    ',','',regex=True).str.replace(
    ';   ',';').str.lstrip()

    return df 



    
