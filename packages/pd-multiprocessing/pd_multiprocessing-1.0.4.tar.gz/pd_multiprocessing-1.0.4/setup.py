"""
setup.py of this project
"""
from setuptools import setup


CLASSIFIERS = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

setup(

    install_requires=[
        'pandas>=0.22.0',
        'pytest>=3.4.1'
    ],
)
