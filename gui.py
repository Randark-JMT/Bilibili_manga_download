from tkinter import tix
# from tkinter import END
from tkinter.scrolledtext import ScrolledText
from download_gui import download_gui

TCL_ALL_EVENTS = 0


class MainGUI:
    def __init__(self, w):
        self.root = w
        self.exit = -1
        # 窗口建立
        manga_window = w.winfo_toplevel()
        manga_window.wm_protocol("WM_DELETE_WINDOW", lambda self_self=self: self.quitcmd())
        # window.geometry('500x300')
        manga_window.minsize(800, 600)  # 最小尺寸
        manga_window.maxsize(800, 600)  # 最大尺寸
        manga_window.title('Bilibili漫画下载    V1.1    Mox.moe内部使用')
        balloon_massage = tix.Balloon(w)
        # 窗口元素对齐
        gui_interval_left: int = 25
        gui_interval_up: int = 10
        gui_interval_each: int = 30

        # 用户SESSDATA输入框
        self.manga_sessdata_label = tix.Label(manga_window, text='用户SESSDATA=', font=('Arial', 12))
        self.manga_sessdata_label.place(x=gui_interval_left + 7, y=gui_interval_up)
        self.manga_sessdata_entry = tix.Entry(manga_window, show=None, font=('Arial', 14), exportselection=0, width=25)
        self.manga_sessdata_entry.place(x=180, y=gui_interval_up)
        balloon_massage.bind_widget(self.manga_sessdata_entry, balloonmsg='从浏览器的开发者工具中获取到的cookie数据')

        # 漫画ID输入框
        self.manga_id_label = tix.Label(manga_window, text='漫画ID=', font=('Arial', 12))
        self.manga_id_label.place(x=gui_interval_left + 80, y=gui_interval_up + gui_interval_each)
        self.manga_id_entry = tix.Entry(manga_window, show=None, font=('Arial', 14), exportselection=0, width=25)
        self.manga_id_entry.place(x=180, y=gui_interval_up + gui_interval_each)
        balloon_massage.bind_widget(self.manga_id_entry, balloonmsg='B站漫画链接中”mc”后面的5位数数字')

        # 漫画章节数据输入框
        self.manga_range_label = tix.Label(manga_window, text='下载的章节范围为：', font=('Arial', 12))
        self.manga_range_label.place(x=gui_interval_left, y=gui_interval_up + gui_interval_each * 2)
        self.manga_range_entry = tix.Entry(manga_window, show=None, font=('Arial', 14), exportselection=0, width=25)
        self.manga_range_entry.place(x=180, y=gui_interval_up + gui_interval_each * 2)
        balloon_massage.bind_widget(self.manga_range_entry, balloonmsg='输入0为下载全部，单章直接输入，连续下载用“-”，可用逗号隔开，\n如“12，16-18”表示下载12，16，17，18话')

        # 控制台输出
        self.manga_range_output = ScrolledText(manga_window, width=111, height=38)
        self.manga_range_output.place(x=0, y=gui_interval_up + gui_interval_each * 3)
        # manga_range_output_scroll = tix.Scrollbar(w, orient="vertical", command=manga_range_output.yview, )
        # manga_range_output_scroll.grid()

        # 开始按钮
        manga_range_button = tix.Button(manga_window, width=25, height=3, font=('Arial', 14), command=self.main_gui_start, text='开始', )
        manga_range_button.place(x=500, y=gui_interval_up)
        balloon_massage.bind_widget(manga_range_button, balloonmsg='点击即可开始搜索下载')
        # 进度条
        # TODO 在界面增加一个进度条

    # 获取输入数据,开始任务
    def main_gui_start(self):
        print(0)
        # self.manga_range_output.insert("insert", "python\n")
        sessdata = self.manga_sessdata_entry.get()
        manga_id = self.manga_id_entry.get()
        manga_range = self.manga_range_entry.get()
        download_gui(manga_id, manga_range, sessdata, self.manga_range_output)
    def quitcmd(self):
        self.exit = 0

    def mainloop(self):
        found_event = 1
        while self.exit < 0 and found_event > 0:
            found_event = self.root.tk.dooneevent(TCL_ALL_EVENTS)

    def destroy(self):
        self.root.destroy()
