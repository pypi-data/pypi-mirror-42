#!/usr/bin/env python3
from setuptools import setup, find_packages

from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='minepkg',
    version="0.2",
    description='A package manager for minetest mods',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    url='https://gitlab.com/MartijnBraam/minepkg',
    license='MIT',
    install_requires=[
        'tqdm',
        'pyxdg',
        'requests'
    ],
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='minetest',
    packages=find_packages(exclude=['packages']),
    entry_points={
        'console_scripts': [
            'minepkg=minepkg.__init__:main',
        ],
    },
)
