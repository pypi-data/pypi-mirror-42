from setuptools import setup, find_packages

setup(
    name = 'osimis_broker_helpers',
    packages = find_packages(),
    version='0.1.9',  # always keep all zeroes version, it's updated by the CI script
    setup_requires=[],
    description = 'A simple library to make queueing/retry easy.',
    author = 'Benoit Crickboom',
    author_email = 'bc@osimis.io',
    url = 'https://bitbucket.org/osimis/python-osimis-broker-helpers',
    keywords = ['Helpers', 'Broker', 'Rabbitmq', 'Queue'],
    classifiers = [],
    install_requires = [
        'pika==0.13.0',
        'docker==3.7.0',
        'osimis_logging==0.1.0'
    ],
)
