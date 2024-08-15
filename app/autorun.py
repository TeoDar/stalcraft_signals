"""
Автоматический бег по нажатию Alt
Статья подсказка:
https://pythonhint.com/post/8830992746003799/simulate-key-press-at-hardware-level-windows
Коды клавиш:
https://learn.microsoft.com/ru-ru/windows/win32/inputdev/virtual-key-codes
"""

from time import sleep, time
import win32api
import win32con
from multiprocessing import Process


class Runner:
    def __init__(self) -> None:
        self.RUNNING = False
        self.process = Process(target=self.run)

    def start_stop(self):
        if not self.RUNNING:
            print("Запуск автобега")
            self.process = Process(target=self.run)
            self.RUNNING = True
            # Запуск процесса снова
            self.process.start()
        else:
            print("Остановка автобега")
            self.RUNNING = False
            # Удаление процесса
            self.process.terminate()
            self.stop()

    def run(self):
        win32api.keybd_event(win32con.VK_LSHIFT, 0, 0, 0)
        while True:
            sleep(0.1)
            win32api.keybd_event(0x57, 0, 0, 0)

    def stop(self):
        win32api.keybd_event(win32con.VK_LSHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)


def main():
    while True:
        print("Ожидаю нажатия Alt для включения автобега", time())
        if win32api.GetAsyncKeyState(win32con.VK_LMENU) < 0:
            print("Автобег включен")
            win32api.keybd_event(win32con.VK_LSHIFT, 0, 0, 0)
            while True:
                sleep(0.1)
                win32api.keybd_event(0x57, 0, 0, 0)
                if win32api.GetAsyncKeyState(win32con.VK_LMENU) < 0:
                    win32api.keybd_event(win32con.VK_LSHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
                    break
        sleep(0.1)


if __name__ == "__main__":
    main()
