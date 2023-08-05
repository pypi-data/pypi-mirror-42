import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mechachainsaw',
    author='The Fuel Rats Mischief',
    author_email='shatt@fuelrats.com',
    description="An easy to use logging wrapper.",
    url='https://github.com/FuelRats/mechachainsaw',
    version='1.21',
    packages=['mechachainsaw', ],
    license='BSD-3-Clause',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['coloredlogs'],
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: OS Independent",
                 "Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers"],
)
