#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import six
import time


from api.wsclient import WSClient
from api.lib_utils import Closer





if __name__ == '__main__':
  xurl = "ws://127.0.0.1:3501/ws"
  ws = WSClient(xurl)
  ws.start()
  while True:
    time.sleep(1)
  six.print_("over")
  ws.stop()
  Closer.close()

