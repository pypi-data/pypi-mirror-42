#!/usr/bin/env python
from distutils.core import setup

setup(
    name='TranscryptFrame',
    version='1.0',
    author='Andreas Bunkahle',
    author_email='abunkahle@t-online.de',
    description='Wrapper for transcrypt transpiler for most common html5 functions like cookies, dom, buttons, canvas',
    license='GNU GPL v3',
    py_modules=['TranscryptFrame'],
    python_requires='>=3',
    url='https://github.com/bunkahle/Transcrypt-Examples/blob/master/dom/TranscryptFrame.py',
    long_description=open('README.txt').read(),
    platforms = ['any'],
    install_requires=['transcrypt']
)
