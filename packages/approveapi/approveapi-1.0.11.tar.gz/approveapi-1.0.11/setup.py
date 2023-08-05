# coding: utf-8

"""
    ApproveAPI

    The simple API to request a user's approval on anything via email + sms.

    Contact: hello@approveapi.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "approveapi"
VERSION = "1.0.11"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["approveapi-swagger"]

setup(
    name=NAME,
    version=VERSION,
    description="ApproveAPI",
    author_email="hello@approveapi.com",
    url="https://approveapi.com",
    keywords=[],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    The simple API to request a user&#39;s approval on anything via email + sms.
    """
)
