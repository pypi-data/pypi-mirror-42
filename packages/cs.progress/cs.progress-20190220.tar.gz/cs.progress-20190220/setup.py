#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.progress',
  description = 'A progress tracker with methods for throughput, ETA and update notification',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190220',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils', 'cs.seq', 'cs.units'],
  keywords = ['python2', 'python3'],
  long_description = 'A progress tracker with methods for throughput, ETA and update notification.\n\n## Class `CheckPoint`\n\nMRO: `builtins.tuple`  \nCheckPoint(time, position)\n\n## Class `Progress`\n\nA progress counter to track task completion with various utility methods.\n\n>>> P = Progress(name="example")\n>>> P                         #doctest: +ELLIPSIS\nProgress(name=\'example\',start=0,position=0,start_time=...,thoughput_window=None,total=None):[CheckPoint(time=..., position=0)]\n>>> P.advance(5)\n>>> P                         #doctest: +ELLIPSIS\nProgress(name=\'example\',start=0,position=5,start_time=...,thoughput_window=None,total=None):[CheckPoint(time=..., position=0), CheckPoint(time=..., position=5)]\n>>> P.total = 100\n>>> P                         #doctest: +ELLIPSIS\nProgress(name=\'example\',start=0,position=5,start_time=...,thoughput_window=None,total=100):[CheckPoint(time=..., position=0), CheckPoint(time=..., position=5)]\n\nA Progress instance has an attribute ``notify_update`` which\nis a set of callables. Whenever the position is updates, each\nof these will be called with the Progress instance and the\nlatest CheckPoint.\n\nProgress objects also make a small pretense of being an integer.\nThe expression `int(progress)` returns the current position,\nand += and -= adjust the position.\n\nThis is convenient for coding, but importantly it is also\nimportant for discretionary use of a Progress with some other\nobject.\nIf you want to make a lightweight Progress capable class\nyou can set a position attribute to an int\nand manipulate it carefully using += and -= entirely.\nIf you decide to incur the cost of maintaining a Progress object\nyou can slot it in:\n\n    # initial setup with just an int\n    my_thing.amount = 0\n\n    # later, or on some option, use a Progress instance\n    my_thing.amount = Progress(my_thing.amount)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.progress'],
)
