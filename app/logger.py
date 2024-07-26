from window import Ui_main_window


class Logger:
    def __init__(self, window: Ui_main_window) -> None:
        self.window = window

    def clear(self):
        self.window.log.clear()

    def put(self, text):
        self.window.log.insertPlainText(text)
