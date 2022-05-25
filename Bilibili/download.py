import json
import os
import requests
import traceback
from Bilibili.decode import decode_index_data, get_image_url
from Bilibili.settings import headers, url_ComicDetail, download_path, url_GetEpisode, url_GetImageIndex, get_cookie


# TODO 加入代理设置


def get_data(url, data, headers_user, log_out):  # 网络数据获取
    try:
        res = requests.post(url, data, headers=headers_user)
    except Exception:
        log_out("0x00", "--+--+--+-- 错误 网络通信时出错 --+--+--+--")
        errmsg = traceback.format_exc(limit=3).split("\n")[-2].split(": ")
        log_out(errmsg[0] + "-" + errmsg[1])
        if errmsg[0] == "requests.exceptions.SSLError":
            log_out("0x00", "请检查网络连接情况，并尝试关闭网络代理")
        return None
    return res


def get_purchase_status(comic_id: int, log_out):  # 购买情况查询
    # cookie 数据读取
    get_cookie()
    data_rt = []
    # 数据解析
    data_re = get_data(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers, log_out)
    if data_re is None:
        return None
    try:
        data = json.loads(data_re.text)['data']
    except Exception:
        log_out("0x00", "--*--*--*-- 错误 漫画数据解析时出错 --*--*--*--\n请检查输入的数据是否正确")
        return None
    data_rt.append([data['id'], data['title']])
    manga_list = data['ep_list']
    manga_list.reverse()
    ep_order: int = 1
    for ep in manga_list:
        data_rt_per = []
        if ep['short_title'].isnumeric():
            data_rt_per.append("#" + str(ep_order).rjust(3, "0") + "#  " + '第' + ep['short_title'].rjust(3, '0') + '话—' + ep['title'])
            if ep['is_locked']:
                data_rt_per.append('：未购买')
            else:
                data_rt_per.append('：已购买')
        else:
            data_rt_per.append("#" + str(ep_order).rjust(3, "0") + "#  " + ep['short_title'] + '—' + ep['title'])
            if ep['is_locked']:
                data_rt_per.append('：未购买')
            else:
                data_rt_per.append('：已购买')
        data_rt.append(data_rt_per)
        ep_order += 1
    return data_rt


def download_manga_episode(episode_id: int, root_path: str, log_out):  # ID-索引下载漫画模块
    data_re = get_data(url_GetEpisode, json.dumps({"id": episode_id}), headers, log_out)
    data = json.loads(data_re.text)
    short_title = data['data']['short_title']
    title = short_title + '_' + data['data']['title']
    comic_id = data['data']['comic_id']
    log_out("0x00", '正在下载：' + title)
    # 获取索引文件cdn位置
    res = requests.post(url_GetImageIndex, json.dumps({"ep_id": episode_id}), headers=headers)
    data = json.loads(res.text)
    index_url = 'https://manga.hdslb.com' + data['data']['path']
    # log_out('获取索引文件cdn位置:' + index_url)
    # 获取索引文件
    res = requests.get(index_url)
    # 解析索引文件
    pics = decode_index_data(comic_id, episode_id, res.content)
    # 文件储存
    ep_path = os.path.join(root_path, str(title).replace(" ", ""))
    if not os.path.exists(ep_path):
        os.makedirs(ep_path)
    for i, e in enumerate(pics):
        url = get_image_url(e)
        res = requests.get(url)
        with open(os.path.join(ep_path, str(i + 1).rjust(3, '0') + '.jpg'), 'wb+') as f:
            f.write(res.content)
            pass
        if i % 4 == 0 and i != 0:
            # time.sleep(1)
            pass
        log_out("0x00", '第' + str(i + 1).rjust(3, "0") + '页  "下载成功"    ' + e)
    log_out("0x00", "")


def download_main(comic_id: int, download_range: str, log_out):  # 主下载模块
    # cookie 数据读取
    from settings import get_cookie
    get_cookie()
    data_re = get_data(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers, log_out)
    comic_info = json.loads(data_re.text)['data']
    log_out("0x00", "正在下载 " + str(comic_info['id']) + "-" + str(comic_info['title']))
    download_range = download_range.replace('，', ',')  # 防呆设计
    download_range = download_range.replace('—', '-')
    download_range = download_range.replace(" ", "")
    if download_range == '0':
        data = json.loads(data_re.text)['data']
        comic_title = data['title']
        # 漫画下载目录检查&创建
        root_path = os.path.join(download_path, comic_title)
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        manga_list = data['ep_list']
        manga_list.reverse()
        # TODO 全部下载的进度条
        for ep in manga_list:
            # 检查付费章节是否购买
            if not ep['is_locked']:
                # log_out('正在下载第:' + ep['short_title'] + ep['title'])
                download_manga_episode(ep['id'], root_path, log_out)
            else:
                log_out("0x00", '第' + data['short_title'].rjust(3, '0') + '话—' + data['title'] + " 未购买，已跳过")
                continue
        log_out("0xe3", "--*--*--*-- 下载任务已完成 --*--*--*--")
        return None
    # 对用户输入的章节数据进行读取
    download_range = download_range.split(",")
    for chunk in download_range:
        chunk = chunk.split("-")
        if len(chunk) == 2:
            if not chunk[0].isnumeric() or not chunk[1].isnumeric():
                log_out("0xe3", "下载范围输入错误，请检查输入")
                return None
            elif int(chunk[0]) >= int(chunk[1]):
                log_out("0xe3", "下载范围输入错误，请检查输入")
                return None
            else:
                section = int(chunk[0])
                while section <= int(chunk[1]):
                    download_manga_each(comic_id, section, log_out)
                    section += 1
        elif chunk[0] == "":
            continue
        else:
            download_manga_each(comic_id, int(chunk[0]), log_out)
    log_out("0xe3", "--*--*--*-- 下载任务已完成 --*--*--*--")
    return None


def download_manga_each(comic_id: int, section: int, log_out):
    res = requests.post(url_ComicDetail, json.dumps({"comic_id": comic_id}), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    # 漫画下载目录检查&创建
    root_path = os.path.join(download_path, comic_title)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    manga_list = data['ep_list']
    manga_list.reverse()
    manga_section = manga_list[section - 1]
    if not manga_section['is_locked']:  # 检查付费章节是否购买
        # TODO 单章下载的进度条
        download_manga_episode(manga_section['id'], root_path, log_out)
    else:
        log_out("0x00", '第' + data['short_title'].rjust(3, '0') + '话—' + data['title'] + " 未购买，已跳过")
