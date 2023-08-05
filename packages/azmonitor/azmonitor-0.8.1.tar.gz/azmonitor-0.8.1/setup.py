"""azmonitor setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='azmonitor',
    version='0.8.1',
    description='It is a helper tool for azure monitor. It is not official.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KentaroAOKI/azmonitor',
    author='Kentaro Aoki',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='azmonitor',
    packages=find_packages(),
    install_requires=['requests'],
)