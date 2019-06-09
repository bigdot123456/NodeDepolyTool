# -*- coding: utf-8 -*-

"""
Module implementing MATRIXAppCode.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from Ui_MATRIXWallet import Ui_MainWindow

from random import randint

import sys

import re


class MATRIXAppCode(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MATRIXAppCode, self).__init__(parent)
        self.setupUi(self)
        self.num = randint(1, 100)

        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '确认', '确认退出吗', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # QMessageBox.about(self,self.lineEdit.text(), 'Good!')
        inputstr1 = self.lineEdit.text()
        inputstr = inputstr1.strip()

        regPattern = 'r\'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}\''
        # regPattern= '''r'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}\''''
        # regPattern=r'^https?:/{2}\w.+$'
        # pattern = re.compile(regPattern) #This method is not ok!
        pattern = re.compile(r'^MAN\.[a-km-zA-HJ-NP-Z1-9]{25,34}')

        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        match = pattern.match(inputstr)

        if match:
            # 使用Match获得分组信息
            print("Ok.")
            QMessageBox.question(self, '提示部署输入账户为', inputstr, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            QMessageBox.about(self, '提示请勿输入A0账户', '请输入正确的MATRIX A1账户')

            self.num = randint(1, 100)

            self.lineEdit.clear()

            self.lineEdit.setFocus()
        # guessnumber = 10
        # int(self.lineEdit.text())

        print(self.num)
        # raise NotImplementedError


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MATRIXAppCode()

    sys.exit(app.exec_())
