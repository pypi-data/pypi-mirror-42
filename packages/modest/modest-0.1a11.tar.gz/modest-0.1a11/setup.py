import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
    
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='modest',
    version='0.1.a11',
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        'Pint',
        'numpy',
        'matplotlib',
        'skyfield',
        'scipy',
        'pyquaternion',
        'requests',
        'pandas',
        'astropy',
        'PyYAML',
        'datetime',
    ],
    description='A modular estimation library',
    long_description=read('README.md'),
    url='https://modular-estimator.readthedocs.io/en/latest/index.html',
    license='MIT',
    author='Joel Runnels',
    author_email='runne010@umn.edu'
)
