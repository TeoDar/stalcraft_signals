"""
Автонажатие на кнопку Отправить в аукционе и ожидание 5 сек.
Когда влом выставлять кучу однотипных предметов.
"""

from os import environ
from ahk import AHK, Window
from time import sleep

PROGRAMFILES = environ["PROGRAMFILES"]
ahk_path = rf"{PROGRAMFILES}\AutoHotkey\v2\AutoHotkey.exe"
environ["AHK_PATH"] = ahk_path

x_sale, y_sale = 1120, 1060
x_ok, y_ok = 1283, 714


def sale(count=18):
    ahk = AHK()
    win: Window = ahk.win_get(title="STALCRAFT")
    print("Осталось продать предметов:")
    while count>0:
        print(f"\t{count}")
        ahk.mouse_move(x_sale, y_sale, speed=10, blocking=True)
        sleep(0.1)
        win.click(x_sale, y_sale, blocking=True)
        sleep(0.5)
        ahk.mouse_move(x_ok, y_ok, speed=10, blocking=True)
        sleep(0.1)
        win.click(x_ok, y_ok, blocking=True)
        sleep(5.1)
        count-=1


def main():
    sale()


if __name__=="__main__":
    main()