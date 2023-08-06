from setuptools import setup
from layer7_utilities import const

with open("ReadMe.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name=const.__app_name__,
    version=const.__version__,
    description=const.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://Layer7.Solutions",
    author=const.__author__,
    author_email="Mike@Layer7.Solutions",
    license="MIT",
    packages=[
        "layer7_utilities",
        "layer7_utilities.logger",
        "layer7_utilities.exceptions",
        "layer7_utilities.database",
        "layer7_utilities.auth",
    ],
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
