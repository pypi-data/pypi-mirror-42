#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

def get_version(package):
    """
    Return package version as listed in `__version__` in `__version__.py`.
    """
    with open(os.path.join(package, "__version__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="wg_countdown_timer",
    python_requires=">=3.6",
    version=get_version("wg_countdown_timer"),
    url="https://gitlab.com/harry.sky.vortex/wgct",
    license="Apache License 2.0",
    description="Worldman Games Countdown Timer",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Igor Nehoroshev",
    author_email="mail@neigor.me",
    packages=get_packages("wg_countdown_timer"),
    data_files=[("", ["LICENSE"])],
    include_package_data=True,
    install_requires=["starlette", "apscheduler", "aiofiles"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)