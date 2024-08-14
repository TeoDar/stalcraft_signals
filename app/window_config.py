# Для пересборки UI python -m PyQt6.uic.pyuic -o ./app/window.py -x interface.ui

from time import sleep
from PyQt6.QtWidgets import QApplication, QMainWindow, QSpinBox
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from window import Ui_main_window
from config import Configuration
from signal_catcher import SignalCatcher
from logger import Logger
import webbrowser
import win32api
import py_win_keyboard_layout


class Interface(QMainWindow, Ui_main_window):
    def __init__(self, app: QApplication, conf: Configuration):
        self.conf = conf
        super().__init__()
        # Set up the user interface from Designer.
        self.setupUi(self)
        # Настройки всех функций окна
        self.configure()
        QTimer.singleShot(1, self.move_to_right_bottom)
        app.focusChanged.connect(self.onFocusChanged)

        self.logger = Logger(self)
        self.catcher = SignalCatcher(conf, self.logger)
        self.cathing = False
        # Установка горячей клавиши
        self.catcher.ahk.add_hotkey(self.qt_hotkey_to_ahk(self.conf.hotkey), callback=self.start_search)
        self.catcher.ahk.start_hotkeys()
        # Конфигурация кнопки "ПОИСК"
        self.search.clicked.connect(self.start_search)

    def reconfigure(self):
        self.conf.init_config()
        self.close()

    def configure(self):
        # Window
        self.setWindowIcon(QIcon("./res/icon.ico"))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(self.conf.width, self.conf.height)
        #self.move_to_right_bottom()
        self.pb.hide()
        # Menu
        self.menu_repository_open.triggered.connect(lambda: webbrowser.open("https://github.com/TeoDar/stalcraft_signals"))
        self.menu_create_issue.triggered.connect(lambda: webbrowser.open("https://github.com/TeoDar/stalcraft_signals/issues/new/choose"))
        self.menu_restore_settings.triggered.connect(self.reconfigure)
        #  Кнопки и конфигурация
        # Горячая клавиша запуска/остановки
        self.hotkey.setKeySequence(self.conf.hotkey)
        self.hotkey.editingFinished.connect(self.set_hotkey)
        # Клавиша в игре, для открытия САК
        self.sak_key.setKeySequence(self.conf.sak_key)
        self.sak_key.editingFinished.connect(lambda: self.conf.set_value(key="sak_key", value=self.sak_key.keySequence().toString()))
        # Путь к AHK
        self.ahk_path.setText(self.conf.ahk_path)
        self.ahk_path.editingFinished.connect(lambda: self.conf.set_value(key="ahk_path", value=self.ahk_path.text()))
        # На какой лампочке останавливать поиск
        self.time_to_stop.setValue(self.conf.time_to_stop)
        self.time_to_stop.valueChanged.connect(lambda: self.conf.set_value(key="time_to_stop", value=self.time_to_stop.value()))
        # Задержка в сек. между открытиями САК
        self.reopen_time.setValue(self.conf.reopen_time)
        self.reopen_time.valueChanged.connect(lambda: self.conf.set_value(key="reopen_time", value=self.reopen_time.value()))
        # Задержка между кликами по кнопкам САК
        self.click_interval.setValue(self.conf.click_interval)
        self.click_interval.valueChanged.connect(lambda: self.conf.set_value(key="click_interval", value=self.click_interval.value()))
        # Индикатор сигнала
        self.x_signal.setValue(self.conf.x_signal)
        self.x_signal.valueChanged.connect(lambda: self.conf.set_value(key="x_signal", value=self.x_signal.value()))
        self.y_signal.setValue(self.conf.y_signal)
        self.y_signal.valueChanged.connect(lambda: self.conf.set_value(key="y_signal", value=self.y_signal.value()))
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

        # Кнопки установить
        self.signal_set.clicked.connect(lambda: self.get_coords_for(self.x_signal, self.y_signal, "x_signal", "y_signal"))
        self.med_rad_set.clicked.connect(lambda: self.get_coords_for(self.x_med_rad, self.y_med_rad, "x_med_rad", "y_med_rad"))
        self.tumbler_set.clicked.connect(lambda: self.get_coords_for(self.x_tumbler, self.y_tumbler, "x_tumbler", "y_tumbler"))
        self.ready_set.clicked.connect(lambda: self.get_coords_for(self.x_ready, self.y_ready, "x_ready", "y_ready"))
        self.search_set.clicked.connect(lambda: self.get_coords_for(self.x_search, self.y_search, "x_search", "y_search"))

        # Звуки
        self.sound_start_play.clicked.connect(lambda: self.catcher.play_sound(self.conf.sound_start_path, self.conf.sound_start_volume))
        self.sound_fail_play.clicked.connect(lambda: self.catcher.play_sound(self.conf.sound_fail_path, self.conf.sound_fail_volume))
        self.sound_found_play.clicked.connect(lambda: self.catcher.play_sound(self.conf.sound_found_path, self.conf.sound_found_volume))

        self.sound_start_path.setText(self.conf.sound_start_path)
        self.sound_start_path.editingFinished.connect(lambda: self.conf.set_value(key="sound_start_path", value=self.sound_start_path.text()))
        self.sound_start_slider.setValue(self.conf.sound_start_volume)
        self.sound_start_slider.valueChanged.connect(lambda: self.conf.set_value(key="sound_start_volume", value=self.sound_start_volume.text()))
        self.sound_fail_path.setText(self.conf.sound_fail_path)
        self.sound_fail_path.editingFinished.connect(lambda: self.conf.set_value(key="sound_fail_path", value=self.sound_fail_path.text()))
        self.sound_fail_slider.setValue(self.conf.sound_fail_volume)
        self.sound_fail_slider.valueChanged.connect(lambda: self.conf.set_value(key="sound_fail_volume", value=self.sound_fail_volume.text()))
        self.sound_found_path.setText(self.conf.sound_found_path)
        self.sound_found_path.editingFinished.connect(lambda: self.conf.set_value(key="sound_found_path", value=self.sound_found_path.text()))
        self.sound_found_slider.setValue(self.conf.sound_found_volume)
        self.sound_found_slider.valueChanged.connect(lambda: self.conf.set_value(key="sound_found_volume", value=self.sound_found_volume.text()))

    def before_search(self):
        self.config_tab.setEnabled(False)
        self.search.setText("Идёт поиск")
        self.pb.show()

    def after_search(self):
        self.pb.hide()
        self.search.setText("Поиск сигнала")
        self.config_tab.setEnabled(True)

    def start_search(self):
        # Смена на таб с поиском
        self.tabs.setCurrentWidget(self.search_tab)
        # Смена раскладки на Английскую
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
        if not self.cathing:
            self.before_search()
            self.cathing = True
            self.catcher.catch()
        else:
            self.logger.put("[Остановка сканирования]")
            self.catcher.stop()
        self.cathing = False
        self.after_search()

    def move_to_right_bottom(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().bottomRight()
        qr.moveBottomRight(cp)
        self.move(qr.topLeft())

    def get_coords_for(self, x_widget: QSpinBox, y_widget: QSpinBox, x_key, y_key):
        coords_not_getted = True
        clicked = None
        x, y = x_widget.value(), y_widget.value()
        while coords_not_getted:
            lkm_clicked = win32api.GetKeyState(0x01)
            if lkm_clicked < 0:
                clicked = True
                x, y = self.catcher.get_mouse_coords()
                x_widget.setValue(x)
                self.conf.set_value(key=x_key, value=x)
                y_widget.setValue(y)
                self.conf.set_value(key=y_key, value=y)
            else:
                if clicked == True:
                    coords_not_getted = False
            QTest.qWait(100)
        return x, y

    def set_hotkey(self):
        key = self.hotkey.keySequence().toString()
        self.conf.set_value(key="hotkey", value=key)
        self.catcher.ahk.clear_hotkeys()
        self.catcher.ahk.stop_hotkeys()
        self.catcher.ahk.add_hotkey(self.qt_hotkey_to_ahk(key), callback=self.start_search)
        self.catcher.ahk.start_hotkeys()

    def qt_hotkey_to_ahk(self, key: str):
        key = key.replace("Shift+", "+")
        key = key.replace("Ctrl+", "^")
        key = key.replace("Alt+", "!")
        return key

    ##########################################
    ####    Переопределение событий QT    ####
    ##########################################

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def resizeEvent(self, event):
        g = self.geometry()
        self.conf.set_value(key="width", value=g.width())
        self.conf.set_value(key="height", value=g.height())

    def onFocusChanged(self):
        if self.isActiveWindow():
            self.setWindowOpacity(1)
        else:
            self.setWindowOpacity(0.5)
