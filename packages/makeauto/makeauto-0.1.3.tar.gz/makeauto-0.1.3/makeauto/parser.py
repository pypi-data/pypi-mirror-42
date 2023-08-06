# -*- coding: utf-8 -*-

__author__ = 'gchlebus'


import os
from .utils import printmsg

class MakefileParser(object):
  def __init__(self, filename, target='all', debug=False):
    self.targets = {}
    self.variables = {}
    self.debug = debug
    self.parse(filename)
    if target not in self.targets:
      raise RuntimeError('Target %s not found.' % target)
    self.expand_variables()
    self.prerequisites = self.resolve_dependencies(target)

  def parse(self, filename):
    if os.path.exists(filename):
      with open(filename, 'r') as f:
        for line in f.readlines():
          if ':' in line:
            target, prerequisites = line.split(':')
            self.targets[target.strip()] = prerequisites.strip().split()
          if '=' in line:
            k, v = line.split('=', 1)
            self.variables[k.strip()] = v.strip()
      if self.debug:
        printmsg('parse()')
        self.debug_print(print_variables=True)
    else:
      raise RuntimeError('%s not found.' % filename)

  def expand_variables(self):
    for target, prerequisites in self.targets.items():
      for i in range(len(prerequisites)):
        for varname, value in self.variables.items():
          self.targets[target][i] = self.targets[target][i].replace('${%s}' % varname, value)
    if self.debug:
      printmsg('expand_variables()')
      self.debug_print()

  def resolve_dependencies(self, target):
    prerequisites = []
    for p in self.targets[target]:
      if p in self.targets:
        prerequisites.extend(self.resolve_dependencies(p))
      else:
        prerequisites.append(p)
    return prerequisites

  def debug_print(self, print_variables=False):
    if self.targets:
      printmsg('Targets:')
      for target, prerequisites in self.targets.items():
        printmsg('  %s: %s' % (target, ', '.join(prerequisites)))
    else:
      printmsg('No targets.')
    if print_variables:
      if self.variables:
        printmsg('Variables:')
        for varname, value in self.variables.items():
          printmsg('  %s=%s' % (varname, value))
      else:
        printmsg('No variables.')

