import sys
import subprocess
import pyautogui, keyboard
from time import sleep, strftime, localtime
from ahk import AHK
from ahk.directives import NoTrayIcon

from app.config import *
conf = Configuration()

class SignalFinder:
    def __init__(self) -> None:
        self.ahk = AHK(directives=[NoTrayIcon(apply_to_hotkeys_process=True)])
        self.win = self.ahk.win_get("STALCRAFT")
        if not self.win:
            exit("[Ошибка]: Не найдено окно STALCRAFT или игра не запущена")

        self.searching_active = False
        self.ahk.add_hotkey(keyname="f3", callback=self.manager)
        self.ahk.add_hotkey(keyname="=", callback=self.incr_lumps)
        self.ahk.add_hotkey(keyname="-", callback=self.decr_lumps)
        self.ahk.start_hotkeys()
        keyboard.wait("f4")
        subprocess.run(["taskkill", "/F", "/IM", "AutoHotkey.exe"])

    def manager(self):
        if self.searching_active:
            self.searching_active = False
            print("\n[Поиск остановлен]")
        else:
            print("[Запуск поиска]")
            self.searching_active = True
        self.searching()

    def searching(self):
        if self.searching_active == False:
            return
        self.win.activate()
        sleep(0.5)
        self.win.send("x")
        sleep(1)
        rs, gs, bs = pyautogui.pixel(conf.x_signal, conf.y_signal)  # Цвет индикатора НЕнайденного сигнала
        print(strftime("\n[%H:%M:%S]", localtime()), end=": ")
        print(f"Начальный цвет индикатора: [R:{rs} G:{gs} B:{bs}]")
        s_color_summ = rs + gs + bs  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала
        s = [".", "..", "...", "...."]
        i = 0
        while self.searching_active:
            # 5-кратная проверка индикатора сигнала, каждые 0.25 секунд
            for _ in range(6):
                sleep(0.25)
                r, g, b = pyautogui.pixel(conf.x_signal, conf.conf.y_signal)
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
        pyautogui.moveTo(x=conf.x_med_rad, y=conf.y_med_rad)  # , duration=0.2)
        self.win.click(x=conf.x_med_rad, y=conf.y_med_rad, blocking=True)
        # pyautogui.moveTo(x=conf.x_small_rad, y=conf.y_small_rad)#, duration=0.2)
        # self.win.click(x=conf.x_small_rad, y=conf.y_small_rad, blocking=True)
        # Запуск сканирования
        pyautogui.moveTo(x=conf.x_m_tumbler, y=conf.y_tumbler)  # , duration=0.2)
        self.win.click(x=conf.x_m_tumbler, y=conf.y_tumbler, blocking=True)
        for i in range(11):
            if i <= self.lamps:
                sleep(1.5)
        # Отключение сканирования
        pyautogui.moveTo(x=conf.x_m_tumbler, y=conf.y_tumbler)
        self.win.click(x=conf.x_m_tumbler, y=conf.y_tumbler, blocking=True)
        # Нажатие на кнопку ПОИСК
        sleep(0.15)
        if self.check_founded():
            pyautogui.moveTo(x=conf.x_search, y=conf.y_search)  # , duration=0.2)
            self.win.click(x=conf.x_search, y=conf.y_search, blocking=True)
            return True
        else:
            return False

    def check_founded(self) -> bool:
        r, g, b = pyautogui.pixel(conf.x_s_ready, conf.conf.y_s_ready)
        if r + g + b >= 100:
            return True
        print("Похоже сигнал не найден. Цвет окна:", r, g, b)
        winsound.PlaySound("./sounds/fail.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        sleep(3)
        return False

    def incr_lumps(self):
        print(f"Сканирование до {conf.lamp_to_stop} лампочки")
        if conf.lamp_to_stop+1 > 10:
            return
        conf.set_value("lamp_to_stop", conf.lamp_to_stop+1)

    def decr_lumps(self):
        print(f"Сканирование до {conf.lamp_to_stop} лампочки")
        if conf.lamp_to_stop-1 < 0:
            return
        conf.set_value("lamp_to_stop", conf.lamp_to_stop-1)

    def reopen_suck(self):
        if self.searching_active == False:
            return
        self.win.send("x")
        sleep(S.reopen_time)
        if self.searching_active == False:
            return
        self.win.send("x")
