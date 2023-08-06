"""For packaging and installation."""

from setuptools import setup


setup(
    name='afinn-gaming',
    packages=['afinn'],
    version='0.1dev',
    author='Lukas Corona',
    author_email='luk.corona@gmail.com',
    description='AFINN sentiment analysis for gaming',
    license='Apache License 2.0',
    keywords='sentiment analysis',
    url='https://github.com/korsmed/afinn',
    package_data={'afinn': ['data/*.txt', 'data/LICENSE']},
    long_description='',
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    )
