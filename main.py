import ctypes
from gui import MainGUI
from tkinter.tix import Tk
from settings import cookie_file, download_path
import sys
import os

if __name__ == '__main__':
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(cookie_file):
        file = open(cookie_file, 'w')
        file.close()
    manga_window = Tk()
    manga_window.tk.call('tk', 'scaling', ScaleFactor / 75)
    manga_window.wm_geometry('900x600')
    manga_window.wm_resizable(False, False)
    manga_window.title('Bilibili漫画下载    V1.2.2    仅限Mox内部使用')
    manga_window.update()
    MainGUI(manga_window).mainloop()
    MainGUI(manga_window).destroy()
