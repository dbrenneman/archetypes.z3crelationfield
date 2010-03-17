from setuptools import setup, find_packages
import os

version = '0.1a1'

setup(name='archetypes.z3crelationfield',
      version=version,
      description="An archetypes field for using zc.relation relations",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='archetypes dexterity relations plone zc.relation',
      author='David Brenneman',
      author_email='db@davidbrenneman.com',
      url='http://bitbucket.org/dbrenneman/archetypes.z3crelationfield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['archetypes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
