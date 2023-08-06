# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='tablat',
    version='0.1.2',
    description='Print basic tables in python',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='salpreh',
    author_email='salva.perez46@gmail.com',
    url='https://github.com/salpreh/tablat',
    license='MIT License',
    packages=find_packages(exclude=('test', 'assets', 'venv', 'doc'))
)
