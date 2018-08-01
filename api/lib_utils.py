#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import copy
import six
import uuid
import traceback

from multiprocessing.pool import ThreadPool

def strid():
  return str(uuid.uuid4())

def mills():
  return int(round(time.time() * 1000))

POOL0  = ThreadPool()
POOLIO = ThreadPool(1000)

class XLogger(object):
  def __init__(self):
    self.debug   = six.print_
    self.info    = six.print_
    self.warning = six.print_
    self.error   = six.print_


Logger = XLogger()

# closer term
class XCloser(object):
  L_WORK = 0
  L_CONN = 100
  L_SYSM = 1000

  def __init__(self):
    self.target = []

  def add(self, level, func):
    self.target.append([level, func])

  def closeSub(self, l0):
    try:
      xdig = "%5d" % l0[0]
      Logger.info("killing", xdig, l0[1])
      l0[1]()
    except:
      traceback.print_exc()
    finally:
      return


  def close(self):
    self.target.sort(key=lambda tup: tup[0])
    t2 = copy.copy(self.target)
    for l0 in t2:
      self.closeSub(l0)

Closer = XCloser()
