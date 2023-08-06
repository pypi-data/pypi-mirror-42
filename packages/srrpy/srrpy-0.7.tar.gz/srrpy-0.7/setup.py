#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup
import os

def import_require(require_file="requirements.txt"):
    if os.path.isfile(require_file):
        with open(require_file,"r") as f:
            require_list = f.read().split()
        return require_list
    return ['redis','Jinja2']

setup(
    name='srrpy',
    version='0.7',
    description='Simple Remote Run Python/Script',
    author='Heysion',
    author_email='heysion@priv.com',
    url = 'https://github.com/heysion/srrpy',
    py_modules=['srrpy'],
    install_requires=import_require(),
)
