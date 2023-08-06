from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextBlockFormat, QTextCharFormat
from time import time


class LoggingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Logging')

        button_box = QWidget()
        b_clear = QPushButton('Clear')
        b_close = QPushButton('Close')
        b_clear.clicked.connect(self.clear_click)
        b_close.clicked.connect(self.close_click)
        b_layout = QHBoxLayout()
        b_layout.addWidget(b_clear)
        b_layout.addWidget(b_close)
        button_box.setLayout(b_layout)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.log_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    @pyqtSlot()
    def clear_click(self):
        self.log_box.clear()

    @pyqtSlot()
    def close_click(self):
        self.hide()

    def _msg(self, msg, color):
        fmt = QTextBlockFormat()
        fmt.setBackground(Qt.black)
        char_f = QTextCharFormat()
        char_f.setForeground(color)
        self.log_box.textCursor().beginEditBlock()
        self.log_box.textCursor().setBlockFormat(fmt)
        self.log_box.textCursor().insertText(f'{time()}  -  {msg}\n', char_f)
        self.log_box.textCursor().endEditBlock()
        # TODO: follow check box?
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def info(self, msg):
        self._msg(msg, Qt.green)

    def warn(self, msg):
        self._msg(msg, Qt.yellow)

    def debug(self, msg):
        self._msg(msg, Qt.white)

    def error(self, msg):
        self._msg(msg, Qt.red)
