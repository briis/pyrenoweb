from distutils.core import setup

setup(
    name="pyrenoweb",
    packages=["pyrenoweb"],
    version="1.0.0",
    license="MIT",
    description="Python Wrapper for RenoWeb Garbage System API",
    long_description=" ".join(
    ["A module to retrieve Garbage Collection data ",
    "for Danish Municipalities that are using RenoWeb."]),
    author="Bjarne Riis",
    author_email="bjarne@briis.com",
    url="https://github.com/briis/pyrenoweb",
    keywords=["Garbage", "RenoWeb", "Home Assistant", "Python"],
    install_requires=[
        "aiohttp",
        "asyncio",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
