#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import sys
import re
from shutil import rmtree
from os import path
from collections import OrderedDict

from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

with open(path.join(here, 'dbdoc/__init__.py'), 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
with open(path.join(here, 'README.rst'), encoding='utf8') as f:
    long_description = f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


setup(
    name='DBDoc',
    version=version,
    url='https://github.com/faeli/dbdoc',
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/faeli/dbdoc/wiki'),
        ('Code', 'https://github.com/faeli/dbdoc'),
        ('Issue tracker', 'https://github.com/faeli/dbdoc/issues'),
    )),
    license='Apache License 2.0',
    author='Feng pengbin',
    author_email='fengpengbin@live.cn',
    maintainer='Feng pengbin',
    maintainer_email='fengpengbin@live.cn',
    description='A simple database doc with one html file',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=['dbdoc'],
    include_package_data=True,
    zip_safe=False,
    data_files=['dbdoc/style.css'],
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=[
        'SQLAlchemy>=1.2'
    ],
    entry_points={
        'console_scripts': [
            'dbdoc = dbdoc.cli:main',
        ],
    },
    cmdclass={
        'upload': UploadCommand,
    }
)
