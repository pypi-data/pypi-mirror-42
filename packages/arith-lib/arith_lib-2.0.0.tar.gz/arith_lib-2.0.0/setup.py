# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages 

with open("README.md", "r") as fh:
    long_description = fh.read()

keywords=("gcd lcm bezout pseudo prime miller rabin factorization "
          "divisor chinese remainder phi euler totient moebius base "
          "frobenius isqrt"
          )

import arith_lib

setup(
     name='arith_lib',
     version=arith_lib.__version__,
     author="JM Allard",
     author_email="jma214@gmail.com",
     description="A set of functions for miscellaneous arithmetic calculation",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url='',
     keywords=keywords,
     packages=find_packages(),
     classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
