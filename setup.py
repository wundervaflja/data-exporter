# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('src/cli.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="azimu-cli",
    packages=["src"],
    entry_points={
        "console_scripts": ['src = src.cli:main']
    },
    version=version,
    description="Python command line application for Azimu functionality",
    long_description=long_descr,
    author="Maksym Doroshenko",
    author_email="mdoroshenko@src.ai",
    url="https://azimu.ai/",
)
