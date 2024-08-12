"""
Автоматическое разбиение стака по 1 объекту и продажа через каждые 5 сек.
"""

from os import environ
from ahk import AHK, Window
from ahk.directives import NoTrayIcon
from time import sleep
from sale_after_5_sec import *

PROGRAMFILES = environ["PROGRAMFILES"]
ahk_path = rf"{PROGRAMFILES}\AutoHotkey\v2\AutoHotkey.exe"
environ["AHK_PATH"] = ahk_path
ahk = AHK(directives=[NoTrayIcon])

# Дельта координаты Х для ввода количества разделения
one_delta_x = 130
# Дельта координаты Х для смещение к подтверждению разделения
ok_delta_x = 155
# Координаты первой левой ячейки в окне Аукционера
x, y = 700, 670


def main():
    count_items = int(input("Введите количество предметов на разделение: "))
    win: Window = ahk.win_get(title="STALCRAFT")
    ahk.mouse_move(x, y, blocking=True)
    sleep(0.1)
    win.click(x, y, blocking=True)
    i = count_items
    while i > 1:
        ahk.key_down("Ctrl")
        sleep(0.1)
        ahk.mouse_move(x, y, blocking=True)
        sleep(0.1)
        win.click(x, y, blocking=True)
        sleep(0.1)
        ahk.key_release("Ctrl")
        sleep(0.1)
        ahk.mouse_move(x - one_delta_x, y, blocking=True)
        sleep(0.1)
        win.click(x - one_delta_x, y, blocking=True)
        sleep(0.1)
        ahk.key_press("Backspace")
        sleep(0.1)
        ahk.key_press("Backspace")
        sleep(0.1)
        ahk.key_press("1")
        sleep(0.1)
        ahk.mouse_move(x + ok_delta_x, y, blocking=True)
        sleep(0.1)
        win.click(blocking=True)
        sleep(0.1)
        i -= 1
    
    sale(count_items)


if __name__ == "__main__":
    main()
