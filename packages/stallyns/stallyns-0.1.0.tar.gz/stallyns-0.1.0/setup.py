# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='stallyns',
    version='0.1.0',
    description='Webapp for user switching with RetroPie and EmulationStation',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Doug Steigerwald',
    author_email='steigerwald.doug@gmail.com',
    url='https://github.com/dlawregiets/stallyns',
    license=license,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
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
