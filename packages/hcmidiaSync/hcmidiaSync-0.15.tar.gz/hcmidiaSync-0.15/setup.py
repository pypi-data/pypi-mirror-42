# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='hcmidiaSync',
    version='0.15',
    url='https://temoque.com.br/',
    license='MIT License',
    author='Carla Dias',
    author_email='carladias@temoque.com.br',
    keywords='sync videos screenly',
    description=u'Sync videos',
    packages=['hcmidiaSync'],
    py_modules=["sync"],
    install_requires=['requests', 'simplejson'],
)