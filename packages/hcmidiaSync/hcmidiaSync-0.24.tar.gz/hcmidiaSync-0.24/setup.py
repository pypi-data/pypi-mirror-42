# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='hcmidiaSync',
    version='0.24',
    url='https://temoque.com.br/',
    license='MIT License',
    author='Carla Dias',
    author_email='carladias@temoque.com.br',
    keywords='sync videos screenly',
    description=u'Sync videos',
    packages=['hcmidiaSync'],
    #py_modules=["sync"],
    scripts=['bin/hcmidia-sync', 'bin/hcmidia-schedule'],
    install_requires=['requests', 'simplejson'],
)