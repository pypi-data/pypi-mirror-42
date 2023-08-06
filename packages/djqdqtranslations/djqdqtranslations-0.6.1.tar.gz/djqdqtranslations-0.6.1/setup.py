#!/usr/bin/env python

import os
import sys

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


packages = [
    'djqdqtranslations',
    'djqdqtranslations.management',
    'djqdqtranslations.management.commands',
    'djqdqtranslations.templatetags'
]

install_reqs = parse_requirements("requirements.txt", session=False)
requires = [str(ir.req) for ir in install_reqs]

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='djqdqtranslations',
    version="0.6.1",
    description='Python django commands for crowding translations management',
    long_description=readme,
    author="QdqMedia Web Team",
    author_email="equipo_web@qdqmedia.com",
    url='https://gitlab.qdqmedia.com/shared-projects/djqdqtranslations.git',
    packages=packages,
    package_data={'': ['requirements.txt']},
    package_dir={'djqdqtranslations': 'djqdqtranslations'},
    include_package_data=True,
    install_requires=requires,
    license='MIT License',
    zip_safe=False,
    download_url='https://gitlab.qdqmedia.com/shared-projects/djqdqtranslations/repository/archive.tar.bz2',
    keywords=['qdqmedia', 'translation', 'django'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
