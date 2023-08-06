# -*- coding: utf-8 -*-

__author__ = 'gchlebus'

import sys, os

def printmsg(msg):
  print('makeauto: %s' % msg)

def notify(msg):
  if sys.platform == 'darwin':
    os.system("""
    osascript -e 'display notification "%s" with title "%s"'
    """ % (msg, 'makeauto'))
    
