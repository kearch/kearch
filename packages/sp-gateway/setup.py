# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "sp_gateway_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion==2.0.0",
    "swagger-ui-bundle==0.0.2",
    "python_dateutil==2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Kearch specialist search engine gateway API",
    author_email="",
    url="",
    keywords=["OpenAPI", "Kearch specialist search engine gateway API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['sp_gateway_server=sp_gateway_server.__main__:main']},
    long_description="""\
    Kearch specialist search engine gateway API
    """
)

