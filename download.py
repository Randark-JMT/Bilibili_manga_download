import json
import os
import requests
import traceback
import time
import settings
from decode import decode_index_data, get_image_url
from settings import headers, url_ComicDetail, download_path, url_GetEpisode, url_GetImageIndex
from PySide6.QtWidgets import *


def get_purchase_status(comic_id: int, log_output: QTextBrowser):  # 购买情况查询
    # cookie 数据读取
    settings.get_cookie()
    data_rt = []
    # 数据解析
    try:
        res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    except Exception:
        log_output.append("--*--*--*-- 错误 获取漫画购买情况时出错 --*--*--*--")
        errmsg = traceback.format_exc(limit=3).split("\n")[-2].split(": ")
        log_output.append(errmsg[0] + "-" + errmsg[1])
        if errmsg[0] == "requests.exceptions.SSLError":
            log_output.append("请检查网络连接情况，并尝试关闭网络代理")
        return None
    data = json.loads(res.text)['data']
    data_rt.append([data['id'], data['title']])
    manga_list = data['ep_list']
    manga_list.reverse()
    for ep in manga_list:
        data_rt_per = []
        if ep['short_title'].isnumeric():
            data_rt_per.append('第' + ep['short_title'].rjust(3, '0') + '话—' + ep['title'])
            if ep['is_locked']:
                data_rt_per.append('：未购买')
            else:
                data_rt_per.append('：已购买')
        else:
            data_rt_per.append(ep['short_title'] + '—' + ep['title'])
            if ep['is_locked']:
                data_rt_per.append('：未购买')
            else:
                data_rt_per.append('：已购买')
        data_rt.append(data_rt_per)
    return data_rt


def download_manga_episode(episode_id: int, root_path: str, log_output: QTreeWidgetItem):  # ID-索引下载漫画模块
    try:
        res = requests.post(url_GetEpisode, json.dumps({"id": episode_id}), headers=headers)
    except Exception:
        msg = QTreeWidgetItem(log_output)
        msg.setText(0, "错误 下载漫画时出错")
        errmsg = traceback.format_exc(limit=3).split("\n")[-2].split(": ")
        msg.setText(1, errmsg[0] + "\n" + errmsg[1])
        return None
    data = json.loads(res.text)
    short_title = data['data']['short_title']
    title = short_title + '_' + data['data']['title']
    comic_id = data['data']['comic_id']
    root = QTreeWidgetItem(log_output)
    root.setText(0, '正在下载：' + title)

    # 获取索引文件cdn位置
    res = requests.post(url_GetImageIndex, json.dumps({"ep_id": episode_id}), headers=headers)
    data = json.loads(res.text)
    index_url = 'https://manga.hdslb.com' + data['data']['path']
    # print('获取索引文件cdn位置:', index_url)
    # 获取索引文件
    res = requests.get(index_url)
    # 解析索引文件
    pics = decode_index_data(comic_id, episode_id, res.content)
    # 文件储存
    ep_path = os.path.join(root_path, title)
    if not os.path.exists(ep_path):
        os.makedirs(ep_path)
    for i, e in enumerate(pics):
        url = get_image_url(e)
        child = QTreeWidgetItem(root)
        child.setText(0, '第' + str(i + 1) + '页    ' + e)
        child.setText(1, "下载成功")
        res = requests.get(url)
        with open(os.path.join(ep_path, str(i + 1).rjust(3, '0') + '.jpg'), 'wb+') as f:
            f.write(res.content)
            pass
        if i % 4 == 0 and i != 0:
            # time.sleep(1)
            pass


# 主下载模块
def download_main(self, comic_id: int, download_range: str, log_output: QTreeWidget):
    # cookie 数据读取
    with open(settings.cookie_file, "r") as f:
        headers['cookie'] = f.read()
    if download_range == '0':
        download_manga_all(comic_id, log_output)
        return None
    download_range.replace('，', ',')  # 防呆设计
    download_range.replace('—', '-')
    download_range.replace(" ", "")
    # 对用户输入的章节数据进行读取
    start = int(0)  # 范围下载第一位
    destination = int(0)  # 范围下载第二位
    state = False  # 是否为批量下载
    frequency = int(0)  # 第几位字符
    for letter in download_range:
        frequency = frequency + 1
        if letter == ',':
            if not state:
                section = start
                download_manga_each(self, comic_id, section, log_output)
                continue
            else:
                download_manga_range(self, comic_id, start, destination, log_output)
                # 初始化控制变量
                start = int(0)
                destination = int(0)
                state = False
        elif letter == '-':
            state = True
            continue
        else:
            if not state:
                start = start * 10 + int(letter)
                continue
            if state:
                destination = destination * 10 + int(letter)
                continue
    # 检查是否为最后一块
    if frequency == len(download_range):
        if not state:
            section = start
            download_manga_each(self, comic_id, section, log_output)
        else:
            download_manga_range(comic_id, start, destination, log_output)


def download_manga_range(self, comic_id: int, start: int, destination: int, log_output: QTreeWidget):
    section: int = start
    while section <= destination:
        download_manga_each(self, comic_id, section, log_output)
        section += 1


def download_manga_all(comic_id: int, text_output: QTreeWidget):
    # url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    # 漫画下载目录检查&创建
    root_path = os.path.join(download_path, comic_title)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    manga_list = data['ep_list']
    manga_list.reverse()
    # TODO 日志中尝试增加进度条
    for ep in manga_list:
        # 检查付费章节是否购买
        if not ep['is_locked']:
            main_gui_log_insert('正在下载第:' + ep['short_title'] + ep['title'] + '\n', text_output)
            download_manga_episode(ep['id'], root_path, text_output)
        else:
            break


def download_manga_each(self, comic_id: int, section: int, text_output: QTreeWidget):
    QMessageBox.information(self, "提示", "正在下载：" + str(comic_id) + "\t" + str(section) + "\n注意，此操作需要一定耗时，请耐心等待，不要随便关闭窗口\n开发者正在尝试解决此问题，请谅解。")
    # url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    # 漫画下载目录检查&创建
    root_path = os.path.join(download_path, comic_title)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    manga_list = data['ep_list']
    manga_list.reverse()
    for ep in manga_list:
        # 检查付费章节是否购买
        if not ep['is_locked']:
            # section_temp = int(ep['short_title'])
            if ep['short_title'] == str(section):
                # main_gui_log_insert('正在下载第' + ep['short_title'].rjust(3, '0') + '话：' + ep['title'] + '\n', text_output)
                download_manga_episode(ep['id'], root_path, text_output)
            else:
                print(ep['short_title'])


