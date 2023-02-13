from geopy.geocoders import GoogleV3 #import your preferred API here

import pandas as pd 
import numpy as np

import re
from tqdm import tqdm

import pickle

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


def begin_geocode(df):
    
    """
    Main geocoding loop.
    Inputs: Pandas dataframe.
    Outputs: coordinate array 
    
    Uses locator function from geopy, with GoogleV3 geocoder, can be changed
    below. For information on choosing a geocoder that works for you.
    https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders
    
    """

    #load API key
    with open('geo_address/API_key.txt') as f:
        api = f.read()

    locator = GoogleV3(api_key=api) # choose geocoder here
    print('Using {} geocoder from geopy'.format(locator))
    #checks if a checkpoint exists, you might want to delete it from the folder 
    #if you want to start another search
    try:
        with open('geo_address/checkpoints/checkpoint', 'rb') as fp:
            checkpoint = pickle.load(fp)
    #sets checkpoing list as empty
    except FileNotFoundError: 
        checkpoint = []
    #make a new column for split addresses, maybe not necessary but cleaner
    print('Preparing address field for geocoding...')
    df['Addresses_split'] = df['Addresses'].str.split(';') #splits unique addresses
    df = df.dropna(subset='Addresses_split').reset_index() #removes missing data
    #some more preparation
    coords=checkpoint #restores from checkpoint
    range_ = range(df.Addresses_split.shape[0]) #checks data range for iteration
    #start main loop    
    for row,idx in enumerate(pbar:= tqdm(range_[len(coords):])):
        pbar.set_description("Geocoding row {} of {}".format(idx,range_[-1]+1))
        #for every element in row
        for loc in df.Addresses_split[df.Addresses_split.index==idx]:
            #tries to find coordinates for each address in each row
            try: 
                c = [locator.geocode(f'{i}').point[:2] for i in loc]
            #sets nan to whole row if one of the addresses isn't found
            except AttributeError:
                print('Error in row {}, using nan'.format(loc))
                c = [np.nan]
            #appends coordinates
            coords.append(c)
            #saves step in checkpoint file
            with open('geo_address/checkpoints/checkpoint', 'wb') as fp:
                pickle.dump(coords, fp)

    return coords
