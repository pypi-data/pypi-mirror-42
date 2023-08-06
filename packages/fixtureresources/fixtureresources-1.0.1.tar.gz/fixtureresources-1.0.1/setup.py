import os
import imp
from setuptools import setup, find_packages

__copyright__ = 'Copyright (C) 2019, Nokia'

VERSIONFILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'src', 'fixtureresources', '_version.py')


def get_version():
    return imp.load_source('_version', VERSIONFILE).get_version()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='fixtureresources',
    version=get_version(),
    author='Petri Huovinen',
    author_email='petri.huovinen@nokia.com',
    description='Commonly useful pytest fixtures and mocks.',
    install_requires=['mock', 'pytest'],
    long_description=read('README.rst'),
    license='BSD 3-Clause',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development'],
    keywords='pytest',
    url='https://github.com/nokia/fixtureresources',
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
