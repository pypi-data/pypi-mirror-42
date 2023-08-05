#!/usr/bin/env python
from setuptools import setup, find_packages

desc = ''
with open('README.rst') as f:
    desc = f.read()

setup(
    name='openapi-toolkit',
    version='0.1.2',
    description=('Collection of utilities for OpenAPIs'),
    long_description=desc,
    url='https://github.com/jmvrbanac/openapi-toolkit',
    author='John Vrbanac',
    author_email='john.vrbanac@linux.com',
    license='Apache v2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='openapi toolkit resolver validator',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=[
        'alchemize',
        'jsonschema[format]',
        'mako',
        'ruamel.yaml',
    ],
    data_files=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'openapi-toolkit=openapi_toolkit.cli:app',
        ],
    },
)
