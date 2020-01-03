# as part of your imports
if sys.platform.lower().startswith('win'):
    import ctypes

    def hideConsole():
        """
        Hides the console window in GUI mode. Necessary for frozen application, because
        this application support both, command line processing AND GUI mode and theirfor
        cannot be run via pythonw.exe.
        """

        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            # if you wanted to close the handles...
            #ctypes.windll.kernel32.CloseHandle(whnd)

    def showConsole():
        """Unhides console window"""
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 1)

...
# later, in main()
# hide console window, but only under Windows and only if app is frozen
            if sys.platform.lower().startswith('win'):
                if getattr(sys, 'frozen', False):
                    hideConsole()