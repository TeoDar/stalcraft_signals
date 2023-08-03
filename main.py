###################################################################################################
# Введите номер монитора на котором запущена игра вашего экрана:
screen = 0
###################################################################################################
import subprocess
import sys, os
import winsound
import pyautogui, keyboard
from screeninfo import get_monitors
from time import sleep, strftime, localtime
from multiprocessing import Process, set_start_method
from ahk import AHK
from ahk.directives import NoTrayIcon


#set_start_method('spawn')
ahk = AHK()#directives=[NoTrayIcon])
print('Создал AHK')
win = ahk.win_get("STALCRAFT")
if not win:
    exit("[Ошибка]: Не найдено окно STALCRAFT или игра не запущена")
screen_width, screen_height = [(x.width, x.height) for x in get_monitors()][screen]  # 2560 1440 В моём случае

last_proc: Process = None
x_signal, y_signal = int(0.359375 * screen_width), int(0.368055 * screen_height)  # Координаты индикатора найденного сигнала
x_med_rad, y_med_rad = int(0.5625 * screen_width), int(0.7361 * screen_height)  # Координаты кнопки "Средняя"
x_tumbler, y_tumbler = int(0.703125 * screen_width), int(0.729166 * screen_height)  # Координаты тумблера начала сканирования
x_search, y_search = int(0.328125 * screen_width), int(0.527777 * screen_height)  # Координаты кнопки "ПОИСК"


def reopen_suck(win):
    win.send("x")
    sleep(2)
    win.send("x")


def burn_signal():
    print('Дошёл до перемещения')
    ahk.mouse_move(x=x_med_rad, y=y_med_rad, speed=10, blocking=True)
    ahk.click()
    sleep(0.1)
    ahk.mouse_move(x=x_signal, y=y_signal, speed=10, blocking=True)
    ahk.click()
    sleep(0.1)
    ahk.mouse_move(x=x_signal, y=y_signal, speed=10, blocking=True)
    ahk.click()
    sleep(0.1)
    print('Переместил')


def searching():
    win.activate()
    win.send("x")
    sleep(0.5)
    r, g, b = pyautogui.pixel(x_signal, y_signal)  # Цвет индикатора НЕнайденного сигнала
    print(f"Начальный цвет индикатора: [R:{r} G:{g} B:{b}]")
    s_color_summ = r + g + b  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала
    s = ['.','..','...','....']
    i = 0
    while True:
        sleep(1.5)
        r, g, b = pyautogui.pixel(x_signal, y_signal)
        if r + g + b > s_color_summ:
            print(strftime("\n[%H:%M:%S]", localtime()), end=": ")
            print(f"Сигнал найден!\nЦвет индикатора: [R:{r} G:{g} B:{b}]")
            winsound.MessageBeep()
            burn_signal()
            break
        else:
            sys.stdout.write("\r" + "Поиск" + s[i])
            sys.stdout.flush()
            reopen_suck(win)
            if i == 3:i = 0
            else: i+=1
    print('Поиск окончен')


def start_stop():
    """Функция управляющия потоками для регулирования запуска/остановки"""
    global last_proc
    if last_proc is None: last_proc = Process(target=searching)
    if last_proc.is_alive():
        last_proc.terminate()
        last_proc.join()
        last_proc = None
        print("\n[Поиск остановлен]")
    else:
        print("[Запуск поиска]")
        last_proc.start()


def main():
    print('Запуск мэйна')
    global last_proc
    keyboard.add_hotkey("f3", start_stop)
    keyboard.wait("f4")
    if last_proc:
        last_proc.terminate()
    subprocess.run(['taskkill', '/F', '/IM', 'AutoHotkey.exe'])


if __name__ == "__main__":
    print(
        """
    Скрипт для автоматического обнаружения сигналов STALCRAFT
    !!!!    Перед запуском закройте окно "САКv1"    !!!!
            ______________________________________
           |Для [Запуска]/[Остановки] нажмите "F3"|
            |Для [Завершения работы] нажмите "F4"|
             ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
"""
    )
    main()
