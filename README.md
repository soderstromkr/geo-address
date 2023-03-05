## Code description
Code for paper (submitted): "Global reach, regional strength: Spatial patterns of a big science facility."
## Interactive visualizations.
To see the interactive visualizations, see the [visualizations](geoaddress/visualizations) page
## How it works
Dissagregates and geocodes author addresses from Web of Science (WoS) data and/or any address with the following form:
```
[Authors] Address;  
```
Geocoding done with the geopy package (More info below).    
## More functionality
- distance measurements between addresses and to a point of origin
## Important info
This package uses geopy for the geocoding module. See [geopy's documentation](https://geopy.readthedocs.io/en/stable/) for more info. 
- This example uses the GoogleV3 API, which needs an API Key. Read [here](https://developers.google.com/maps/documentation/geocoding/). 
- Make sure you include an API key [here](geo_address/API_key.txt) if needed.
- You can also change the geocoder [here](geo_address/processing.py) if you prefer.
## Installation
**Recommended** in order to change API key and/or geocoded as detailed above. 
```
git clone https://github.com/soderstromkr/geoaddress.git
cd geoaddress
python setup.py install
```
## Usage
```
from geo_address import *
```
or see [here](example.ipynb) for an example (in-progress).
## Requirements
Uses python 3.x.x
- pandas
- numpy
- tqdm
- geopy
- re
- pickle 
- sklearn
-	haversine
## Recommendations
- Current geocoder gave the best results in paper.
- begin_geocode() creates a checkpoint folder to keep track of progress, which can be re-started. (Make sure to delete the checkpoint file if doing a new run or project.)
