# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

name = 'xml_marshaller'
version = '1.0.2'

def read(name):
    return open(name).read()

long_description=(
        read('README.txt')
        + '\n' +
        read('CHANGES.rst')
    )

setup(name=name,
      version=version,
      description="Converting Python objects to XML and back again.",
      long_description=long_description,
      classifiers=['Development Status :: 4 - Beta',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: Python License (CNRI Python License)',
             'Operating System :: OS Independent',
             'Topic :: Text Processing :: Markup :: XML'], 
      keywords='XML marshaller',
      author='XML-SIG',
      author_email='xml-sig@python.org',
      maintainer='Nicolas Delaby',
      maintainer_email='nicolas@nexedi.com',
      url='http://www.python.org/community/sigs/current/xml-sig/',
      license='Python License (CNRI Python License)',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['lxml','six'],
      test_suite='xml_marshaller',
      )
