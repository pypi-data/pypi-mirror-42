# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('chipmunk/chipmunk.py').read(),
    re.M
    ).group(1) 
 
with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "cmdline-chipmunk",
    packages = ["chipmunk"],
    entry_points = {
        "console_scripts": ['chipmunk = chipmunk.chipmunk:main']
        },
    version = version,
    description = "Python command line application bare bones template.",
    long_description = long_descr,
    author = "Xiangyu_Gao",
    author_email = "xg673@nyu.edu",
    url = "http://gehrcke.de/2014/02/distributing-a-python-command-line-application",
    )
