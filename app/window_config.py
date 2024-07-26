# Для пересборки UI python -m PyQt6.uic.pyuic -o ./app/window.py -x interface.ui

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from window import Ui_main_window
from config import Configuration
from signal_finder import SignalFinder
from logger import Logger
import webbrowser


class Interface(QMainWindow, Ui_main_window):
    def __init__(self, conf: Configuration):
        super().__init__()
        self.conf = conf
        logger = Logger(self)
        self.finder = SignalFinder(conf, logger)

        # Set up the user interface from Designer.
        self.setupUi(self)
        # Настройки всех функций окна
        self.configure()

    def configure(self):
        # Window
        self.setWindowIcon(QIcon("icon.ico"))
        # Menu
        self.menu_repository_open.triggered.connect(lambda: webbrowser.open("https://github.com/TeoDar/stalcraft_signals"))
        self.menu_create_issue.triggered.connect(lambda: webbrowser.open("https://github.com/TeoDar/stalcraft_signals/issues/new/choose"))
        # Кнопки и конфигурация
        self.search.clicked.connect(self.finder.find)
        # Путь к AHK
        self.ahk_path.setText(self.conf.ahk_path)
        self.ahk_path.editingFinished.connect(lambda: self.conf.set_value(key="ahk_path", value=self.ahk_path.text()))
        # На какой лампочке останавливать поиск
        self.lamp_to_stop_slider.setValue(self.conf.lamp_to_stop)
        self.lamp_to_stop_slider.valueChanged.connect(lambda: self.conf.set_value(key="lamp_to_stop", value=self.lamp_to_stop.text()))
        # Задержка в сек. между открытиями САК
        self.reopen_time.setValue(self.conf.reopen_time)
        self.reopen_time.valueChanged.connect(lambda: self.conf.set_value(key="reopen_time", value=self.reopen_time.value()))
        # Индикатор сигнала
        self.x_signal.setValue(self.conf.x_signal)
        self.x_signal.valueChanged.connect(lambda: self.conf.set_value(key="x_signal", value=self.x_signal.value()))
        self.y_signal.setValue(self.conf.y_signal)
        self.y_signal.valueChanged.connect(lambda: self.conf.set_value(key="y_signal", value=self.y_signal.value()))
        # Кнопки [Малая]
        self.x_small_rad.setValue(self.conf.x_small_rad)
        self.x_small_rad.valueChanged.connect(lambda: self.conf.set_value(key="x_small_rad", value=self.x_small_rad.value()))
        self.y_small_rad.setValue(self.conf.y_small_rad)
        self.y_small_rad.valueChanged.connect(lambda: self.conf.set_value(key="y_small_rad", value=self.y_small_rad.value()))
        # Кнопки [Средняя]
        self.x_med_rad.setValue(self.conf.x_med_rad)
        self.x_med_rad.valueChanged.connect(lambda: self.conf.set_value(key="x_med_rad", value=self.x_med_rad.value()))
        self.y_med_rad.setValue(self.conf.y_med_rad)
        self.y_med_rad.valueChanged.connect(lambda: self.conf.set_value(key="y_med_rad", value=self.y_med_rad.value()))
        # Тумблер начала сканирования
        self.x_tumbler.setValue(self.conf.x_tumbler)
        self.x_tumbler.valueChanged.connect(lambda: self.conf.set_value(key="x_tumbler", value=self.x_tumbler.value()))
        self.y_tumbler.setValue(self.conf.y_tumbler)
        self.y_tumbler.valueChanged.connect(lambda: self.conf.set_value(key="y_tumbler", value=self.y_tumbler.value()))
        # Зелёного индикатора найденного сигнала
        self.x_ready.setValue(self.conf.x_ready)
        self.x_ready.valueChanged.connect(lambda: self.conf.set_value(key="x_ready", value=self.x_ready.value()))
        self.y_ready.setValue(self.conf.y_ready)
        self.y_ready.valueChanged.connect(lambda: self.conf.set_value(key="y_ready", value=self.y_ready.value()))
        # Кнопки [Поиск]
        self.x_search.setValue(self.conf.x_search)
        self.x_search.valueChanged.connect(lambda: self.conf.set_value(key="x_search", value=self.x_search.value()))
        self.y_search.setValue(self.conf.y_search)
        self.y_search.valueChanged.connect(lambda: self.conf.set_value(key="y_search", value=self.y_search.value()))
