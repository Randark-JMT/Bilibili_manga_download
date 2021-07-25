from gui import MainGUI
from tkinter.tix import Tk

if __name__ == '__main__':
    manga_window = Tk()
    balloon = MainGUI(manga_window)
    balloon.mainloop()
    balloon.destroy()
    manga_window.mainloop()
    exit()
