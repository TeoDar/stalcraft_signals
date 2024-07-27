# Для преобразования ui файла: python -m PyQt6.uic.pyuic -o ./app/window.py -x interface.ui

from PyQt6.QtWidgets import QApplication
from config import Configuration, exception
from window_config import Interface
import ctypes

awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(0)


class App:
    def __init__(self) -> None:
        app = QApplication([])
        conf = Configuration()
        window = Interface(conf)
        window.show()
        app.exec()


def main():
    try:
        App()
    except Exception as e:
        print(e)
        exception(f"Ошибка запуска приложения!\n{e}")


if __name__ == "__main__":
    main()
