# Для преобразования ui файла: python -m PyQt6.uic.pyuic -o ./app/window.py -x interface.ui

import ctypes
import sys
from PyQt6.QtWidgets import QApplication
from config import Configuration
from window_config import Interface
from signal_finder import SignalFinder


class App:
    def __init__(self) -> None:
        app = QApplication([])

        conf = Configuration()
        window = Interface(conf)

        window.show()
        app.exec()


def main():
    App()


if __name__ == "__main__":
    main()
