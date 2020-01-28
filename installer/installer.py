from project import app
import webview
import threading
import time
import os

import win32gui, win32con, win32console

print(os.getcwd())

def hide_console():
    print('hiding console')
    console = win32console.GetConsoleWindow()
    win32gui.ShowWindow(console , win32con.SW_HIDE)


def create_browser_window():
    webview.create_window('Installer', 'http://localhost:5000')
    webview.start(debug=True, gui='mshtml')

def start_server():
    app.run(host='127.0.0.1', port='5000', threaded=True)

if __name__ == '__main__':
    try:
        st =threading.Thread(target=start_server)
        st.daemon=True
        st.start()
        t = threading.Timer(1.5, hide_console)
        t.daemon =True
        t.start()
        create_browser_window()

    except Exception as e:
        print(e)
        input('press any key to exit')
