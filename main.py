###################################################################################################
# Введите номер монитора на котором запущена игра вашего экрана:
screen = 0
###################################################################################################
import subprocess
import sys, os
import winsound
import pyautogui, keyboard
from screeninfo import get_monitors
from random import randint
from time import sleep, strftime, localtime
from multiprocessing import Process, set_start_method
from ahk import AHK
from ahk.directives import NoTrayIcon


class SignalFinder:
    def __init__(self) -> None:
        self.ahk = AHK(directives=[NoTrayIcon(apply_to_hotkeys_process=True)])
        self.win = self.ahk.win_get("STALCRAFT")
        if not self.win:
            exit("[Ошибка]: Не найдено окно STALCRAFT или игра не запущена")

        screen_width, screen_height = [(x.width, x.height) for x in get_monitors()][screen]
        self.x_signal, self.y_signal = int(0.359375 * screen_width), int(0.368055 * screen_height)  # Координаты индикатора найденного сигнала
        self.x_med_rad, self.y_med_rad = int(0.5625 * screen_width), int(0.7361 * screen_height)  # Координаты кнопки "Средняя"
        self.x_tumbler, self.y_tumbler = int(0.703125 * screen_width), int(0.729166 * screen_height)  # Координаты тумблера начала сканирования
        self.x_search, self.y_search = int(0.328125 * screen_width), int(0.527777 * screen_height)  # Координаты кнопки "ПОИСК"

        self.searching_active = False
        self.ahk.add_hotkey(keyname="f3", callback=self.manager)
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
        if self.searching_active == False: return
        self.win.activate()
        sleep(0.5)
        self.win.send("x")
        sleep(1)
        r, g, b = pyautogui.pixel(self.x_signal, self.y_signal)  # Цвет индикатора НЕнайденного сигнала
        print(f"Начальный цвет индикатора: [R:{r} G:{g} B:{b}]")
        s_color_summ = r + g + b  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала
        s = [".", "..", "...", "...."]
        i = 0
        while self.searching_active:
            sleep(1.5)
            r, g, b = pyautogui.pixel(self.x_signal, self.y_signal)
            if r + g + b > s_color_summ:
                print(strftime("\n[%H:%M:%S]", localtime()), end=": ")
                print(f"Сигнал найден!\nЦвет индикатора: [R:{r} G:{g} B:{b}]")
                winsound.MessageBeep()
                self.burn_signal()
                print("Поиск окончен")
                self.searching_active = False
                break
            else:
                print("Поиск" + s[i], end="\r")
                sys.stdout.flush()
                self.reopen_suck()
                if i == 3:
                    i = 0
                    print("Поиск     ", end="\r")
                else:
                    i += 1

    def burn_signal(self):
        print("Дошёл до перемещения")
        # Переключение на среднюю дистанцию
        pyautogui.moveTo(x=self.x_med_rad, y=self.y_med_rad, duration=0.5)
        self.win.click(x=self.x_med_rad, y=self.y_med_rad, blocking=True)
        # Запуск сканирования
        pyautogui.moveTo(x=self.x_tumbler, y=self.y_tumbler, duration=0.5)
        self.win.click(x=self.x_tumbler, y=self.y_tumbler, blocking=True)
        # Ожидание до 6 дальности
        sleep(14)#randint(2, 4) * 0.1 + 20)
        # Отключение сканирования
        self.win.click(x=self.x_tumbler, y=self.y_tumbler, blocking=True)
        # Нажатие на кнопку ПОИСК
        pyautogui.moveTo(x=self.x_search, y=self.y_search, duration=0.5)
        self.win.click(x=self.x_search, y=self.y_search, blocking=True)
        print("Переместил")

    def reopen_suck(self):
        self.win.send("x")
        sleep(2)
        self.win.send("x")


def main():
    SignalFinder()


if __name__ == "__main__":
    print(
        """
    Скрипт для автоматического обнаружения сигналов STALCRAFT
    !!!!    Перед запуском закройте окно "САКv1"    !!!!
            ______________________________________
           |Для [Запуска]/[Остановки] нажмите "F3"|
            |Для [Завершения работы] нажмите "F4"|
             ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    """)
    main()
