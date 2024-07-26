import sys
import pyautogui, keyboard
from time import sleep, strftime, localtime
from ahk import AHK
from ahk.exceptions import AHKExecutionException
from logger import Logger


class SignalFinder:
    def __init__(self, conf, log: Logger) -> None:
        self.ahk = AHK()
        self.conf = conf
        self.log = log

    def find(self):
        self.log.clear()
        try:
            self.win = self.ahk.win_get("STALCRAFT")
        except AHKExecutionException:
            error = "Не найдено запущенного STALCRAFT"
            self.ahk.show_error_traytip("Ошибка", error)
            self.log.put(error)
            return

    def searching(self):
        if self.searching_active == False:
            return
        self.win.activate()
        sleep(0.5)
        self.win.send("x")
        sleep(1)
        rs, gs, bs = pyautogui.pixel(self.conf.x_signal, self.conf.y_signal)  # Цвет индикатора НЕнайденного сигнала
        print(strftime("\n[%H:%M:%S]", localtime()), end=": ")
        print(f"Начальный цвет индикатора: [R:{rs} G:{gs} B:{bs}]")
        s_color_summ = rs + gs + bs  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала
        i = 0
        while self.searching_active:
            # 5-кратная проверка индикатора сигнала, каждые 0.25 секунд
            for _ in range(6):
                sleep(0.25)
                r, g, b = pyautogui.pixel(self.conf.x_signal, self.conf.self.conf.y_signal)
                if r + g + b > s_color_summ:
                    winsound.PlaySound("./sounds/signal.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                    print(strftime("\n[%H:%M:%S]", localtime()), end=": ")
                    print(f"Сигнал найден!\nЦвет индикатора: [R:{r} G:{g} B:{b}]")
                    founded = self.burn_signal()
                    if founded:
                        winsound.PlaySound("./sounds/success.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                        self.searching_active = False
                        print("Поиск окончен")
                        return
            else:
                if self.searching_active == False:
                    return
                print("Поиск" + s[i], end="\r")
                sys.stdout.flush()
                self.reopen_suck()
                if i == 3:
                    i = 0
                    print("Поиск     ", end="\r")
                else:
                    i += 1

    def burn_signal(self) -> bool:
        # Переключение на среднюю дистанцию
        pyautogui.moveTo(x=self.conf.x_med_rad, y=self.conf.y_med_rad)  # , duration=0.2)
        self.win.click(x=self.conf.x_med_rad, y=self.conf.y_med_rad, blocking=True)
        # pyautogui.moveTo(x=self.conf.x_small_rad, y=self.conf.y_small_rad)#, duration=0.2)
        # self.win.click(x=self.conf.x_small_rad, y=self.conf.y_small_rad, blocking=True)
        # Запуск сканирования
        pyautogui.moveTo(x=self.conf.x_m_tumbler, y=self.conf.y_tumbler)  # , duration=0.2)
        self.win.click(x=self.conf.x_m_tumbler, y=self.conf.y_tumbler, blocking=True)
        for i in range(11):
            if i <= self.lamps:
                sleep(1.5)
        # Отключение сканирования
        pyautogui.moveTo(x=self.conf.x_m_tumbler, y=self.conf.y_tumbler)
        self.win.click(x=self.conf.x_m_tumbler, y=self.conf.y_tumbler, blocking=True)
        # Нажатие на кнопку ПОИСК
        sleep(0.15)
        if self.check_founded():
            pyautogui.moveTo(x=self.conf.x_search, y=self.conf.y_search)  # , duration=0.2)
            self.win.click(x=self.conf.x_search, y=self.conf.y_search, blocking=True)
            return True
        else:
            return False

    def check_founded(self) -> bool:
        r, g, b = pyautogui.pixel(self.conf.x_s_ready, self.conf.self.conf.y_s_ready)
        if r + g + b >= 100:
            return True
        print("Похоже сигнал не найден. Цвет окна:", r, g, b)
        winsound.PlaySound("./sounds/fail.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        sleep(3)
        return False

    def incr_lumps(self):
        print(f"Сканирование до {self.conf.lamp_to_stop} лампочки")
        if self.conf.lamp_to_stop + 1 > 10:
            return
        self.conf.set_value("lamp_to_stop", self.conf.lamp_to_stop + 1)

    def decr_lumps(self):
        print(f"Сканирование до {self.conf.lamp_to_stop} лампочки")
        if self.conf.lamp_to_stop - 1 < 0:
            return
        self.conf.set_value("lamp_to_stop", self.conf.lamp_to_stop - 1)

    def reopen_suck(self):
        if self.searching_active == False:
            return
        self.win.send("x")
        sleep(S.reopen_time)
        if self.searching_active == False:
            return
        self.win.send("x")
