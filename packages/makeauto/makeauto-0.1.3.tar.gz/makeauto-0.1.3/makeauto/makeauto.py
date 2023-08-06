# -*- coding: utf-8 -*-

__author__ = 'gchlebus'

from watchdog.observers import Observer
from .event_handler import MakeautoEventHandler
from .utils import printmsg
import time

STOP_AFTER_NSEC = 0

def makeauto(filename='Makefile', target='all', debug=False):
  event_handler = MakeautoEventHandler(filename, target, debug=debug)
  observer = Observer()
  observer.schedule(event_handler, '.', recursive=True)
  observer.start()
  try:
    loop()
  except KeyboardInterrupt:
    printmsg('Stop requested.')
  finally:
    observer.stop()
  observer.join()

def loop():
  global STOP_AFTER_NSEC
  if STOP_AFTER_NSEC:
    while STOP_AFTER_NSEC > 0:
      time.sleep(1)
      STOP_AFTER_NSEC -= 1
  else:
    while True:
      time.sleep(1)
