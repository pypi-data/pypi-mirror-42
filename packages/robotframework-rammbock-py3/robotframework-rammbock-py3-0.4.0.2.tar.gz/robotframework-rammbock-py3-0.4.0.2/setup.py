#!/usr/bin/env python
import setuptools
from distutils.core import setup
from os.path import join, dirname, abspath

CURDIR = dirname(abspath(__file__))
exec(compile(open(join(CURDIR, 'src', 'Rammbock', 'version.py')).read(), 'version.py', 'exec'))

setup(name         = 'robotframework-rammbock-py3',
      version      = VERSION,
      description  = 'Protocol testing library for Robot Framework',
      author       = 'Robot Framework Developers',
      author_email = 'robotframework-users@googlegroups.com',
      url          = 'http://github.com/robotframework/Rammbock/',
      package_dir  = {'' : 'src'},
      packages     = ['Rammbock', 'Rammbock.templates'],
      long_description = open(join(CURDIR, 'README.rst')).read()
      )
