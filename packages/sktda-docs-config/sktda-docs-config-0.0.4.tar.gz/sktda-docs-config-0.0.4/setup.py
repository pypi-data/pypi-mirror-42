#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(name='sktda-docs-config',
      version='0.0.4',
      description='Custom configuration for the Scikit-TDA documentation',
      long_description=long_description,
      long_description_content_type="text/markdown",	
      author='Nathaniel Saul',
      author_email='nat@riverasaul.com',
      url='https://github.com/scikit-tda/sktda-docs-config',
      license='MIT',
      packages=['sktda_docs_config'],
      include_package_data=True,
      install_requires=[
        'sphinx',
        'ipython',
        'nbsphinx',
        'sphinxcontrib-fulltoc'
      ],
      python_requires='>3.3'
)
