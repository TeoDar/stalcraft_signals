"""Методы для получения координат мыши по нажатию на ЛКМ"""

import win32api
import time

from ctypes import windll, wintypes, byref


def get_cursor_pos():
    cursor = wintypes.POINT()
    windll.user32.GetCursorPos(byref(cursor))
    return (cursor.x, cursor.y)


def get_lkm_pos():
    lkm_clicked = win32api.GetKeyState(0x01)
    if lkm_clicked < 0:
        (get_cursor_pos())
    time.sleep(0.1)


def main():
    while True:
        get_lkm_pos()


if __name__ == "__main__":
    main()
