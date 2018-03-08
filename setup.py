# -*- coding: utf-8 -*-

import subprocess

from setuptools import setup

subprocess.check_call('npm run build', shell=True)


def requirements():
    """
    Python requirements
    """
    with open('requirements/base.txt') as f:
        return f.read().splitlines()


REQUIRED_PYTHON = (2, 7)


setup(
    name='data-healer',
    description='A flasky app to categorize unlabeled datasets',
    url='https://github.com/txerpa/data-healer',
    author='Txerpa',
    maintainer='Alberto Pou Quirós',
    maintainer_email='alberto.pou@txerpa.com',
    version='1.0.0',
    license='MIT License',
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    packages=['healer'],
    install_requires=requirements(),
    scripts=[
        'bin/data-healer-run',
    ],
    keywords='dataset unlabeled categorize',
    classifiers=[
        'Framework :: Flask',
        'Framework :: Flask :: 0.12',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python'
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
)