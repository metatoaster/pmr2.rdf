from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='pmr2.rdf',
      version=version,
      description="RDF handling for PMR2",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Tommy Yu',
      author_email='tommy.yu@auckland.ac.nz',
      url='http://www.bioeng.auckland.ac.nz/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pmr2'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'lxml>2.0.5',
          'rdflib>=4.2',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
