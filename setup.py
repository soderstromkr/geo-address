from setuptools import setup, find_packages

setup(
	name='geo-address', 
	version="0.1",
	author= 'Kristofer R. Söderström',
	description='Companion package for article "ARTICLE_NAME" published \
	in "JOURNAL NAME", LICENSE_TYPE, CITATION', #ADD MORE INFO HERE,
	install_requires=['pandas', 'numpy', 'tqdm', 'geopy'],
	packages=find_packages(exclude=['test'])
 	)
