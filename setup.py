#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='gitalert',
      description='',
      author='Jacinto Shy, Jr.',
      author_email='jacinto.m.shy@gmail.com',
      license='BSD',
      packages=['gitalert'],
      entry_points={
          'console_scripts' : [
              'gitalert = gitalert.gitalert:main'
          ]
      },
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
      ]
)
