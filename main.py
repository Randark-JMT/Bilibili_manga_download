from gui import MainGUI
from tkinter.tix import Tk
from settings import cookie_file, download_path
import os

if __name__ == '__main__':
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(cookie_file):
        file = open(cookie_file, 'w')
        file.close()
    manga_window = Tk()
    manga_window.wm_geometry('800x600')
    manga_window.wm_resizable(False, False)
    balloon = MainGUI(manga_window)
    balloon.mainloop()
    balloon.destroy()
    manga_window.mainloop()
    exit()
