#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import fcntl, os
import time


class Server(object):
    def __init__(self, args, server_env=None):
        if server_env:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=server_env)
        else:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            print(f"Popen({args}, stdin=PIPE, stdout=PIPE, stderr=PIPE)")
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def send(self, data, tail='\n'):
        self.process.stdin.write(data + tail)
        self.process.stdin.flush()

    def recv(self, t=.1, e=1, tr=5, stderr=0):
        time.sleep(t)
        if tr < 1:
            tr = 1
        x = time.time() + t
        r = ''
        pr = self.process.stdout
        if stderr:
            pr = self.process.stdout
        while time.time() < x or r:
            r = pr.read()
            if r is None:
                if e:
                    raise Exception('Error with process Reading!')
                else:
                    break
            elif r:
                return r.rstrip()
            else:
                time.sleep(max((x - time.time()) / tr, 0))
        return r.rstrip()


if __name__ == "__main__":
    fullcmd= """
        work/gman --datadir ./work/chaindata --entrust ./entrust.json --syncmode "full" --manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" --testmode Yeying1021! 
        """
    ServerArgs = ['work/gman', '--datadir ./work/chaindata --syncmode "full" --manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" --testmode Yeying1021!@# --entrust ./entrust.json']
    server = Server(ServerArgs)
    test_data = 'aa', 'vv', 'ccc', 'ss', 'ss', 'xx'
    for x in test_data:
        server.send(x)
        print(x, server.recv())
