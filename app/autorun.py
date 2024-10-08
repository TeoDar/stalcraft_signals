"""
Автоматический бег по нажатию Alt
Статья подсказка:
https://pythonhint.com/post/8830992746003799/simulate-key-press-at-hardware-level-windows
Коды клавиш:
https://learn.microsoft.com/ru-ru/windows/win32/inputdev/virtual-key-codes
"""

from time import sleep
import win32api, win32con, win32gui


keys = {
    "Left mouse button": 0x01,
    "Right mouse button": 0x02,
    "Middle mouse button": 0x04,
    "Mouse button 5": 0x05,
    "Mouse button 6": 0x06,
    "BACKSPACE": 0x08,
    "TAB": 0x09,
    "CAPS LOCK": 0x14,
    "PAGE UP": 0x21,
    "PAGE DOWN": 0x22,
    "END": 0x23,
    "HOME": 0x24,
    "LEFT": 0x25,
    "UP": 0x26,
    "RIGHT": 0x27,
    "DOWN": 0x28,
    "INSERT": 0x2D,
    "DELETE": 0x2E,
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "A": 0x41,
    "B": 0x42,
    "C": 0x43,
    "D": 0x44,
    "E": 0x45,
    "F": 0x46,
    "G": 0x47,
    "H": 0x48,
    "I": 0x49,
    "J": 0x4A,
    "K": 0x4B,
    "L": 0x4C,
    "M": 0x4D,
    "N": 0x4E,
    "O": 0x4F,
    "P": 0x50,
    "Q": 0x51,
    "R": 0x52,
    "S": 0x53,
    "T": 0x54,
    "U": 0x55,
    "V": 0x56,
    "W": 0x57,
    "X": 0x58,
    "Y": 0x59,
    "Z": 0x5A,
    "Left WIN": 0x5B,
    "Right WIN": 0x5C,
    "NUMPAD0": 0x60,
    "NUMPAD1": 0x61,
    "NUMPAD2": 0x62,
    "NUMPAD3": 0x63,
    "NUMPAD4": 0x64,
    "NUMPAD5": 0x65,
    "NUMPAD6": 0x66,
    "NUMPAD7": 0x67,
    "NUMPAD8": 0x68,
    "NUMPAD9": 0x69,
    "MULTIPLY": 0x6A,
    "ADD": 0x6B,
    "SEPARATOR": 0x6C,
    "SUBTRACT": 0x6D,
    "DECIMAL": 0x6E,
    "DIVIDE": 0x6F,
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "NUMLOCK": 0x90,
    "Left SHIFT": 0xA0,
    "Right SHIFT": 0xA1,
    "Left CONTROL": 0xA2,
    "Right CONTROL": 0xA3,
    "Left ALT": 0xA4,
    "Right ALT": 0xA5,
}


def run(key: str = keys["Left ALT"]):
    print("Ожидаю нажатия Alt для включения автобега")
    st_window = win32gui.FindWindow(None, "STALCRAFT")
    while True:
        if win32api.GetAsyncKeyState(key) < 0 and win32gui.GetForegroundWindow() == st_window:
            print("Автобег включен")
            win32api.keybd_event(win32con.VK_LSHIFT, 0, 0, 0)
            win32api.keybd_event(0x57, 0, 0, 0)
            sleep(0.5)
            while True:
                if win32api.GetAsyncKeyState(key) < 0 or win32gui.GetForegroundWindow() != st_window:
                    print("Автобег выключен")
                    win32api.keybd_event(win32con.VK_LSHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
                    sleep(0.4)
                    break
        sleep(0.1)


if __name__ == "__main__":
    run()
