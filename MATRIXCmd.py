# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys

import re
import subprocess


class MATRIXCmd():

    def checkAddressValid(address):
        inputstr = address.strip()
        # regPattern = 'r\'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}\''
        # regPattern= '''r'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}\''''
        # regPattern=r'^https?:/{2}\w.+$'
        # pattern = re.compile(regPattern) #This method is not ok!
        pattern = re.compile(r'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}')

        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        match = pattern.match(inputstr)
        if match:
            valid_address = inputstr
        else:
            valid_address = []

        return match, valid_address

    @property
    def execute_cmd(cmd):
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            return p.returncode, stderr
        return p.returncode, stdout

        # cmd = 'ls /u01'
        # returncode, out = execute_cmd(cmd)
        #
        # if returncode != 0:
        #     raise SystemExit('execute {0} err :{1}'.format(cmd, out))
        # else:
        #     print("execute command ({0} sucessful)".format(cmd))


if __name__ == "__main__":
    print("It's MATRIX World!")

    sys.exit()
