import ctypes
from os import path, environ
import configparser


FILEPATH = "config.ini"

PROGRAMFILES = environ["PROGRAMFILES"]
ahk_path = rf"{PROGRAMFILES}\AutoHotkey\v2\AutoHotkey.exe"
environ["AHK_PATH"] = ahk_path

DEFAULT_CONFIG = {
    "# Размер окна": None,
    "width": "475",
    "height": "275",
    "# Путь к AHK": None,
    "ahk_path": ahk_path,
    "# На какой лампочке останавливать поиск": None,
    "lamp_to_stop": "6",
    "# Задержка в сек. между открытиями САК": None,
    "reopen_time": "1500",
    "# Задержка между кликами по кнопкам САК": None,
    "click_interval": "500",
    "": None,
    "# Стандартные координаты для индикаторов под монитор 2560х1440,": None,
    "# для игры в оконном режиме с рамкой на весь экран": None,
    " ": None,
    "# Координаты [X] и [Y] для:": None,
    "# Индикатора сигнала": None,
    "x_signal": "1010",
    "y_signal": "545",
    "# Кнопки [Малая]": None,
    "x_small_rad": "1300",
    "y_small_rad": "950",
    "# Кнопки [Средняя]": None,
    "x_med_rad": "1400",
    "y_med_rad": "950",
    "# Тумблера начала сканирования": None,
    "x_tumbler": "1650",
    "y_tumbler": "950",
    "# Зелёного индикатора найденного сигнала": None,
    "x_ready": "950",
    "y_ready": "640",
    "# Кнопки [Поиск]": None,
    "x_search": "950",
    "y_search": "730",
}


def exception(error: str):
    ctypes.windll.user32.MessageBoxW(0, error, "Error", 0)


class Configuration:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str  # Для сохранения регистра записи коментариев

        if not self.exist():
            self.init_config()
        else:
            self.config.read(FILEPATH, encoding="utf-8")
        try:
            self.set_values_from_file()
        except Exception:
            exception("Ошибка чтения конфигурации.\nКонфигурационный файл был сброшен.")
            self.init_config()
            self.set_values_from_file()

    def set_values_from_file(self):
        self.width = int(self.get("width"))
        self.height = int(self.get("height"))
        self.ahk_path = str(self.get("ahk_path"))
        self.lamp_to_stop = int(self.get("lamp_to_stop"))
        self.reopen_time = int(self.get("reopen_time"))
        self.click_interval = int(self.get("click_interval"))
        self.x_signal = int(self.get("x_signal"))
        self.y_signal = int(self.get("y_signal"))
        self.x_small_rad = int(self.get("x_small_rad"))
        self.y_small_rad = int(self.get("y_small_rad"))
        self.x_med_rad = int(self.get("x_med_rad"))
        self.y_med_rad = int(self.get("y_med_rad"))
        self.x_tumbler = int(self.get("x_tumbler"))
        self.y_tumbler = int(self.get("y_tumbler"))
        self.x_ready = int(self.get("x_ready"))
        self.y_ready = int(self.get("y_ready"))
        self.x_search = int(self.get("x_search"))
        self.y_search = int(self.get("y_search"))

    def exist(self):
        return path.exists(FILEPATH)

    def init_config(self):
        self.config["CONFIG"] = DEFAULT_CONFIG
        self.save_config()

    def get(self, key):
        try:
            return self.config["CONFIG"][key]
        except Exception:
            self.init_config()
            exception(f"[ВНИМАНИЕ]: В конфигурационном файле не найден параметр [{key}]\nКонфиг был сброшен до стандартного.")
            return self.config["CONFIG"][key]

    def set_value(self, key, value):
        try:
            type_ = type(self.__getattribute__(key))
            self.__setattr__(key, value)
            value = type_(value)
            self.config["CONFIG"][key] = str(value)
            self.save_config()
        except Exception as e:
            exception(f"Ошибка записи параметра конфигурации\n{e}")

    def save_config(self):
        with open(FILEPATH, "w+", encoding="utf-8") as f:
            self.config.write(f)


def main():
    Configuration()


if __name__ == "__main__":
    main()
