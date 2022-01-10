import json
import requests
import traceback
from settings import headers, url_ComicDetail
from PySide6.QtWidgets import *


def get_purchase_status(comic_id: int, sessdata: str, log_output: QTreeWidget):  # 购买情况查询
    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    data_rt = []
    # 数据解析
    res = None
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
