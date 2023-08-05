# -*- coding: utf-8 -*-
"""setup.py"""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
]


long_description = (
    read_content("README.rst") +
    read_content(os.path.join("docs/source", "CHANGELOG.rst")))

requires = ['setuptools', 'attrs==18.1.0', 'cattrs==0.8.0', 'inflection==0.3.1']

extras_require = {
    'reST': ['Sphinx'],
}
if os.environ.get('READTHEDOCS', None):
    extras_require['reST'].append('recommonmark')

setup(name='jast',
      version='1.0.0-beta1',
      description='Construct javascript AST structures using python objects.',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      author='Kostas Papadimitriou',
      author_email='kpap@grnet.gr',
      url='https://github.com/grnet/jast',
      classifiers=classifiers,
      packages=['jast'],
      data_files=[],
      install_requires=requires,
      include_package_data=True,
      extras_require=extras_require,
      tests_require=['tox', 'sh==1.12.14', 'dictdiffer==0.7.1'],
      cmdclass={'test': Tox},)
