#!/usr/bin/env python

import subprocess
import shlex
from setuptools import setup

version = '0.4.1.0'

try:
    hash = (
        subprocess
        .check_output(shlex.split('git rev-parse --short HEAD'))
        .rstrip()
        .decode('ASCII')
    )
    commit = (
        subprocess
        .check_output(shlex.split('git rev-list --count HEAD'))
        .rstrip()
        .decode('ASCII')
    )
except:
    pass
else:
    version = '{}.dev{}+{}'.format(version, commit, hash)


setup(
    name='x-highlight-region',
    version=version,
    description="Dims everything but a selected region of the screen.",
    author="Sebastian Reuße",
    author_email='seb@wirrsal.net',
    url='https://github.com/eigengrau/x-highlight-region',
    packages=[
        'xhighlight',
        'xhighlight.server',
        'xhighlight.client'
    ],
    package_dir={'': 'src'},
    install_requires=[
        'pygobject >= 3.18, < 3.21',
        'python3-keybinder >= 1.1, < 1.2'
    ],
    license="GPL3",
    entry_points={
        'console_scripts': [
            'xhighlight-server = xhighlight.server.cli:console_entry',
            'xhighlight = xhighlight.client.cli:console_entry'
        ],
    }
)
