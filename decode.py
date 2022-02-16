import json
import numpy as np
import zipfile
import io
from settings import url_ImageToken
import requests

from settings import headers


def decode_index_data(season_id: int, episode_id: int, buf):
    u = [66, 73, 76, 73, 67, 79, 77, 73, 67]
    length = len(u)
    e = buf[length:]
    # print(buf)
    _e = []
    for i in range(len(e)):
        _e.append(e[i])
    e = np.uint8(_e)
    # print(e)
    n = [0, 0, 0, 0, 0, 0, 0, 0]
    n = np.array(n, dtype='uint8')
    n[0] = episode_id
    n[1] = episode_id >> 8
    n[2] = episode_id >> 16
    n[3] = episode_id >> 24
    n[4] = season_id
    n[5] = season_id >> 8
    n[6] = season_id >> 16
    n[7] = season_id >> 24
    # print(n)
    _n = 0
    r = len(e)
    while _n < r:
        e[_n] = e[_n] ^ n[_n % 8]
        _n = _n + 1
    # print("解密后：")
    # print(e)
    ret = bytes(e)
    # print(ret)
    z = zipfile.ZipFile(io.BytesIO(ret), 'r')
    j = z.read('index.dat')
    # print(j)
    # pprint(json.loads(j)['pics'])
    return json.loads(j)['pics']


# 单文件链接解析
def get_image_url(img_url):
    # url = str('https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web')
    # 获取图片token
    res = requests.post(url_ImageToken, json.dumps({"urls": json.dumps([img_url])}), headers=headers)
    data = json.loads(res.text)['data'][0]
    url = data['url'] + '?token=' + data['token']
    return url
