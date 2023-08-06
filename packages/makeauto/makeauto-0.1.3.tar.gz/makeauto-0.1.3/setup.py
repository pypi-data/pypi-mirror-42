# -*- coding: utf-8 -*-

__author__ = 'gchlebus'

from setuptools import setup, find_packages

setup(
  name='makeauto',
  version='0.1.3',
  author='Grzegorz Chlebus',
  url='https://github.com/gchlebus/makeauto',
  license='BSD 3-Clause',
  author_email='gchlebus@gmail.com',
  description=('Run make automatically on sources change.'),
  long_description='See project homepage for more information.',
  keywords='make makefile',
  packages=find_packages(exclude=['test']),
  install_requires=['click', 'watchdog'],
  entry_points='''
    [console_scripts]
    makeauto=makeauto.cli:cli
  ''',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Topic :: Utilities',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License'
  ]
)
