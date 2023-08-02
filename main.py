###################################################################################################
# Введите разрешение вашего экрана:
screen_width, scrin_height = 2560, 1440
###################################################################################################


from time import sleep, strftime, localtime
import winsound
import pyautogui, keyboard
from multiprocessing import Process, Manager

delta_x = screen_width/1920
delta_y = scrin_height/1080

last_proc: Process
x_signal, y_signal = int(688 * delta_x), int(398 * delta_y)  # Координаты индикатора найденного сигнала
x_tumbler, y_tumbler = int(1350 * delta_x), int(790 * delta_y)  # Координаты тумблера начала сканирования
x_search_btn, y_search_btn = int(630 * delta_x), int(570 * delta_y)  # Координаты кнопки "ПОИСК"
r, g, b = pyautogui.pixel(x_signal, y_signal)  # Цвет индикатора НЕнайденного сигнала
s_color_summ = r + g + b  # Вычисление суммы светов для дальнейшего сравнения и обнаружения найденного сигнала


def searching(SEARCHING_ACTIVE: Manager):
    while SEARCHING_ACTIVE.value:
        sleep(0.5)  # Задержка между проверками
        r, g, b = pyautogui.pixel(x_signal, y_signal)
        if r + g + b > s_color_summ:
            print(strftime("[%H:%M:%S]", localtime()), end=": ")
            print(f"Сигнал найден!\nR:{r} G:{g} B:{b}")
            winsound.MessageBeep()
            pyautogui.moveTo(x_tumbler, y_tumbler)
            sleep(26.5)
            pyautogui.moveTo(x_search_btn, y_search_btn)
            SEARCHING_ACTIVE.value = False
        # else:
        #     print('Сигнал не найден...')
        #     print(f'R:{r} G:{g} B:{b}')


def start_stop(SEARCHING_ACTIVE: Manager):
    """Функция управляющия потоками для регулирования запуска/остановки"""
    global last_proc
    search_proc = Process(target=searching, args=(SEARCHING_ACTIVE,))
    if SEARCHING_ACTIVE.value:
        print("Остновка поиска")
        print('Для запуска/остановки поиска нажмите "F3"\nДля завершения нажмине "F4"')
        SEARCHING_ACTIVE.value = False
        last_proc.terminate()
    else:
        print("Запуск поиска")
        SEARCHING_ACTIVE.value = True
        search_proc.start()
        last_proc = search_proc


def main():
    global last_proc
    manager = Manager()
    SEARCHING_ACTIVE = manager.Value("SEARCHING_ACTIVE", False)
    print('Для запуска/остановки поиска нажмите "F3"\nДля завершения нажмине "F4"')
    keyboard.add_hotkey("f3", start_stop, args=(SEARCHING_ACTIVE,))
    keyboard.wait("f4")
    last_proc.terminate()


if __name__ == "__main__":
    main()


# x:660 y:370
#############
#           #
#           #
#           #
#           #
#############
# x:720 y:430
# x:1080 y:800 - Средняя
# x:1350 y:790 - Сканирование
# x:630  y:580 - Поиск
