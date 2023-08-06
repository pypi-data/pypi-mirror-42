from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ContinentInfo',
	version='1.2',
	description = 'Get the name of the continent in which a country is located in.',
	long_description=long_description,
    	long_description_content_type="text/markdown",
	packages=['ContinentInfo'],
	author = 'Rohit Swami',
	author_email = 'rowhitswami1@gmail.com',
	zip_safe=False)
