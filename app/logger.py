from window import Ui_main_window
from PyQt6 import QtGui


class Logger:
    def __init__(self, window: Ui_main_window) -> None:
        self.window = window
        self.log = window.log

    def clear(self):
        self.log.clear()

    def put(self, text):
        if self.window.cathing:
            self.log.insertPlainText(text + "\n")
            self.log.moveCursor(QtGui.QTextCursor.MoveOperation.End)
