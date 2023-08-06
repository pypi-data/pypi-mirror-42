# -*- coding: utf-8 -*-

import os

currentdir = os.getcwd()

# Построение списка всех модулей проекта:
packages = []
for dirname, dirnames, filenames in os.walk(currentdir):
  if '__init__.py' in filenames:
    packages.append(dirname)

from distutils.core import setup
setup(
  name='dichotomy',
  packages=packages,
  version='0.1.0',
  description='Библиотека для работы с операциями деления надвое.',
  author='Аббас Гусенов',
  author_email='gusenov@live.ru',
  license='MIT',
  url='https://github.com/gusenov/dichotomy-py',
  download_url='https://github.com/gusenov/dichotomy-py/archive/v0.1.0.tar.gz',
  keywords='dichotomy division',
  classifiers=[
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Mathematics',
      'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
