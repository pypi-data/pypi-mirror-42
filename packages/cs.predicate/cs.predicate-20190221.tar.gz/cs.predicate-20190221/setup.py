#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.predicate',
  description = 'fnctions for expressing predicates',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190221',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils'],
  keywords = ['python2', 'python3'],
  long_description = 'Trite support for code predicates, presently just the context manager `post_condition`.\n\nInterested people should also see the `icontract` module.\n\n## Function `post_condition(*predicates)`\n\nContext manager to test post conditions.\n\nPredicates may either be a tuple of `(description,callable)`\nor a plain callable.\nFor the latter the description is taken from `callable.__doc__`\nor `str(callable)`.\nRaises `AssertionError` if any predicates are false.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.predicate'],
)
