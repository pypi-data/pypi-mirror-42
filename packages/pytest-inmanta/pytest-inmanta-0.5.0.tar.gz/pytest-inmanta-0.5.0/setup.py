# Based on setup.py from pytest-tornado
import os
import io
from setuptools import setup, find_packages


cwd = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(cwd, 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()


setup(
    name='pytest-inmanta',
    version='0.5.0',
    description=('A py.test plugin providing fixtures to simplify inmanta modules testing.'),
    long_description=long_description,
    url='https://github.com/inmanta/pytest-inmanta',
    author='Inmanta NV',
    author_email='code@inmanta.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
    ],
    keywords=('pytest py.test inmanta testing unit tests plugin'),
    packages=find_packages(),
    install_requires=['pytest', 'inmanta'],
    entry_points={
        'pytest11': ['inmanta = pytest_inmanta.plugin'],
    },
)
