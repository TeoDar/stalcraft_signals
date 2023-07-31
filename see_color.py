import pyautogui, sys

print("Press Ctrl-C to quit.")
x, y = (688, 398)
pyautogui.moveTo(x, y)

try:
    while True:
        #x, y = pyautogui.position()
        r,g,b = pyautogui.pixel(x, y)
        ColorStr = "R: " + str(r).rjust(4) + " G: " + str(g).rjust(4) + " B: " + str(b).rjust(4)
        print(ColorStr, end="") # positionStr
        print("\b" * len(ColorStr), end="", flush=True)
except KeyboardInterrupt:
    print("\n")
