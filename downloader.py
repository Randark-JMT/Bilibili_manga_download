import json
import requests
from settings import headers, url_ComicDetail


def download_purchase_status(comic_id: int, sessdata: str):  # 购买情况查询
    # cookie 数据读取
    sessdata = 'SESSDATA=' + sessdata
    headers['cookie'] = sessdata
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    data_rt = []
    # 数据解析
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
