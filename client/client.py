import logging
logger = logging.getLogger()
logger.disabled = True

import webview
import win32gui, win32con, win32console
import threading

def hide_console():
    print('hiding console')
    console = win32console.GetConsoleWindow()
    win32gui.ShowWindow(console , win32con.SW_HIDE)

t = threading.Timer(1, hide_console)
t.daemon =True
t.start()

webview.create_window('Umisoft', 'http://localhost:8989/login')
webview.start(gui='cef')#setting the gui is important


