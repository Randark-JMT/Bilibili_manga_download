from gui import MainGUI
from tkinter.tix import Tk
from settings import cookie_file
from os import path

if __name__ == '__main__':
    if not path.exists(cookie_file):
        file = open(cookie_file, 'w')
        file.close()
    manga_window = Tk()
    balloon = MainGUI(manga_window)
    balloon.mainloop()
    balloon.destroy()
    manga_window.mainloop()
    exit()
