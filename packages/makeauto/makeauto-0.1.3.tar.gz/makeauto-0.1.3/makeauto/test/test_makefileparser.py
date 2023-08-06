# -*- coding: utf-8 -*-
__author__ = 'gchlebus'

import pytest
import os
from ..parser import MakefileParser

TEST_DIR = 'makeauto/test/makefiles'

def test_target_not_found():
  with pytest.raises(RuntimeError):
    parser = MakefileParser(_get_filepath('Makefile1'), 'asd')

def test_simple_makefile():
  parser = MakefileParser(_get_filepath('Makefile1'))
  assert parser.prerequisites == 'foo1 foo2'.split()

def test_expand_variables():
  parser = MakefileParser(_get_filepath('Makefile2'))
  assert parser.prerequisites == 'foo bar'.split()

def test_dependencies():
  parser = MakefileParser(_get_filepath('Makefile3'))
  assert parser.prerequisites == 'foo1 foo2 foo3'.split()

def test_variables():
  parser = MakefileParser(_get_filepath('test_variables'))
  variables = parser.variables
  assert variables['CC'] == 'g++'
  assert variables['CFLAGS'] == '-g -Wall -std=c++0x'

def _get_filepath(filename):
  return os.path.join(TEST_DIR, filename)

