#!/usr/bin/env python3
import setuptools

from fich import APP_VERSION


with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'fich',
	version = APP_VERSION,
	author = 'grolip',
	url = 'https://github.com/grolip/fich',
	project_urls={
		'Source': 'https://github.com/grolip/fich'},
	description = 'Suppression sécurisée et hashage.',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
		'Environment :: Console',
		'Natural Language :: French',
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT License',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: System Administrators',
		'Operating System :: POSIX :: Linux',
		'Topic :: System :: Filesystems',
		'Topic :: Utilities',
	],
	entry_points={
		'console_scripts': [
			'fich = fich.cli:main',
		],
	},
)
