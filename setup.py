#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import sys
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

NAME = "zmapio"
DESCRIPTION = "Python library for reading and writing map gridded data using ZMAP Plus ASCII Grid format"
URL = "https://github.com/abduhbm/zmapio"
AUTHOR = "Abdulelah Bin Mahfoodh"

REQUIRED = ["numpy"]
EXTRA_REQS = ["pandas", "matplotlib"]
TEST_REQS = ["pytest"]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

about = {}
with open(os.path.join(here, NAME, "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=REQUIRED,
    extras_require={"all": EXTRA_REQS, "test": (EXTRA_REQS, TEST_REQS)},
    tests_require=TEST_REQS,
    license="MIT",
    keywords="ZMAP Plus Grid format",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
