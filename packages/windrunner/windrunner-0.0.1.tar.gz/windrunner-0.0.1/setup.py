#!/usr/bin/env python

import io
import glob
import os

import setuptools


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ).read()


setuptools.setup(
    name="windrunner",
    version="0.0.1",
    license="MIT License",
    description="Run like the wind",
    long_description=read("README.md"),
    author="Foad Green",
    author_email="foadgreen@gmail.com",
    url="https://github.com/foadgr/windrunner",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob.glob("src/*.py")
    ],
    include_package_data=True,
    zip_safe=False,
    dependency_links=['https://github.com/foadgr/strava_v3/tarball/master#egg=package-1.0'],
    
    entry_points={
        "console_scripts": []
    },
    scripts=glob.glob("scripts/*"),
)