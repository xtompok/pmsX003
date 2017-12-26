from setuptools import setup, find_packages

setup(
    name = 'pmsX003',
    version = '0.1',
    author = 'Tomas \'Jethro\' Pokorny',
    author_email = 'xtompokAT_MARKgmailDOTcom',
    packages = find_packages(),
    license = 'LICENSE.txt',
    description = 'Reads particle concetration from a PMS-x003 sensor.',
    long_description = open('README.txt').read(),
    keywords = "PM PM2.5 PM10 PMS-5003 PMS-7003 serial",
    url = "",
    install_requires = "pyserial>=3.4",
)
