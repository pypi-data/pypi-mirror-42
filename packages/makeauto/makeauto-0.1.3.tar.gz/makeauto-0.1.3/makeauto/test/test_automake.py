# -*- coding: utf-8 -*-
__author__ = 'gchlebus'

import pytest
import os
import imp
import contextlib
from threading import Thread
import time
from .. import makeauto

TMP_FILENAME = 'tmp_file'
TEST_MAKEFILES_DIR = 'makeauto/test/makefiles'

@contextlib.contextmanager
def changedir(dirpath):
  cwd = os.getcwd()
  os.chdir(dirpath)
  try:
    yield
  finally:
    os.chdir(cwd)

@contextlib.contextmanager
def cleanupfiles(*filenames):
  try:
    yield
  finally:
    for f in filenames:
      if os.path.exists(f):
        os.remove(f)


def test_simplerun():
  makeauto.STOP_AFTER_NSEC = 1
  with changedir(TEST_MAKEFILES_DIR), cleanupfiles(TMP_FILENAME):
    makeauto.makeauto(test_simplerun.__name__, debug=True)
    assert os.path.exists(TMP_FILENAME)

def test_makefilechange():
  makeauto.STOP_AFTER_NSEC = 2
  with changedir(TEST_MAKEFILES_DIR), cleanupfiles(TMP_FILENAME):
    t = Thread(target=makeauto.makeauto, args=(test_makefilechange.__name__,))
    t.start()
    time.sleep(1)
    touch_file(test_makefilechange.__name__)
    t.join()
    with open(TMP_FILENAME, 'r') as f:
      assert 2 == len(f.readlines())

def test_sourcefilechange():
  makeauto.STOP_AFTER_NSEC = 2
  tmp_source_file = 'source_file'
  with changedir(TEST_MAKEFILES_DIR), cleanupfiles(TMP_FILENAME, tmp_source_file):
    open(tmp_source_file, 'w').close()
    t = Thread(target=makeauto.makeauto, args=(test_sourcefilechange.__name__,))
    t.start()
    time.sleep(1)
    touch_file(tmp_source_file)
    t.join()
    with open(TMP_FILENAME, 'r') as f:
      assert 2 == len(f.readlines())

def touch_file(filename):
  os.utime(filename, None)
  
