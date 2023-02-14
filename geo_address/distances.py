import pandas as pd 
import numpy as np
from tqdm import tqdm
import warnings
from sklearn.metrics import DistanceMetric
dist = DistanceMetric.get_metric('haversine')
from haversine import haversine, Unit


def address_distance(df, origin):

	new_coords=[]
	df = df.dropna(subset='coords').reset_index()
	df['coords'] = df['coords'].astype(str)
	
	for i in df.index:
	    nc = df['coords'][i].replace('[','').replace(']','').replace('),','|').replace('(','').replace(')','').replace(' ','')
	    new_coords.append(nc)
	    
	df['new_coords'] = new_coords
	df = df.drop(columns=['index'])
	df = df.drop_duplicates('DOI')

	mean_list = []
	dist_to_fal = []
	mean_dist_to_fal = []

	for row in tqdm(range(df.shape[0])):
	    addresses = df.loc[row]['Num_Addresses']
	    
	    #for matrix
	    lat_list = []
	    lon_list = []

	    #for distance to facility
	    fal_list = []
	    
	    for address in range(addresses):
	        try:
	            lat = df.loc[row]['new_coords'].split('|')[address].split(',')[0]
	            
	            lon = df.loc[row]['new_coords'].split('|')[address].split(',')[1]
	            
	        except IndexError:
	            
	            lat = 0
	            lon = 0
	        
	        #convert to radians
	        lat_rad = np.radians(float(lat))
	        lon_rad = np.radians(float(lon))

	        origin_lat_rad = np.radians(origin[0])
	        origin_lon_rad = np.radians(origin[1])

	        lab = haversine(
	        	(float(lat), float(lon)), (origin), unit='km')
	        
	        fal_list.append(np.round(lab,2))
	    
	        #for within distance (between addresses)
	        lat_list.append(lat_rad)
	        lon_list.append(lon_rad)
	        
	        p_mat = pd.DataFrame({'lat' : lat_list,'lon' : lon_list})

	    a = dist.pairwise(p_mat[['lat','lon']].to_numpy())*6371
	    np.fill_diagonal(a, np.nan)
	    
	    #expecting errors here
	    with warnings.catch_warnings():
	        warnings.simplefilter("ignore", category=RuntimeWarning)
	        b = np.nanmean(a)
	    
	    
	    mean_list.append(b)
	    dist_to_fal.append(fal_list)
	    mean_dist_to_fal.append(np.mean(fal_list))
	    
	df['mean_distance_between_addresses'] = mean_list
	df['distance_to_facility'] = dist_to_fal
	df['mean_distance_to_facility'] = mean_dist_to_fal

	return df