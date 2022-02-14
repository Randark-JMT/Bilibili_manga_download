import random

download_path = './B站漫画下载'
cookie_file = './B站漫画下载/cookie.txt'
url_ImageToken = 'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web'
url_GetImageIndex = 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web'
url_GetEpisode = 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web'
url_ComicDetail = "https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json;charset=UTF-8",
    "origin": 'https://manga.bilibili.com',
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.61 Safari/537.36",
    "cookie": ""
}
headers_cdn = {
    'Host': 'manga.hdslb.com',
    'Origin': 'https://manga.bilibili.com',
}


def get_cookie():
    with open(cookie_file, "r") as f:
        cookie_raw = f.read()
        sessdata_w = cookie_raw.find("SESSDATA")
        headers["cookie"] = cookie_raw[sessdata_w:sessdata_w + 9] + cookie_raw[sessdata_w + 10:sessdata_w + 42]
        print(headers["cookie"])
