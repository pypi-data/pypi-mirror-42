# -*- coding: utf-8 -*-
from setuptools import setup
import codecs

setup(
    name='selecta',
    version='0.0.16',
    author='Thomas Schüßler',
    author_email='vindolin@gmail.com',
    packages=['selecta'],
    scripts=['bin/selecta', 'bin/selecta_install_bash'],
    url='https://github.com/vindolin/selecta',
    license='MIT',
    description='Interactively select an entry from your bash/zsh history.',
    long_description=codecs.open('README.rst', 'r', 'utf-8').read(),
    install_requires=['urwid >= 1.3.1'],
    include_package_data=True,
    keywords=['bash', 'zsh', 'curses', 'history'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console :: Curses',
        'Programming Language :: Python :: 3',
    ],
)
