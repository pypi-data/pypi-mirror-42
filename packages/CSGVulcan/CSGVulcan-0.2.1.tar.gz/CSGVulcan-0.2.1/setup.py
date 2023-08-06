import os
import pathlib
import codecs
import re
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'README.md'), "r").read()


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='CSGVulcan',
    version=find_version("vulcan", "__init__.py"),
    description="A tiny library for describing data as a resource",
    packages=find_packages(exclude=("tests",)),
    long_description=README,
    long_description_content_type="text/markdown",
    author='CSG Data Science',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Framework :: Setuptools Plugin",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Utilities",
        "Development Status :: 1 - Planning",
    ],
    author_email='csgdatascience01@gmail.com',
    include_package_data=True,
    install_requires=["Flask", "Cython", "pandas"]
)
