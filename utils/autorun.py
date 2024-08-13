"""
Автоматический двойной клик, для быстрой продажи кучи хлама.
Активация по хоткею Alt
"""

from os import environ
from time import sleep
from ahk import AHK, Window
from ahk.directives import NoTrayIcon

PROGRAMFILES = environ["PROGRAMFILES"]
ahk_path = rf"{PROGRAMFILES}\AutoHotkey\v2\AutoHotkey.exe"
environ["AHK_PATH"] = ahk_path
ahk = AHK(directives=[NoTrayIcon(apply_to_hotkeys_process=True)])

running = False

def autorun():
    global running
    if running:
        running = False
        ahk.key_release("Shift")
        sleep(0.1)
        ahk.key_release("w")
        return
    else:
        running = True
    while running:
        ahk.key_down("Shift")
        sleep(0.1)
        ahk.key_down("w")


def main():
    ahk.add_hotkey("Alt", callback=autorun)
    ahk.start_hotkeys()
    ahk.block_forever()


if __name__=="__main__":
    main()