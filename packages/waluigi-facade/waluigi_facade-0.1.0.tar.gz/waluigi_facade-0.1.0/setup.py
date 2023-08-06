# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

setup(
	name="waluigi_facade",
	author="Daniel Domínguez",
	author_email="daniel.dominguez@imdea.org",
	url="https://github.com/0xddom/waluigi",
	version="0.1.0",
	packages=find_packages(),
	include_package_data=True,
	install_requires=[
		'luigi'
	],
	license="LICENSE",
	description="The python part of the waluigi library"
)