#!/usr/bin/env python3

# Copyright 2016, 2017, 2018, 2019 Fraunhofer FKIE
#
# This file is part of BREACH.
#
# BREACH is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BREACH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BREACH. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

setup(
    name="breach-framework",
    version="16.0.0",
    packages=find_packages("src", exclude=["*tests"]),
    package_dir={"": "src"},
    install_requires=[
        "colorama",
        "paramiko",
        "pyvmomi",
        "veryprettytable",
    ],
    entry_points={
        'console_scripts': [
            'attackconsole = attacks.attackconsole:main',
            'generateattackchains = attacks.generateattackchains:main',
            'vmconsole = vmcontrol.vmconsole:main'
        ]
    }
)
