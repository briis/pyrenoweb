"""Package Setup."""

import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrenoweb",
    version="2.0.12",
    author="briis",
    author_email="bjarne@briis.com",
    description="Gets garbage collection data from RenoWeb",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briis/pyrenoweb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
