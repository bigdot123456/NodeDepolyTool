# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys

from rpyc import Service
from rpyc.utils.server import ThreadedServer


class MATRIXVersionServer(Service):
    i = 0

    # 对于服务端来说， 只有以"exposed_"打头的方法才能被客户端调用，所以要提供给客户端的方法都得加"exposed_"
    def exposed_testVersion(self):
        print(f"check version {self.i}!\n")
        MATRIXVersionServer.i = self.i + 1
        return MATRIXVersionServer.i

if __name__ == "__main__":
    print("It's MATRIX World!")
    sr = ThreadedServer(service=MATRIXVersionServer, port=9999, auto_register=False)
    print("Start Server!")
    sr.start()

    sys.exit()
