from setuptools import setup, find_packages
import os


def readme():
	with open('./README.md') as f:
		return f.read()


data_dir = os.path.join('chemistry', 'data_files')

data_files = [
	(d, [os.path.join(d,f) for f in files])
	for d, folders, files in os.walk(data_dir)
]


setup(
	name='chemistry',
	version='0.0',
	license='MIT',

	url='https://github.com/idin/chemistry',
	author='Idin',
	author_email='py@idin.ca',

	description='',
	long_description=readme(),
	long_description_content_type='text/markdown',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],

	data_files=data_files,
	include_package_data=True,

	packages=find_packages(exclude=["jupyter_tests", ".idea", ".git"]),
	install_requires=['pandas'],
	python_requires='~=3.6',
	zip_safe=False
)