import json
import time
import requests
from PySide6.QtWidgets import *
from settings import headers, url_ComicDetail


def download_purchase_status(comic_id: int, sessdata: str, log_output: QTreeWidget):  # 购买情况查询
    # 设置信息输出的根节点
    root = QTreeWidgetItem(log_output)
    root.setText(0, comic_id)
    root.setText(1, "查询时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)

    # 数据解析
    data = json.loads(res.text)['data']
    comic_title = data['title']
    time.sleep(1)
    manga_list = data['ep_list']
    manga_list.reverse()
    for ep in manga_list:
        child = QTreeWidgetItem()
        if ep['short_title'].isnumeric():
            child.setText(0, '第' + ep['short_title'].rjust(3, '0') + '话：' + ep['title'])
            if ep['is_locked']:
                child.setText(1, '未购买')
            else:
                child.setText(1, '已购买')
        else:
            child.setText(0, ep['short_title'] + '：' + ep['title'] + '----->')
            if ep['is_locked']:
                child.setText(1, '未购买')
            else:
                child.setText(1, '已购买')
        root.addChild(child)
        QApplication.processEvents()
