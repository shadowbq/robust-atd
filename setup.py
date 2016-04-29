#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join, realpath
from setuptools import setup, find_packages


BASE_DIR = dirname(abspath(__file__))
INIT_FILE = join(BASE_DIR, 'ratd', '__init__.py')

def get_version():
    with open(INIT_FILE) as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                version = line.split()[-1].strip('"')
                return version
        raise AttributeError("Package does not have a __version__")

def install_requires():
    req_list = []
    with open('requirements.txt', 'rt') as f:
      for line in f:
        if line.strip().startswith('#'):
          continue
        if not line.strip():
          continue
        req_list.append(line.strip())
        print "Registering Requirement: " + line.strip()
    return req_list

py_maj, py_minor = sys.version_info[:2]

if py_maj != 2:
    raise Exception('robust-atd required Python 2.6/2.7')

if (py_maj, py_minor) < (2, 6):
    raise Exception('robust-atd requires Python 2.6/2.7')

fn_readme = join(BASE_DIR, "README.md")
with open(fn_readme) as f:
    readme = f.read()

extras_require = {
    'docs': [
        'Sphinx==1.2.1',
        'sphinxcontrib-napoleon==0.2.4',
    ],
    'test': [
        "nose==1.3.0",
        "tox==1.6.1"
    ],
}

setup(
    name='robust-atd',
    description='Manipulate Intel Security ATD appliance',
    author='Shadowbq',
    author_email='shadowbq@gmail.com',
    url='http://github.com/shadowbq/robust-atd',
    version=get_version(),
    packages=find_packages(),
    scripts=['ratd/scripts/robust.py','ratd/scripts/robust-reporter.py','ratd/scripts/robust-profiles.py','ratd/scripts/robust-watchdog.py','ratd/scripts/robust-search.py','ratd/scripts/robust-convict.py'],
    #install_requires=[line for line in open('./requirements.txt')],
    install_requires=install_requires(),
    extras_require=extras_require,
    long_description=readme,
    keywords="atd mcafee ioc"
)
