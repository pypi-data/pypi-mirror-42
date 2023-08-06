from setuptools import setup, find_packages

setup(
    name = 'nanopyfw',
    version = '0.0.3',
    url = 'https://github.com/AndreasAlbert/nanopyfw.git',
    author = 'Andreas Albert',
    author_email = 'andreas.albert@cern.ch',
    description = 'HEP Analysis on flat TTrees, like CMS NanoAOD',
    packages = find_packages(),    
    install_requires = ['numpy','root_numpy','numba', 'uproot'],
)