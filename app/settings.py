from os import path, environ
import configparser
import asyncio


FILEPATH = "config.ini"

PROGRAMFILES = environ["PROGRAMFILES"]
environ["AHK_PATH"] = f"{PROGRAMFILES}\AutoHotkey\AutoHotkey.exe"

DEFAULT_CONFIG = {
    "# Номер монитора на котором запущена игра если мониторов больше чем 1 (начиная с 0)": None,
    "monitor": "0",
    "# На какой лампочке останавливать поиск": None,
    "lamp_to_stop": "6",
    "# Задержка в сек. между открытиями САК": None,
    "reopen_time": "1.5",
    "": None,
    "# Стандартные координаты для индикаторов под монитор 2560х1440,": None,
    "# для игры в оконном режиме с рамкой на весь экран": None,
    " ": None,
    "# Координаты [X] и [Y] для:": None,
    "# Индикатора сигнал": None,
    "x_signal": "745",
    "y_signal": "435",
    "# Кнопки [Малая]": None,
    "x_small_rad": "1070",
    "y_small_rad": "860",
    "# Кнопки [Средняя]": None,
    "x_med_rad": "1160",
    "y_med_rad": "860",
    "# Тумблера начала сканирования": None,
    "x_m_tumbler": "1445",
    "y_m_tumbler": "860",
    "# Зелёного индикатора найденного сигнала": None,
    "x_s_ready": "680",
    "y_s_ready": "530",
    "# Кнопки [Поиск]": None,
    "x_search": "680",
    "y_search": "630",
}


class Settings:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str  # Для сохранения регистра записи коментариев

        if not self.exist():
            self.init_config()
        else:
            self.config.read(FILEPATH, encoding="utf-8")

        self.lamp_to_stop = int(self.get("lamp_to_stop"))
        self.monitor = int(self.get("monitor"))
        self.reopen_time = float(self.get("reopen_time"))
        self.x_signal = int(self.get("x_signal"))
        self.y_signal = int(self.get("y_signal"))
        self.x_small_rad = int(self.get("x_small_rad"))
        self.y_small_rad = int(self.get("y_small_rad"))
        self.x_med_rad = int(self.get("x_med_rad"))
        self.y_med_rad = int(self.get("y_med_rad"))
        self.x_m_tumbler = int(self.get("x_m_tumbler"))
        self.y_m_tumbler = int(self.get("y_m_tumbler"))
        self.x_s_ready = int(self.get("x_s_ready"))
        self.y_s_ready = int(self.get("y_s_ready"))
        self.x_search = int(self.get("x_search"))
        self.y_search = int(self.get("y_search"))

    def exist(self):
        return path.exists(FILEPATH)

    def init_config(self):
        self.config["CONFIG"] = DEFAULT_CONFIG
        self.save_config()

    def save_config(self):
        with open(FILEPATH, "w+", encoding="utf-8") as f:
            self.config.write(f)

    def set_value(self, key, value):
        self.key = str(value)
        self.config[key] = value
        self.save_config()

    def get(self, key):
        try:
            return self.config["CONFIG"][key]
        except Exception:
            self.init_config()
            print(
                f"[ВНИМАНИЕ]: В конфигурационном файле не найден параметр [{key}]\nКонфиг был сброшен до стандартного."
            )
            return self.config["CONFIG"][key]


def main():
    Settings()


if __name__ == "__main__":
    main()
