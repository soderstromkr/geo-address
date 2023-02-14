# geo-address (in-progress)
1. Dissagregates authors addresses from Web of Science (WoS) data.   
1. Geocode and mapping examples included in the example notebooks.   
This package uses geopy for the geocoding module. See [geopy's documentation](https://geopy.readthedocs.io/en/stable/) for more info. 
This example uses the GoogleV3 API, which needs an API Key. Read [here](https://developers.google.com/maps/documentation/geocoding/). Make sure you include an API key [here](geo_address/API_key.txt).\
You can also change the API [here](geo_address/processing.py)
Install options:
```
git clone https://github.com/soderstromkr/geo-address.git
```
or
```
pip install git+https://github.com/soderstromkr/geo-address.git
```
Draft in progress: The spatial distribution of big science: A methodology for disaggregating and geocoding address fields (Working title)
