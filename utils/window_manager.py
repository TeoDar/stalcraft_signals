import re
import win32gui
import win32com.client 


class WindowMgr:
    """ Encapsulates calls to the winapi for window management
        Forces context window to take focus
        Based on: 
         - https://stackoverflow.com/questions/2090464/python-window-activation
         - https://stackoverflow.com/questions/14295337/win32gui-setactivewindow-error-the-specified-procedure-could-not-be-found
    """

    def __init__ (self):
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)
        return self

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        return self

    def set_foreground(self):
        """put the window in the foreground"""
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')  # left shift key sent, this shifts focus from current window
        win32gui.SetForegroundWindow(self._handle)