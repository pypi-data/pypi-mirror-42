import setuptools
import os, sys

sys.path.insert(0, './src')

from ksp import name, version, description

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author="Sumner Magruder",
    author_email="sumner.magruder@zmnh.uni-hamburg.de",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SumNeuron/{}".format(name),
    package_dir={'': 'src'},
    packages=
    setuptools.find_packages()
    # setuptools.find_namespace_packages(include=['cksp*', 'ksp*'])
    ,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
