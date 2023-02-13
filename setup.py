import setuptools

descr = '''
Dissagregates author addresses from Web of Science data.
Calculates author to address multiplier.
'''
if __name__ == "__main__":
	setuptools.setup(
		name='geo_address', 
		version="0.1",
		author= 'Kristofer R. Söderström',
		description='Companion package for article "ARTICLE_NAME" published \
		in "JOURNAL NAME", LICENSE_TYPE, CITATION', #ADD MORE INFO HERE,
		install_requires=['re', 'pandas', 'numpy', 'tqdm', 'geopy', 'pickle'],
		packages=["geo_address"]
 	)
