#!/bin/env python
from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys

class osx_install_data(install_data):
    def finalize_options(self):
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}

packages, data_files = [], []

def fullsplit(path, result=None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

for module in ("beautiful_fields",):
    for dirpath, dirnames, filenames in os.walk(module):
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'): del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


import datetime, time
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
version = '0.1.0-' + st


setup(
    name='BeautifulFields',
    version=version,
    author='Excentrics LLC',
    author_email='info@excentrics.ru',
    packages=packages,
    data_files=data_files,
    cmdclass=cmdclasses,
    scripts=[],
    url='https://github.com/Excentrics/beautiful_fields.git',
    license='LICENSE.txt',
    description='Beautiful fields.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.5",
        "phonenumbers == 5.7b2",
    ],
)
