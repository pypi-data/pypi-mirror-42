#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Frootlab Developers
#
# This file is part of the Frootlab Shared Library, https://github.com/frootlab
#
#  The Frootlab Shared Library (flib) is free software: you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  The Frootlab Shared Library (flib) is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#  Public License for more details. You should have received a copy of the GNU
#  General Public License along with the frootlab shared library. If not, see
#  <http://www.gnu.org/licenses/>.
#
"""Setuptools based installation."""

__license__ = 'GPLv3'
__copyright__ = 'Copyright (c) 2019 Frootlab Developers'
__email__ = 'frootlab@gmail.com'
__docformat__ = 'google'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

import pathlib
import re
import setuptools

def install() -> None:
    """Setuptools based installation script."""

    # Get module variables from file 'flib/__init__.py'.
    text = pathlib.Path('./flib/__init__.py').read_text()
    rekey = "__([a-zA-Z][a-zA-Z0-9_]*)__"
    reval = r"['\"]([^'\"]*)['\"]"
    pattern = f"^[ ]*{rekey}[ ]*=[ ]*{reval}"
    pkg_vars = {}
    for mo in re.finditer(pattern, text, re.M):
        pkg_vars[str(mo.group(1))] = str(mo.group(2))

    # Install package
    setuptools.setup(
        name='flib',
        version=pkg_vars['version'],
        description='multi-purpose library',
        long_description=pathlib.Path('.', 'README.rst').read_text(),
        long_description_content_type='text/x-rst',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
    		'Programming Language :: Python :: 3.7',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules'],
        keywords=(
            'library '
            'shared-library '
            'python-library '),
        url='https://github.com/frootlab/flib',
        author=pkg_vars['author'],
        author_email=pkg_vars['email'],
        license=pkg_vars['license'],
        packages=['flib'],
        python_requires='>=3.7',
        install_requires=[
            'appdirs>=1.4.1',
            'pyparsing>=2.2'],
        extras_require={
            'numpy': ['numpy>=1.15']}
    )

if __name__ == '__main__':
    install()
