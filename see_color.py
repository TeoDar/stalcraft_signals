###################################################################################################
####            Скрипт для вывода цвета под курсором или в заданных координатах                ####
###################################################################################################

import pyautogui

print("Нажми Ctrl-C чтобы выйти.")
x, y = (688, 398)  # Координаты заданы вручную
pyautogui.moveTo(x, y)

try:
    while True:
        # x, y = pyautogui.position() # Для определения цвета под курсовом
        r, g, b = pyautogui.pixel(x, y)
        ColorStr = "R: " + str(r).rjust(4) + " G: " + str(g).rjust(4) + " B: " + str(b).rjust(4)
        print(ColorStr, end="")
        print("\b" * len(ColorStr), end="", flush=True)
except KeyboardInterrupt:
    print("\n")
