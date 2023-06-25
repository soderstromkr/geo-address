## [Go to GitHub repository](https://github.com/soderstromkr/geoaddress/)
## Code description
Code for paper ; ["Global reach, regional strength: Spatial patterns of a big science facility." DOI: 10.1002/asi.24811](https://asistdl.onlinelibrary.wiley.com/doi/full/10.1002/asi.24811)
## Interactive visualizations.
To see the interactive visualizations, see the [visualizations](visualizations.md) page
## How it works
* Dissagregates and geocodes author addresses from Web of Science (WoS) publication data, using the column DOI to uniquely identify publications. Full functionality with any address with the following form:
```
[Authors] Address;  
```
* It also find addresses and other named locations in the Address column, but won't be able to calculate aggregation metrics without x in [x] y;  
* Geocoding is done with the geopy package (More info below).    
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
pip install -e . 
```
**Note**: You might need administration rights, adding --user to the end of the previous command should take care of that.

## Usage
```
from geo_address import *
```
or see [here](https://github.com/soderstromkr/geoaddress/blob/main/example.ipynb) for an example that includes visualizations.
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
