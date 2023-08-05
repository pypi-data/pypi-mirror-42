#!/usr/bin/env python

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pysamloader",
    use_scm_version={"root": ".", "relative_to": __file__},
    author="Chintalagiri Shashank",
    author_email="shashank@chintal.in",
    description="python library for writing flash on "
                "Atmel's ARM chips via SAM-BA.",
    license="GPLv3+",
    keywords="utilities",
    url="https://github.com/chintal/pysamloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Embedded Systems",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Environment :: Console"
    ],
    install_requires=[
        'six',
        'appdirs',
        'xmodem',
        'pyserial',
        'progress',
        'bitstring',
        'cython',
        'kivy'
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    extras_require={
        'docs': ['sphinx',
                 'sphinx-argparse',
                 'sphinxcontrib-documentedlist',
                 'sphinx-rtd-theme'],
        'build': ['doit',
                  'setuptools_scm',
                  'wheel',
                  'twine',
                  'pygithub']
    },
    platforms='any',
    entry_points={
        'console_scripts': [
            'pysamloader=pysamloader.cli:main',
            'pysamloader-gui=pysamloader.gui.app:main',
        ],
    },
    include_package_data=True,
)
