# -*- coding: utf-8 -*-

__author__ = 'gchlebus'

import os
from .utils import printmsg, notify
from .parser import MakefileParser
from subprocess import PIPE, CalledProcessError, check_output
from watchdog.events import FileSystemEventHandler


class MakeautoEventHandler(FileSystemEventHandler):
  def __init__(self, filename, target, debug=False):
    self.filename = filename
    self.target = target
    self.debug = debug
    self.init()

  def __call__(self):
    args = ['make', '-f', self.filename, self.target]
    printmsg('Calling: %s' % ' '.join(args))
    try:
      check_output(args, stdin=PIPE)
    except CalledProcessError as e:
      printmsg('Failure: %s' % e)
      notify("Failed")

  def on_any_event(self, event):
    if self.debug:
      printmsg(event)
    if self.is_watched(event.src_path):
      self()
    elif self.is_makefile(event.src_path):
      if self.debug:
        printmsg('Makefile change detected.')
      self.init()

  def init(self):
    parser = MakefileParser(self.filename, self.target, debug=self.debug)
    self.watched_files = self.get_files(parser.prerequisites)
    self.watched_dirs = self.get_dirs(parser.prerequisites)
    self()

  def get_files(self, path_list):
    files = [p for p in path_list if os.path.isfile(p)]
    if files and self.debug:
      printmsg('Watched files: %s' % ', '.join(files))
    return files

  def get_dirs(self, path_list):
    dirs = [p for p in path_list if os.path.isdir(p)]
    if dirs and self.debug:
      printmsg('Watched directories: %s' % ', '.join(dirs))
    return dirs

  def is_watched(self, src_path):
    ret = False
    if os.path.exists(src_path):
      ret |= any([os.path.samefile(src_path, s) for s in self.watched_files])
      ret |= any([s in src_path for s in self.watched_dirs])
    return ret

  def is_makefile(self, src_path):
    if os.path.exists(src_path):
      return os.path.samefile(self.filename, src_path)
    return False
  
