#!/usr/bin/env python
# coding: utf-8
"""
    Python boilerplate short description
    Copyright (C) 2019  Adrien Oliva

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from setuptools import setup


version = "0.0.3"

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='Playschool Python',
    version=version,
    description='Python boilerplate short description',
    long_description=readme,
    author='Adrien Oliva',
    author_email='olivaa@yapbreak.fr',
    url='https://gitlab.yapbreak.fr/olivaa/playschool_python',
    packages=[
        'playschool_python',
    ],
    package_dir={'playschool_python': 'playschool_python'},
    entry_points={
        'console_scripts': [
            'playschool_python = playschool_python.__main__:main',
        ]
    },
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=requirements,
    license='GNU/GPL v3',
    zip_safe=False,
    classifiers=[
        # Look at https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=(
        'playschool_python'
    ),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_requires=test_requirements,
)
