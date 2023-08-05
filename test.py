from time import sleep
import winsound
import pyautogui
from screeninfo import get_monitors


try:
    winsound.PlaySound('bfuzz_hit.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
except Exception as e:
    print(e)
sleep(2)
# screen = 0
# screen_width, screen_height = [(x.width, x.height) for x in get_monitors()][screen]
# x_s_ready, y_s_ready = int(0.33 * screen_width), int(0.44 * screen_height)  # Координаты окна сигнализирующего о найденном сигнале
# pyautogui.moveTo(x_s_ready, y_s_ready)

# def check_founded() -> bool:
#         for i in range(10):
#             r, g, b = pyautogui.pixel(x_s_ready+i, y_s_ready)
#             pyautogui.moveTo(x_s_ready, y_s_ready+i)
#             print(f'Проверка цвета иконки:', r, g, b, end='\r')
