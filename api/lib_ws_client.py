#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import json
import traceback

import websocket

from .lib_utils import mills
from .lib_utils import POOLIO as POOL
from .lib_utils import Closer
from .lib_utils import Logger
from .lib_utils import strid


SLEEP_TIME = 5 * 1000

class C0WS(object):
  def __init__(self, xaddr, pool = POOL):
    # websocket.enableTrace(True)
    self.xaddr = xaddr
    self.pool = pool
    self.ws = 0
    self.clientid = ""
    self.isRunning = False

    self.on_message = None
    self.on_error = None
    self.on_close = None
    self.on_open = None
    self.lastTime = 0

  def _callback(self, callback, *args):
    if callback:
      try:
        callback(*args)
      except:
        traceback.print_exc()

  def loopRunForever(self):
    while self.isRunning:
      self.lastTime = mills()
      self.ws.run_forever()
      xtime = mills()
      if xtime < self.lastTime + SLEEP_TIME:
        xdt = self.lastTime + SLEEP_TIME - xtime
        time.sleep(xdt / 1000.0)

  def trigger_start(self):
    if not self.isRunning:
      return
    if self.ws is not 0:
      return

    self.ws = websocket.WebSocketApp(self.xaddr,
                                     on_message=self.on_message_inter,
                                     on_error=self.on_error_inter,
                                     on_close=self.on_close_inter)
    self.ws.on_open = self.on_open_inter
    self.pool.apply_async(self.loopRunForever, [])

  def start(self):
    if self.isRunning:
      return
    self.isRunning = True
    Closer.add(1000, self.stop)
    self.trigger_start()

  def sendStr(self, xstr):
    if self.clientid == "":
      Logger.error("C0WS", "send to a closed ws")
      return
    try:
      self.ws.send(xstr)
    except:
      traceback.print_exec()

  def send(self, xjson):
    return self.sendStr(json.dumps(xjson))

  def on_message_str(self, xmessage):
    self._callback(self.on_message, json.loads(xmessage))

  def on_message_inter(self, ws, message):
    self.pool.apply_async(self.on_message_str, [message])

  def on_error_inter(self, ws, error):
    self._callback(self.on_error, error)

  def on_close_inter(self, ws):
    Logger.warning("C0WS", "socket closed")
    self.clientid = ""
    self._callback(self.on_close)

  def on_open_inter(self, ws):
    self.clientid = strid()
    self._callback(self.on_open, self.clientid)

  def stop(self):
    if not self.isRunning:
      return
    self.isRunning = False
    if self.ws is 0:
      return
    Logger.warning("WSClient", "try close")
    self.ws.close()
    Logger.warning("WSClient", "try close over")

  def kill(self, clientid):
    if self.clientid == clientid:
      self.ws.close()