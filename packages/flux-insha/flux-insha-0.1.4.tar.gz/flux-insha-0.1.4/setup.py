import ast
import re

from setuptools import setup, find_packages
from collections import OrderedDict

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flux/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))

with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name='flux-insha',
    version=version,
    url='https://github.com/insha/Flux',
    include_package_data=True,
    packages=find_packages(),
    description='A lightweight finite state machine',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='BSD-3-Clause',
    python_requires='>=3.6',
    platforms='any',
    project_urls=OrderedDict((
            ('Code', 'https://github.com/insha/Flux'),
            ('Issue tracker', 'https://github.com/insha/Flux/issues'),
    )),
    author='Farhan Ahmed',
    author_email='farhan@themacronaut.com',
    classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
    ],
)