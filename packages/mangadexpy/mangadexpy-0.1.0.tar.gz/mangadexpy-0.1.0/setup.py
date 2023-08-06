import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name='mangadexpy',
	version='0.1.0',
	author='thatonerandomdev',
	author_email='no@u.net',
	description='Acts as a wrapper between you and mangadex\'s API, to allow easy integration.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://repl.it/@thatonedev/mangadexpy',
	packages=setuptools.find_packages(),
	install_requires='requests-html',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)