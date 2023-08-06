# -*- coding: utf-8 -*-

__author__ = 'gchlebus'

from makeauto import makeauto
from utils import printmsg
import click

@click.command(help='Run make automatically on source files change.')
@click.option('--filename', '-f', default='Makefile', type=click.STRING,
              help='Name of the makefile.', show_default=True)
@click.option('--target', '-t', default='all', type=click.STRING,
              help='Make target.', show_default=True)
@click.option('--debug', '-d', is_flag=True, help='Toggle debug mode.')
def cli(filename, target, debug):
  try:
    makeauto(filename, target, debug)
  except RuntimeError as e:
    printmsg(e)

if __name__ == '__main__':
  cli()

