# geo-address (in-progress)
## Description
Dissagregates authors addresses from Web of Science (WoS) data.
## Important info
- This package uses geopy for the geocoding module. See [geopy's documentation](https://geopy.readthedocs.io/en/stable/) for more info. 
- This example uses the GoogleV3 API, which needs an API Key. Read [here](https://developers.google.com/maps/documentation/geocoding/). 
- Make sure you include an API key [here](geo_address/API_key.txt) if needed.
- You can also change the geocoder [here](geo_address/processing.py) if you prefer.
## Installation
```
git clone https://github.com/soderstromkr/geo-address.git
```
or
```
pip install git+https://github.com/soderstromkr/geo-address.git
```
Draft in progress: The spatial distribution of big science: A methodology for disaggregating and geocoding address fields (Working title)
## Requirements
Uses python 3.x.x
- pandas
- numpy
- tqdm
- geopy
- re
- pickle
## Example
See [here](example.ipynb) for an example (in-progress).
