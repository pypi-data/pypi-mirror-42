# -*- coding: utf-8 -*-

import os


from distutils.core import setup
setup(
  #name='distrib',  # testpypi
  name='distrib_val',  # pypi

  packages=['distrib'],
  version='0.1.0',
  description='Распределитель числового значения.',
  author='Аббас Гусенов',
  author_email='gusenov@live.ru',
  license='MIT',
  url='https://github.com/gusenov/distributor-of-numerical-value-py',
  download_url='https://github.com/gusenov/distributor-of-numerical-value-py/archive/v0.1.0.tar.gz',
  keywords='division',
  classifiers=[
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Mathematics',
      'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
