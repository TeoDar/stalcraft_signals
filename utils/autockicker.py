"""
Автоматический двойной клик, для быстрой продажи кучи хлама.
Активация по хоткею Alt
"""

from os import environ
from ahk import AHK, Window
from ahk.directives import NoTrayIcon

PROGRAMFILES = environ["PROGRAMFILES"]
ahk_path = rf"{PROGRAMFILES}\AutoHotkey\v2\AutoHotkey.exe"
environ["AHK_PATH"] = ahk_path
ahk = AHK(directives=[NoTrayIcon(apply_to_hotkeys_process=True)])

clicking = False

def autosale():
    win: Window = ahk.win_get(title="STALCRAFT")
    global clicking
    if clicking:
        clicking = False
        return
    else:
        clicking = True
    while clicking:
        win.click(click_count=1)


def main():
    ahk.add_hotkey("Alt", callback=autosale)
    ahk.start_hotkeys()
    ahk.block_forever()


if __name__=="__main__":
    main()