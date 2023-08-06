# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='stallyns',
    version='0.1.2',
    description='Webapp for user switching with RetroPie and EmulationStation',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Doug Steigerwald',
    author_email='steigerwald.doug@gmail.com',
    url='https://github.com/dlawregiets/stallyns',
    license="Apache License 2.0",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        'console_scripts': [
            'stallyns = stallyns.stallyns:main'
        ]
    },
    install_requires=['flask~=1.0'],
    package_data={
        'stallyns':['templates/*.html']
    }
)
