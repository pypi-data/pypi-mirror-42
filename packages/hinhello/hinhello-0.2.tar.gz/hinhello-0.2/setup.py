#!/usr/bin/env python
"""
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md',"r") as readme_file:
    readme = readme_file.read()

setup(
    name='helo',
    version='0.1',
    description="writes helo and hi with speciel functions",
    long_description=readme,# + '\n\n' + history
    author="Ceyhun",
    author_email='ceyhun@gmail.com',
    url='https://github.com/Ceyhunyc/helo',
    packages=[
        'helo',
    ],
    package_dir={'helo': 'helo'},
    license="MIT license",
    zip_safe=False,
    keywords='helo',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
"""
from setuptools import setup

setup(name='hinhello',
      version='0.2',
      description='You can write hello and hi with specific functions',
      url='https://github.com/Ceyhunyc/hinhello',
      author='Ceyhun',
      author_email='coskunyceyhun@gmail.com',
      license='MIT',
      packages=['hinhello'],
      entry_points={'console_scripts': ['hiorhello=hinhello.chs:main']},
      zip_safe=False
      )
