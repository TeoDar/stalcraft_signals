from time import sleep, strftime, localtime
import winsound
import pyautogui, keyboard
from multiprocessing import Process, Manager


last_proc: Process
x_signal, y_signal = 688, 398  # Координаты индикатора найденного сигнала
x_tumbler, y_tumbler = 1350, 790  # Координаты тумблера начала сканирования
x_search_btn, y_search_btn = 630, 570  # Координаты кнопки "ПОИСК"
r, g, b = 95, 114, 92  # Цвет индикатора НЕнайденного сигнала
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
    '''Функция управляющия потоками для регулирования запуска/остановки'''
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
