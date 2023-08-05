#!/usr/bin/env python

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="sphinx-runner",
        author="Jakob Jul Elben",
        author_email="elbenjakobjul@gmail.com",
        version="0.1.0",
        description="A sphinx-runner for setuptools",
        py_modules=['sphinx_runner'],
        install_requires=['sphinx'],
    )
