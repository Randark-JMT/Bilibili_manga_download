import json
import os
import requests
import traceback
import time
from decode import decode_index_data, get_image_url
from settings import headers, url_ComicDetail, download_path, url_GetEpisode, url_GetImageIndex
from PySide6.QtWidgets import *


def get_purchase_status(comic_id: int, sessdata: str, log_output: QTreeWidget):  # 购买情况查询
    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    data_rt = []
    # 数据解析
    try:
        res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    except Exception:
        msg = QTreeWidgetItem(log_output)
        msg.setText(0, "错误 获取漫画购买情况时出错")
        errmsg = traceback.format_exc(limit=3).split("\n")[-2].split(": ")
        msg.setText(1, errmsg[0] + "\n" + errmsg[1])
        return None
    data = json.loads(res.text)['data']
    data_rt.append([data['id'], data['title']])
    manga_list = data['ep_list']
    manga_list.reverse()
    for ep in manga_list:
        data_rt_per = []
        if ep['short_title'].isnumeric():
            data_rt_per.append('第' + ep['short_title'].rjust(3, '0') + '话：' + ep['title'])
            if ep['is_locked']:
                data_rt_per.append('未购买')
            else:
                data_rt_per.append('已购买')
        else:
            data_rt_per.append(ep['short_title'] + '：' + ep['title'])
            if ep['is_locked']:
                data_rt_per.append('未购买')
            else:
                data_rt_per.append('已购买')
        data_rt.append(data_rt_per)
    return data_rt


def download_manga_episode(episode_id: int, root_path: str, log_output: QTreeWidget):  # ID-索引下载漫画模块
    # url = str('https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web')
    res = requests.post(url_GetEpisode, json.dumps({"id": episode_id}), headers=headers)
    data = json.loads(res.text)
    # comic_title = data['data']['comic_title']
    short_title = data['data']['short_title']
    # title = comic_title + '_' + short_title + '_' + data['data']['title']
    title = short_title + '_' + data['data']['title']
    comic_id = data['data']['comic_id']
    # main_gui_log_insert('正在下载：' + title + '\n', text_output)

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
        # main_gui_log_insert('第' + str(i + 1) + '页    ' + e + '\n', text_output)
        res = requests.get(url)
        with open(os.path.join(ep_path, str(i + 1).rjust(3, '0') + '.jpg'), 'wb+') as f:
            f.write(res.content)
            # sleep(10)
            pass
        if i % 4 == 0 and i != 0:
            time.sleep(1)
