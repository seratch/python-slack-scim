#!/usr/bin/env python
from glob import glob
from os.path import splitext, basename

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slack-scim",
    version="1.0.1",
    author="Kazuhiro Sera",
    author_email="seratch@gmail.com",
    description="Slack SCIM API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seratch/pyton-slack-scim",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    setup_requires=["pytest-runner==5.2"],
    tests_require=["pytest==3.8.2"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
