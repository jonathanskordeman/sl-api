import sl
from setuptools import setup


setup(
    name='sl-api',
    version=sl.__version__,
    description='SL API',
    long_description='A python wrapper for Stockholms Lokaltrafik API',
    packages=['trafiklab'],
    url='https://github.com/jonathanskordeman/trafiklab',
    license='MIT',
    author='Jonathan Skordeman',
    author_email='jonathan@skordeman.se',
    keywords='sl stockholm trafiklab',
    install_requires=['requests>=2.11.1'],
    tests_require=['pytest', 'requests-mock'],
    setup_requires=['pytest-runner'],
    extras_require={
        'testing': ['pytest','requests-mock']
    }
)
