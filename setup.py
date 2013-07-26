# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import subprocess
from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import swiftsc

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Environment :: OpenStack",
]

long_description = \
        open(os.path.join("docs","README.rst")).read() + \
        open(os.path.join("docs","TODO.rst")).read() + \
        open(os.path.join("docs","HISTORY.rst")).read()


def is_debian_system():
    fnull = open(os.devnull, 'w')
    if (subprocess.call(['which', 'apt-get'], stdout=fnull) == 0 and
        subprocess.call(['apt-cache', 'show', 'python-magic'], stdout=fnull) == 0):
        fnull.close()
        return True
    else:
        fnull.close()
        return False

requires = ['setuptools', 'requests']
if not is_debian_system():
    requires.append('python-magic')


setup(name='swiftsc',
      version='0.4',
      description='Simple client library of OpenStack Swift',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/swiftsc',
      license=' GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=requires,
      extras_require=dict(
        test=[
            'pytest',
            'pep8',
            'mock',
            ],
        ),
      test_suite='tests',
      tests_require=['pytest','pep8', 'mock'],
)
