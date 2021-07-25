import os
import time
import requests
import json
from decode import decode_index_data, get_image_url
from settings import download_path, headers
from tkinter.scrolledtext import ScrolledText


def download_gui(id_input: int, download_range: str, sessdata: str, text_output: ScrolledText):
    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    download_manga_title_gui(id_input, text_output)

    if download_range == '0':
        download_manga_all_gui(id_input, text_output)
        exit(0)
    # 防呆设计
    download_range.replace('，', ',')
    # download_range.replace('-', '-')
    text_output.insert("insert", download_range + '\n')
    text_output.see('insert')
    text_output.update()

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
                download_manga_each_gui(id_input, section, text_output)
                continue
            else:
                section = start
                while section <= destination:
                    # print(section)
                    download_manga_each_gui(id_input, section, text_output)
                    section += 1
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
    # TODO 将范围下载的函数独立出来
    # 检查是否为最后一块
    if frequency == len(download_range):
        if not state:
            section = start
            download_manga_each_gui(id_input, section, text_output)
        else:
            section = start
            while section <= destination:
                # print(section)
                download_manga_each_gui(id_input, section, text_output)
                section = section + 1
    text_output.insert("insert", '下载完毕' + '\n')
    text_output.see('insert')
    text_output.update()


# 全部漫画下载模块
def download_manga_all_gui(comic_id: int, text_output: ScrolledText):
    url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url, json.dumps({"comic_id": comic_id}), headers=headers)
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
            # text_output.insert('insert', 'test\n')
            text_output.insert("insert", '正在下载第:' + ep['short_title'] + ep['title'] + '\n')
            text_output.see('insert')
            text_output.update()
            download_manga_episode_gui(ep['id'], root_path, text_output)


# 逐章节下载模块
def download_manga_each_gui(comic_id: int, section: int, text_output: ScrolledText):
    url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url, json.dumps({"comic_id": comic_id}), headers=headers)
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
            if int(ep['short_title']) == section:
                # print('正在下载章节:', ep['short_title'], ep['title'])
                text_output.insert("insert", '正在下载第' + ep['short_title'].rjust(3, '0') + '话：' + ep['title'] + '\n')
                text_output.see('insert')
                text_output.update()
                download_manga_episode_gui(ep['id'], root_path, text_output)


# ID~索引下载漫画模块
def download_manga_episode_gui(episode_id: int, root_path: str, text_output: ScrolledText):
    url = str('https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web')
    res = requests.post(url, json.dumps({"id": episode_id}), headers=headers)
    data = json.loads(res.text)
    # comic_title = data['data']['comic_title']
    short_title = data['data']['short_title']
    # title = comic_title + '_' + short_title + '_' + data['data']['title']
    title = short_title + '_' + data['data']['title']
    comic_id = data['data']['comic_id']
    # text_output.insert("insert", '正在下载：' + title + '\n')
    # text_output.see('insert')
    # text_output.update()

    # 获取索引文件cdn位置
    url = str('https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web')
    res = requests.post(url, json.dumps({"ep_id": episode_id}), headers=headers)
    data = json.loads(res.text)
    index_url = 'https://manga.hdslb.com' + data['data']['path']
    # print('获取索引文件cdn位置:', index_url)
    # 获取索引文件
    res = requests.get(index_url)
    # 解析索引文件
    pics = decode_index_data(comic_id, episode_id, res.content)
    # print(pics)
    ep_path = os.path.join(root_path, title)
    if not os.path.exists(ep_path):
        os.makedirs(ep_path)
    for i, e in enumerate(pics):
        url = get_image_url(e)
        text_output.insert("insert", '第' + str(i + 1) + '页    ' + e + '\n')
        text_output.see('insert')
        text_output.update()
        res = requests.get(url)
        with open(os.path.join(ep_path, str(i + 1).rjust(3, '0') + '.jpg'), 'wb+') as f:
            f.write(res.content)
            pass
        if i % 4 == 0 and i != 0:
            time.sleep(2)


def download_manga_title_gui(comic_id: int, text_output: ScrolledText):
    url = str("https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
    res = requests.post(url, json.dumps({"comic_id": comic_id}), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    text_output.insert("insert", '正在下载的漫画为：' + comic_title + '\n')
    text_output.see('insert')
    text_output.update()
