###################################################################################################
# Введите номер монитора на котором запущена игра вашего экрана:
screen = 0
lamps = 6  # На какой лампочке останавливать поиск
###################################################################################################
import subprocess
import sys, os
from tkinter import messagebox
import winsound
import pyautogui, keyboard
from screeninfo import get_monitors
from time import sleep, strftime, localtime
from traceback import format_exc as exc
from ahk import AHK
from ahk.directives import NoTrayIcon
from sys import exit
PROGRAMFILES = os.environ["PROGRAMFILES"]
os.environ["AHK_PATH"] = f"{PROGRAMFILES}\AutoHotkey\AutoHotkey.exe"


screen_width, screen_height = [(x.width, x.height) for x in get_monitors()][screen]
x_signal, y_signal = int(0.359375 * screen_width), int(0.368055 * screen_height)  # Координаты индикатора найденного сигнала
x_small_rad, y_small_rad = int(0.51875 * screen_width), int(0.73611 * screen_height)  # Координаты кнопки "Малая"
x_med_rad, y_med_rad = int(0.5625 * screen_width), int(0.7361 * screen_height)  # Координаты кнопки "Средняя"
x_m_tumbler, y_m_tumbler = int(0.703125 * screen_width), int(0.729166 * screen_height)  # Координаты тумблера начала сканирования
x_s_ready, y_s_ready = int(0.33 * screen_width), int(0.44 * screen_height)  # Координаты окна сигнализирующего о найденном сигнале
x_search, y_search = int(0.328125 * screen_width), int(0.528 * screen_height)  # Координаты кнопки "ПОИСК"


x_first, y_first = int(0.2 * screen_width), int(0.25 * screen_height)  # Координаты 1 ячейки инвентаря противника
x_inventory, y_first_inventory = int(0.177 * screen_width), int(0.12 * screen_height)  # Координаты 1 ячейки инвентаря противника


class SignalFinder:
    def __init__(self) -> None:
        global lamps
        self.lamps = lamps
        self.ahk = AHK(directives=[NoTrayIcon(apply_to_hotkeys_process=True)])
        self.win = self.ahk.win_get("STALCRAFT")
        if not self.win:
            exit("[Ошибка]: Не найдено окно STALCRAFT или игра не запущена")

        self.searching_active = False
        #keyboard.add_hotkey(hotkey="v", callback=self.get_first)
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
        rs, gs, bs = pyautogui.pixel(x_signal, y_signal)  # Цвет индикатора НЕнайденного сигнала
        print(strftime("\n[%H:%M:%S]", localtime()), end=": ")
        print(f"Начальный цвет индикатора: [R:{rs} G:{gs} B:{bs}]")
        s_color_summ = rs + gs + bs  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала
        s = [".", "..", "...", "...."]
        i = 0
        while self.searching_active:
            for k in range(6):
                sleep(0.25)
                r, g, b = pyautogui.pixel(x_signal, y_signal)
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
        pyautogui.moveTo(x=x_med_rad, y=y_med_rad)  # , duration=0.2)
        self.win.click(x=x_med_rad, y=y_med_rad, blocking=True)
        # pyautogui.moveTo(x=x_small_rad, y=y_small_rad)#, duration=0.2)
        # self.win.click(x=x_small_rad, y=y_small_rad, blocking=True)
        # Запуск сканирования
        pyautogui.moveTo(x=x_m_tumbler, y=y_m_tumbler)  # , duration=0.2)
        self.win.click(x=x_m_tumbler, y=y_m_tumbler, blocking=True)
        # Ожидание до 6 дальности
        for i in range(11):
            if i <= self.lamps:
                sleep(1.5)
        # Отключение сканирования
        pyautogui.moveTo(x=x_m_tumbler, y=y_m_tumbler)
        self.win.click(x=x_m_tumbler, y=y_m_tumbler, blocking=True)
        # Нажатие на кнопку ПОИСК
        sleep(0.15)
        if self.check_founded():
            pyautogui.moveTo(x=x_search, y=y_search)  # , duration=0.2)
            self.win.click(x=x_search, y=y_search, blocking=True)
            return True
        else:
            return False

    def check_founded(self) -> bool:
        r, g, b = pyautogui.pixel(x_s_ready, y_s_ready)
        if r + g + b >= 100:
            return True
        print("Похоже сигнал не найден. Цвет окна:", r, g, b)
        winsound.PlaySound("./sounds/fail.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        sleep(3)
        # self.timer()
        return False

    def incr_lumps(self):
        self.lamps += 1
        if self.lamps > 10:
            self.lamps = 10
        print(f"Сканирование до [{self.lamps}] лампочки")

    @staticmethod
    def timer():
        for remaining in range(270, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:3d} Cекунд до появления следующего сигнала".format(remaining))
            sys.stdout.flush()
            sleep(1)
        print("\n")

    def decr_lumps(self):
        self.lamps -= 1
        if self.lamps < 1:
            self.lamps = 1
        print(f"Сканирование до [{self.lamps}] лампочки")

    def reopen_suck(self):
        if self.searching_active == False:
            return
        self.win.send("x")
        sleep(1.5)
        if self.searching_active == False:
            return
        self.win.send("x")

    def get_first(self):
        print('Забрал 1 предмет')
        sleep(0.15)
        pyautogui.moveTo(x_first, y_first)
        self.win.click(click_count=2)


def main():
    try:
        SignalFinder()
    except:
        messagebox.showinfo(message=exc(),icon="question")


if __name__ == "__main__":
    print(
        """
    Скрипт для автоматического обнаружения сигналов STALCRAFT
    !!!!    Перед запуском закройте окно "САКv1"    !!!!
            ______________________________________
           |Для [Запуска]/[Остановки] нажмите "F3"|
            |Для [Завершения работы] нажмите "F4"|
             ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
  +/- для уменьшения или увеличения лампочек до остановки поиска
    """
    )
    main()
