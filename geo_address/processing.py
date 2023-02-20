from geopy.geocoders import GoogleV3 #import your preferred geocoder
import os 
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

    #load API key needed
    with open('geo_address/API_key.txt') as f:
        api = f.read()

    if not os.path.exists('geo_address/checkpoints'):
        os.mkdir('geo_address/checkpoints') 

    locator = GoogleV3(api_key=api) # choose geocoder here
    print('API domain: {}'.format(vars(locator)['domain']))
    #checks if a checkpoint exists, you might want to delete it from the folder 
    #if you want to start another search
    try:
        with open('geo_address/checkpoints/checkpoint', 'rb') as fp:
            checkpoint = pickle.load(fp)
            print('Checkpoint loaded!')
    #sets checkpoing list as empty
    except FileNotFoundError: 
        checkpoint = []
        print('No checkpoint found, starting from scratch!')
    #make a new column for split addresses, maybe not necessary but cleaner
    df['Addresses_split'] = df['Addresses'].str.split(';') #splits unique addresses
    df = df.dropna(subset='Addresses_split').reset_index() #removes missing data
    #some more preparation
    coords=checkpoint #restores from checkpoint
    range_ = range(df.Addresses_split.shape[0]) #checks data range for iteration
    #start main loop
    errors=[]    
    for row,idx in enumerate(pbar:= tqdm(range_[len(coords):])):
        pbar.set_description("Geocoding row {} of {}".format(idx,range_[-1]+1))
        #for every element in row
        for loc in df.Addresses_split[df.Addresses_split.index==idx]:
            #tries to find coordinates for each address in each row
            try: 
                c = [locator.geocode(f'{i}').point[:2] for i in loc]
            #sets nan to whole row if one of the addresses isn't found
            except AttributeError:
                print('Error in row {}, using nan'.format(idx))
                c = [np.nan]
                errors.append(idx)
            #appends coordinates
            coords.append(c)
            #saves step in checkpoint file
            with open('geo_address/checkpoints/checkpoint', 'wb') as fp:
                pickle.dump(coords, fp)

    if len(errors) > 0 :
        print('Could not find one or more addresses in the following rows: ', errors,'and have been removed.')
    else:
        print('Done!')

    return coords

def to_coord_data(df): #input df with coordinates and distances

    df['Fractional publications'] = 1/df['Num_Addresses']

    addresses_l = []
    multiplier_l = []
    num_addresses_l = []
    doi_l = []
    year_l = []
    n_coords_l = []
    m_d_b_a_l = []
    m_d_f_l = []
    d_t_f_l = []
    f_p_l = []
    #divide and collect data for row
    for i in range(len(df.index)):
        addresses = df['Addresses'].iloc[i]
        multiplier = df['Multiplier'].iloc[i]
        num_addresses = df['Num_Addresses'].iloc[i]
        doi = df['DOI'].iloc[i]
        year = df['Year'].iloc[i]
        n_coords = df['new_coords'].iloc[i]
        m_d_b_a = df['mean_distance_between_addresses'].iloc[i]
        m_d_f = df['mean_distance_to_facility'].iloc[i]
        d_t_f = df['distance_to_facility'].iloc[i]
        f_p  = df['Fractional publications'].iloc[i]
        #divide and collect data for each coordinate pair per row
        for j in range(len(n_coords.split('|'))):
            addresses_l.append(addresses.split(';')[j])
            multiplier_l.append(list(multiplier)[j])
            num_addresses_l.append(num_addresses)
            doi_l.append(doi)
            year_l.append(year)
            n_coords_l.append(n_coords.split('|')[j])
            m_d_b_a_l.append(m_d_b_a)
            m_d_f_l.append(m_d_f)
            d_t_f_l.append(list(d_t_f)[j])
            f_p_l.append(f_p)

    #create dataframe for mapping 
    #map data
    data = {

    'Addresses' : addresses_l,
    'Multiplier': multiplier_l,
    'Num_Addresses' : num_addresses_l,
    'DOI' : doi_l,
    'Year' : year_l,
    'Coordinates': n_coords_l,
    'mean_distance_between_addresses' : m_d_b_a_l,
    'mean_distance_to_facility' : m_d_f,
    'distance_to_facility' : d_t_f_l
    }
    #create df
    map_df = pd.DataFrame(
        data
        )
    map_df['Fractional pubs'] = f_p_l
    map_df = map_df.rename(columns={'Addresses':'Address'})
    #split lat, lon
    #lat_lon = map_df['Coordinates'].str.split(',', expand=True)
    #lat_lon = lat_lon.rename(columns={0:'lat',1:'lon'})



    return map_df









