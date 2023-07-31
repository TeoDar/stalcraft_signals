from time import sleep
import mouse
import winsound
import pyautogui, keyboard, pydirectinput
from multiprocessing import Process, Manager
# По цветам:
# x:690 y:400
# R:95  G:114  B:92 - Стандартный цвет
# Цвета светлее:
# R:23  G:191 B:15
# R:151 G:221 B:148
# R:20  G:153 B:13


last_proc: Process
x = 688
y = 398 
r, g, b = 95, 114, 92
s_color_summ = r+g+b

def searching(SEARCHING_ACTIVE: Manager):
    while SEARCHING_ACTIVE.value:
        sleep(0.5)
        #signal_founded = pyautogui.locateOnScreen('./test/1.png', region=(660,370, 720, 430), confidence=0.95)
        r,g,b = pyautogui.pixel(x, y)
        if r+g+b > s_color_summ:
            print(f'Сигнал найден!\nR:{r} G:{g} B:{b}')
            winsound.MessageBeep()
            pyautogui.moveTo(630, 580)
            sleep(2)
            pyautogui.moveTo(x, y)
            SEARCHING_ACTIVE.value = False
        # else:
        #     print('Сигнал не найден...')
        #     print(f'R:{r} G:{g} B:{b}')


def start_stop(SEARCHING_ACTIVE: Manager):
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


def cancel():
    exit(0)


def main():
    manager = Manager()
    SEARCHING_ACTIVE = manager.Value("SEARCHING_ACTIVE", False)
    print('Для запуска/остановки поиска нажмите "F3"\nДля завершения нажмине "F4"')
    keyboard.add_hotkey("f3", start_stop, args=(SEARCHING_ACTIVE,))
    keyboard.wait("f4")
    last_proc.terminate()


if __name__ == "__main__":
    main()

    
#x:660 y:370
    #############
    #           #
    #           #
    #           #
    #           #
    #############
                #x:720 y:430
# x:1080 y:800 - Средняя
# x:1350 y:790 - Сканирование
# x:630  y:580 - Поиск
