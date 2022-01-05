import os
import requests
import json
from decode import decode_index_data, get_image_url
from settings import download_path, headers, url_ComicDetail, url_GetImageIndex, url_GetEpisode
from tkinter.scrolledtext import ScrolledText
from time import sleep


# 主下载模块
def download_main(comic_id: int, download_range: str, sessdata: str, text_output: ScrolledText):
    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    download_manga_title(comic_id, text_output)
    if download_range == '0':
        download_manga_all(comic_id, text_output)
        main_gui_log_insert('下载完毕' + '\n\n\n', text_output)
        exit(0)
    # 防呆设计
    download_range.replace('，', ',')
    download_range.replace('—', '-')

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
                download_manga_each(comic_id, section, text_output)
                continue
            else:
                download_manga_range(comic_id, start, destination, text_output)
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
            download_manga_each(comic_id, section, text_output)
        else:
            download_manga_range(comic_id, start, destination, text_output)
    main_gui_log_insert('下载完毕' + '\n\n\n', text_output)


# 范围下载漫画模块
def download_manga_range(comic_id: int, start: int, destination: int, text_output: ScrolledText):
    section: int = start
    while section <= destination:
        download_manga_each(comic_id, section, text_output)
        section += 1


# 全部漫画下载模块
def download_manga_all(comic_id: int, text_output: ScrolledText):
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
            main_gui_log_insert('其余章节未下载' + '\n', text_output)
            break


# 单章节下载模块
def download_manga_each(comic_id: int, section: int, text_output: ScrolledText):
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
                main_gui_log_insert('正在下载第' + ep['short_title'].rjust(3, '0') + '话：' + ep['title'] + '\n', text_output)
                download_manga_episode(ep['id'], root_path, text_output)
            else:
                print(ep['short_title'])
    main_gui_log_insert('其余章节未下载' + '\n', text_output)


# ID~索引下载漫画模块
def download_manga_episode(episode_id: int, root_path: str, text_output: ScrolledText):
    # url = str('https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web')
    res = requests.post(url_GetEpisode, json.dumps({"id": episode_id}), headers=headers)
    data = json.loads(res.text)
    # comic_title = data['data']['comic_title']
    short_title = data['data']['short_title']
    # title = comic_title + '_' + short_title + '_' + data['data']['title']
    title = short_title + '_' + data['data']['title']
    comic_id = data['data']['comic_id']
    main_gui_log_insert('正在下载：' + title + '\n', text_output)

    # 获取索引文件cdn位置
    # url = str('https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web')
    res = requests.post(url_GetImageIndex, json.dumps({"ep_id": episode_id}), headers=headers)
    data = json.loads(res.text)
    index_url = 'https://manga.hdslb.com' + data['data']['path']
    # print('获取索引文件cdn位置:', index_url)
    # 获取索引文件
    res = requests.get(index_url)
    # 解析索引文件
    pics = decode_index_data(comic_id, episode_id, res.content)
    # print(pics)
    # 文件储存
    ep_path = os.path.join(root_path, title)
    if not os.path.exists(ep_path):
        os.makedirs(ep_path)
    for i, e in enumerate(pics):
        url = get_image_url(e)
        main_gui_log_insert('第' + str(i + 1) + '页    ' + e + '\n', text_output)
        res = requests.get(url)
        with open(os.path.join(ep_path, str(i + 1).rjust(3, '0') + '.jpg'), 'wb+') as f:
            f.write(res.content)
            # sleep(10)
            pass
        if i % 4 == 0 and i != 0:
            sleep(1)


# 漫画标题获取
def download_manga_title(comic_id: int, text_output: ScrolledText):
    # url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    main_gui_log_insert('正在下载的漫画为：' + comic_title + '\n', text_output)


# 日志输出(带刷新界面)
def main_gui_log_insert(msg: str, text_output: ScrolledText):
    text_output.configure(state='normal')
    text_output.insert('insert', msg)
    text_output.see('insert')
    text_output.configure(state='disabled')
    text_output.update()


# 购买情况查询
def download_purchase_status(comic_id: int, sessdata: str, text_output: ScrolledText):
    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    # url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    main_gui_log_insert('正在查询漫画：' + comic_title + '的购买情况\n', text_output)
    sleep(1)
    manga_list = data['ep_list']
    manga_list.reverse()
    for ep in manga_list:
        if ep['short_title'].isnumeric():
            main_gui_log_insert('第' + ep['short_title'].rjust(3, '0') + '话：' + ep['title'] + '----->', text_output)
            if ep['is_locked']:
                main_gui_log_insert('未购买\n', text_output)
            else:
                main_gui_log_insert('已购买\n', text_output)
        else:
            main_gui_log_insert(ep['short_title'] + '：' + ep['title'] + '----->', text_output)
            if ep['is_locked']:
                main_gui_log_insert('未购买\n', text_output)
            else:
                main_gui_log_insert('已购买\n', text_output)
