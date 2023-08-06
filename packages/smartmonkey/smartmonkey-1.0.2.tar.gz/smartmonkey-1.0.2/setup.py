import sys
from os import path

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

if sys.version_info <= (2, 4):
    error = 'Requires Python Version 2.5 or above... Exiting.'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


requirements = [
    'requests>=2.11.1,<3.0',
]

setup(
    name='smartmonkey',
    version='1.0.2',
    description='Python client for Smartmonkey API Web Services',
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=[],
    url='https://github.com/smartmonkeyio/smartmonkey-services-python',
    packages=['smartmonkey'],
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    setup_requires=requirements,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
