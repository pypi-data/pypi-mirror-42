#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='pygments-arm',
    version='0.7.5',
    description='Pygments lexer for ARM.',
    long_description=open('README.rst').read(),
    keywords='pygments arm assembler lexer',
    license='Apache 2',

    author='Jacques Supcik',
    author_email='jacques.supcik@hefr.ch',

    url='https://github.com/heia-fr/pygments-arm',

    packages=find_packages(),
    install_requires=['pygments >= 1.4'],

    entry_points='''[pygments.lexers]
                    armlexer=pygments_arm:ArmLexer''',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
