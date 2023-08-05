# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rdftransformer',
    version='1.0.0',
    description='Annotation module for ALKIS Ontology',
    long_description=readme,
    author='Edward Dinu',
    author_email='edward.dinu@fokus.fraunhofer.com',
    url='https://gitlab.fokus.fraunhofer.de/Limbo/Annotation-tool',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
    'nose',
    'sphinx',
    'rdflib',
    'rdflib-jsonld',
    'lxml']
)