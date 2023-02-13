from setuptools import setup

setup(
	name='geo-address', 
	version="0.1",
	author= 'Kristofer R. Söderström',
	description='Companion package for article "ARTICLE_NAME" published \
	in "JOURNAL NAME", LICENSE_TYPE, CITATION', #ADD MORE INFO HERE,
	install_requires=['re', 'pandas', 'numpy', 'tqdm', 'geopy'],
	packages=["geo-address"]
 	)
