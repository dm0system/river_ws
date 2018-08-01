#!/usr/bin/python2
# -*- coding: utf-8 -*-

from .lib_utils import Logger
from .lib_ws_client import C0WS

class C1Chatgod(object):
  NAME_SETNAME = "_setname"
  NAME_CTRL = "_"

  def __init__(self):
    self.booked = {}
    self.serverid = ""
    self.ctrlMap = {
      self.NAME_SETNAME: self.setname
    }

    self.do_send = None
    self.onControl = None


  def tryControl(self, xjson):
    xport = xjson[0]
    if xport.startswith(self.NAME_CTRL):
      xf = self.ctrlMap.get(xport, self.onControl)
      xf(xjson)
      return False
    return True

  def setname(self, xjson):
    self.serverid = xjson[1]
    Logger.warning("C1Chatgod", "xid is " + self.serverid)
    self.on_setname()

  def on_setname(self):
    for l0 in self.booked:
      self.listen_direct(l0)

  def listen_direct(self, xname):
    pass

  def listen(self, xname):
    if xname in self.booked:
      return
    self.booked[xname] = 0
    self.listen_direct(xname)

class WSClient(object):
  def __init__(self, xaddr):
    self.c0 = C0WS(xaddr)
    self.c1 = C1Chatgod()

    self.start  = self.c0.start
    self.stop   = self.c0.stop
    self.listen = self.c1.listen

    self.onError = None
    self.onMessage = None
    self.onControl = None

    self.c0.on_error = self.onErrorInner
    self.c0.on_message = self.onMessageInner
    self.c1.onControl = self.onControlInner
    self.c1.do_send = self.c0.send

  def onMessageInner(self, n1):
    if self.c1.tryControl(n1):
      self.recMessage(n1)

  def onErrorInner(self, error):
    if self.onError:
      self.onError(error)

  def onControlInner(self, n1):
    if self.onControl:
      self.onControl(n1)

  def send(self, n1):
    Logger.debug(n1)
    self.c0.send(n1)

  def send2(self, *args):
    self.send(args)

  def recMessage(self, n1):
    self.onMessage(n1)
    return False

