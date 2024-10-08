from ahk import AHK, Window
from ahk.directives import NoTrayIcon
from logger import Logger
from config import Configuration
from PyQt6.QtTest import QTest
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from window_manager import WindowMgr
from traceback import format_exc as exc


class SignalCatcher:
    def __init__(self, conf: Configuration, logger: Logger) -> None:
        self.conf = conf
        self.run = False
        self.logger = logger
        self.player = QMediaPlayer()
        self.ahk = AHK(directives=[NoTrayIcon(apply_to_hotkeys_process=True)])

    def stop(self):
        self.run = False
        self.win = None

    def catch(self):
        self.run = True

        try:
            self.win: Window = self.ahk.win_get(title="STALCRAFT")
        except Exception as e:
            print(e)
            self.logger.put("Не найдено запущенного STALCRAFT")
            return
        self.logger.put("[Запуск поиска]")
        try:
            self.searching()
        except Exception as e:
            print(exc())
            self.logger.put(f"{exc()}")
            return

    def searching(self):
        """Цикл поиска"""
        if not self.run:
            return
        self.logger.put("Активация окна")
        WindowMgr().find_window_wildcard("STALCRAFT").set_foreground()
        QTest.qWait(500)
        if not self.run:
            return
        self.logger.put("Открытие САК")
        self.win.send(self.conf.sak_key)
        QTest.qWait(1000)
        if not self.run:
            return
        rs, gs, bs = self.get_color(self.conf.x_signal, self.conf.y_signal)  # Цвет индикатора НЕнайденного сигнала
        self.logger.put("Перемещение мыши в позицию индикатора сигнала. Проверьте корректность.")
        QTest.qWait(1000)
        self.ahk.mouse_move(self.conf.x_signal, self.conf.y_signal, speed=15)
        self.logger.put(f"Цвет индикатора сигнала:  R[{rs}] G[{gs}] B[{bs}]")
        s_color_summ = rs + gs + bs  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала
        while self.run:
            # 5-кратная проверка индикатора сигнала, каждые 0.25 секунд
            self.logger.put("Проверка индикатора")
            for _ in range(5):
                if not self.run:
                    return
                QTest.qWait(250)
                r, g, b = self.get_color(self.conf.x_signal, self.conf.y_signal)
                # self.logger.put(f"Индикатор сигнала: R[{r}] G[{g}] B[{b}]")
                summ = r + g + b
                if summ != s_color_summ and summ != 765:
                    self.logger.put(f"Новый цвет индикатора сигнала: R[{r}] G[{g}] B[{b}]")
                    if not self.run:
                        return
                    self.logger.put("[Сигнал найден]")
                    self.play_sound(self.conf.sound_start_path, self.conf.sound_start_volume)
                    self.logger.put("Начинаю сканирование")
                    founded = self.burn_signal()
                    if not self.run:
                        return
                    if founded:
                        self.play_sound(self.conf.sound_found_path, self.conf.sound_found_volume)
                        return
                    QTest.qWait(1000)
                    break
            self.logger.put("Сигнал не найден. Переоткрытие САК")
            self.reopen_suck()

    def burn_signal(self):
        """Начало сканирования для обнаружения сигнала"""
        # Переключение на среднюю дистанцию
        QTest.qWait(self.conf.click_interval)
        self.logger.put("Переключаю на среднюю дистанцию")
        if not self.run:
            return
        self.ahk.mouse_move(x=self.conf.x_med_rad, y=self.conf.y_med_rad, speed=10, blocking=True)
        QTest.qWait(100)
        self.win.click(x=self.conf.x_med_rad, y=self.conf.y_med_rad, blocking=True)
        if not self.run:
            return
        # Запуск сканирования
        QTest.qWait(self.conf.click_interval)
        self.logger.put("Переключаю тумблер")
        self.ahk.mouse_move(x=self.conf.x_tumbler, y=self.conf.y_tumbler, speed=10, blocking=True)
        QTest.qWait(100)
        self.win.click(x=self.conf.x_tumbler, y=self.conf.y_tumbler)
        self.logger.put(f"Ожидаю {self.conf.time_to_stop} мс до остановки поиска ...")
        if not self.run:
            return
        QTest.qWait(self.conf.time_to_stop)
        if not self.run:
            return
        # Отключение сканирования
        QTest.qWait(self.conf.click_interval)
        self.logger.put("Останавливаю сканирование")
        self.ahk.mouse_move(x=self.conf.x_tumbler, y=self.conf.y_tumbler, speed=10, blocking=True)
        QTest.qWait(100)
        self.win.click(x=self.conf.x_tumbler, y=self.conf.y_tumbler, blocking=True)
        if not self.run:
            return
        # Нажатие на кнопку ПОИСК
        QTest.qWait(self.conf.click_interval)
        self.logger.put("Проверяю, пойман ли сигнал")
        QTest.qWait(150)
        if self.check_founded():
            self.logger.put("Поймали!")
            self.ahk.mouse_move(x=self.conf.x_search, y=self.conf.y_search, speed=10, blocking=True)
            QTest.qWait(100)
            self.win.click(x=self.conf.x_search, y=self.conf.y_search, blocking=True)
            return True
        else:
            return False

    def check_founded(self) -> bool:
        """Проверка, был ли найден сигнал"""
        r1, g1, b1 = self.get_color(self.conf.x_ready, self.conf.y_ready)
        if r1 + g1 + b1 >= 100:
            return True
        self.logger.put(f"Похоже сигнал не найден. Цвет окошка под индикатором:: R[{r1}] G[{g1}] B[{b1}]")
        self.play_sound(self.conf.sound_fail_path, self.conf.sound_fail_volume)
        QTest.qWait(3000)
        return False

    def reopen_suck(self):
        if not self.run:
            return
        self.win.send(self.conf.sak_key)
        QTest.qWait(self.conf.reopen_time)
        if not self.run:
            return
        self.win.send(self.conf.sak_key)

    def get_color(self, x, y):
        hex_color = self.ahk.pixel_get_color(x, y)[2:]
        rgb = list(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return rgb[0], rgb[1], rgb[2]

    def get_mouse_coords(self):
        return self.ahk.get_mouse_position(coord_mode="Client")

    def play_sound(self, soundpath:str, volume:int):
        if self.player.isPlaying():
            self.player.stop()
            return
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl(soundpath))
        self.audio_output.setVolume(volume/100)
        self.player.play()
