from tkinter import tix, StringVar
# from tkinter import END
from tkinter.scrolledtext import ScrolledText
from download_gui import download_main, download_purchase_status
from settings import cookie_file
from download_gui import main_gui_log_insert

TCL_ALL_EVENTS = 0


class MainGUI:
    def __init__(self, w):
        self.root = w
        self.exit = -1
        # 窗口建立
        manga_window = w.winfo_toplevel()
        manga_window.wm_protocol("WM_DELETE_WINDOW", lambda self_self=self: self.quitcmd())
        manga_window.minsize(800, 600)  # 最小尺寸
        manga_window.maxsize(800, 600)  # 最大尺寸
        manga_window.title('Bilibili漫画下载    V1.2    仅限Mox内部使用')
        balloon_massage = tix.Balloon(w)
        # 窗口元素对齐
        gui_interval_left: int = 25
        gui_interval_up: int = 10
        gui_interval_each: int = 35

        # 用户SESSDATA输入框
        self.manga_sessdata_label = tix.Label(manga_window, text='用户SESSDATA=', font=('Arial', 12))
        self.manga_sessdata_label.place(x=gui_interval_left + 7, y=gui_interval_up)
        manga_sessdata_entry_text = StringVar()
        self.manga_sessdata_entry = tix.Entry(manga_window, show=None, font=('Arial', 14), exportselection=0, width=25, text='test', textvariable=manga_sessdata_entry_text)
        self.manga_sessdata_entry.place(x=180, y=gui_interval_up)
        balloon_massage.bind_widget(self.manga_sessdata_entry, balloonmsg='从浏览器的开发者工具中获取到的cookie数据')
        file = open(cookie_file, 'r')
        manga_sessdata_entry_text.set(file.read())
        file.close()

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
        self.manga_log_output = ScrolledText(manga_window, width=111, height=38, state='disabled')
        self.manga_log_output.place(x=0, y=gui_interval_up + gui_interval_each * 3)

        # 开始按钮
        manga_range_button = tix.Button(manga_window, width=20, height=2, font=('Arial', 14), command=self.main_gui_start, text='开始', )
        manga_range_button.place(x=470, y=gui_interval_up + gui_interval_each)
        balloon_massage.bind_widget(manga_range_button, balloonmsg='点击即可开始搜索下载')

        # 检查购买情况
        manga_check_button = tix.Button(manga_window, width=13, height=1, font=('Arial', 14), command=self.main_gui_check, text='检查购买', )
        manga_check_button.place(x=470, y=gui_interval_up - 5)
        balloon_massage.bind_widget(manga_check_button, balloonmsg='检查购买情况')

        # 更新cookie文件数据
        manga_check_button = tix.Button(manga_window, width=13, height=1, font=('Arial', 14), command=self.main_cookie_renovate, text='更新cookie储存', )
        manga_check_button.place(x=627, y=gui_interval_up - 5)
        balloon_massage.bind_widget(manga_check_button, balloonmsg='点击此按钮可更新软件缓存文件中的cookie数据')

        # 中止按钮
        manga_stop_button = tix.Button(manga_window, width=6, height=2, font=('Arial', 14), command=self.main_gui_stop, text='停止', )
        manga_stop_button.place(x=704, y=gui_interval_up + gui_interval_each)
        balloon_massage.bind_widget(manga_stop_button, balloonmsg='STOP')

        # 进度条
        # TODO 在界面增加一个进度条

    # 获取输入数据,开始任务
    def main_gui_start(self):
        sessdata = self.manga_sessdata_entry.get()
        manga_id = self.manga_id_entry.get()
        manga_range = self.manga_range_entry.get()
        download_main(manga_id, manga_range, sessdata, self.manga_log_output)

    # 获取输入数据，检查购买情况
    def main_gui_check(self):
        sessdata = self.manga_sessdata_entry.get()
        manga_id = self.manga_id_entry.get()
        download_purchase_status(manga_id, sessdata, self.manga_log_output)

    # cookie文件数据写入
    def main_cookie_renovate(self):
        file = open(cookie_file, 'w')
        sessdata = self.manga_sessdata_entry.get()
        file.write(sessdata)
        file.close()
        main_gui_log_insert('cookie数据储存成功\n', self.manga_log_output)

    # 终止下载
    def main_gui_stop(self):
        self.destroy()
        self.exit = 0

    def quitcmd(self):
        self.exit = 0

    def mainloop(self):
        found_event = 1
        while self.exit < 0 and found_event > 0:
            found_event = self.root.tk.dooneevent(TCL_ALL_EVENTS)

    def destroy(self):
        self.root.destroy()
