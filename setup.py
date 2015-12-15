#!/usr/bin/env python

import re,glob
from distutils.core import setup
from setuptools import find_packages

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


setup(
    name                    =   'ccuapi',
    version                 =   '1.2.1',
    description             =   'Python wrapper around Akamai\'s Content Control Utility API',
    author                  =   'David Petzel',
    author_email            =   'david.petzel@disney.com',
    url                     =   'https://github.com/dpetzel/python-ccuapi',
    packages                =   find_packages(),
    long_description        =   open('README.rst', 'r').read(),
    license                 =   'BSD 3 Clause License',
    zip_safe                =   False,
    include_package_data    =   True,
    install_requires        =   parse_requirements('requirements.txt'),
    dependency_links        =   parse_dependency_links('requirements.txt'),
    entry_points            =   {
        'console_scripts':  [
            'ccu_purge = ccuapi.ccu_purge:main',
        ]
    }
)
