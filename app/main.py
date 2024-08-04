# Для преобразования ui файла: python -m PyQt6.uic.pyuic -o ./app/window.py -x interface.ui
# Билд приложения через auto-py-to-exe. Настройки билда в build.json


from PyQt6.QtWidgets import QApplication
from config import Configuration, exception
from window_config import Interface


class App:
    def __init__(self) -> None:
        app = QApplication([])
        conf = Configuration()
        window = Interface(app, conf)
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
