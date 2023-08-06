import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="sb_dev_tools",
    version="0.0.2",
    author="John Aven",
    author_email="john.aven.phd@gmail.com",
    description=("The sb_dev_tools package is a set of basic utility tools used within the snoodleboot libraries and "
                 "packages. They are designed with SOLID principles in mind and are used to speed up the development "
                 "process and enable configuration-as-code (CaC)."),
    license="Apache version 2.0",
    keywords="polymorphic factory, factory, utities",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['sb_dev_tools', 'test'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License  ",
    ],
)
