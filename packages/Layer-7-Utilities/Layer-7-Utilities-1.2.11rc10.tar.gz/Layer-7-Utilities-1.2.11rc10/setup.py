from setuptools import setup

__app_name__ = "Layer-7-Utilities"
__description__ = "This is a set of utilities used by https://Layer7.Solutions for the software tools we create. It includes a logger with default configuration information we setup as well as an oAuth wrapper to be able to pull login information from a custom database."
__author__ = "Layer 7 Solutions (Mike Wohlrab)"
__version__ = "1.2.11rc10"

with open("ReadMe.md", "r") as fh:
    long_description = fh.read()

setup(
    name=__app_name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://Layer7.Solutions",
    author=__author__,
    author_email="Mike@Layer7.Solutions",
    license="MIT",
    packages=[
        "layer7_utilities",
        "layer7_utilities.logger",
        "layer7_utilities.exceptions",
        "layer7_utilities.database",
        "layer7_utilities.auth",
    ],
    install_requires=["psycopg2>=2.7.7", "sentry-sdk>=0.7.0", "praw>=6.1.1"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
