"""Pip installation script."""

from setuptools import find_packages, setup

setup(
    name='bravais',
    description=('A simple package for representing Bravais lattices. '
                 'Primarily useful to check the passed parameters represent a '
                 'valid Bravais lattice.'),
    version='0.1.0',
    author='Adam J. Plowman',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
