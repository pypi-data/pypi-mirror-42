from setuptools import setup, find_packages

def readme():
	with open('./README.md') as f:
		return f.read()

setup(
	name='slytherin',
	version='0.2',
	description='Useful but lonely functions and classes',
	long_description=readme(),
	url='https://github.com/idin/slytherin',
	author='Idin',
	author_email='py@idin.ca',
	license='MIT',
	packages=find_packages(exclude=("jupyter_tests", ".idea", ".git")),
	install_requires=['pandas', 'geopy', 'jellyfish'],
	python_requires='~=3.6',
	zip_safe=False
)