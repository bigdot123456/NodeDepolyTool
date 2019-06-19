from PyQt5.QtWidgets import (QApplication, QWidget, QFontComboBox, QLabel,
                             QHBoxLayout, QPushButton, QMessageBox, QVBoxLayout)
from PyQt5.QtCore import QMetaObject


class MainWindow(QWidget):
    def __init__(self):
        super().__init__(None)

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        # 第一种信号与槽连接的方法
        cb_font = QFontComboBox(currentFontChanged=self.changeLabelFont)
        cb_font.pyqtConfigure(objectName='fontCombo', editable=False)
        # 第二种信号与槽连接的方法
        cb_font.currentFontChanged.connect(self.changeButtonFont)
        main_layout.addWidget(cb_font)

        label = QLabel()
        label.pyqtConfigure(text='示例文本！', objectName='label')

        main_layout.addWidget(label)

        closeButton = QPushButton('关闭')
        # 第三种连接信号与槽的方法
        closeButton.pyqtConfigure(objectName='button', clicked=self.close)
        main_layout.addWidget(closeButton)

        vhbox = QVBoxLayout()
        vhbox.addLayout(main_layout)
        vhbox.addStretch(1)
        self.setLayout(vhbox)

        # 第四种连接信号与槽的方法
        QMetaObject.connectSlotsByName(self)

    def changeLabelFont(self, c_font):
        label = self.findChild(QLabel, 'label')
        label.setFont(c_font)

    def changeButtonFont(self, c_font):
        button = self.findChild(QPushButton, 'button')
        button.setFont(c_font)

    def on_fontCombo_currentFontChanged(self, c_font):
        """
        通过 Widget 的 objectName 来连接槽，槽的名称如下所示：
        on_<object name>_<signal name>(<signal parameters>)
        在我们的这个例子中, object name 是 fontCombo; signal name 是 currentFontChanged; 信号的参数是 c_font, 表示选择的字体
        """
        QMessageBox.information(self, '提示信息', '选择的字体名称是: <b>%s</b>' % c_font.family())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(500, 400)
    w.show()
    sys.exit(app.exec_())