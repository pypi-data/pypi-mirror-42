# -*- coding: utf-8 -*-
from codecs import open
from setuptools import setup, find_packages

with open('kaya/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if '__version__' in line:
            version = line.split("'")[1]

setup(
    name='kaya',
    version=version,
    description="Testing framework inspired by jest",
    install_requires=[
    ],
    long_description="",
    url='https://github.com/JeongUkJae/kaya',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning'
    ],
)
