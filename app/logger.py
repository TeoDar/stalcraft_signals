from window import Ui_main_window
from PyQt6 import QtGui
from PyQt6.QtWidgets import QTextEdit


class Logger:
    def __init__(self, log: QTextEdit) -> None:
        self.log = log

    def clear(self):
        self.log.clear()

    def put(self, text):
        self.log.insertPlainText(text+"\n")
        self.log.moveCursor(QtGui.QTextCursor.MoveOperation.End)

