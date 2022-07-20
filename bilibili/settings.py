version = "v1.4.4"
download_path = '../B站漫画下载'
setting_file = 'setting.json'
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
    "cookie": "",
    'Referer': "https://www.bilibili.com/"
}
headers_login = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    'Host': 'passport.bilibili.com',
    'Referer': "https://passport.bilibili.com/login"
}
headers_cdn = {
    'Host': 'manga.hdslb.com',
    'Origin': 'https://manga.bilibili.com',
}


def property_bilibili_put(key, value, properties):
    """
    在bilibili域内，保存一个属性。如果key不存在，则创建；存在，则覆盖。
    """
    from setting import property_put
    property_put(key, value, properties, domain="bilibili")


def property_bilibili_get(key, properties):
    """
    在bilibili域内，获取一个属性。如果不存在，则返回default。
    """
    from setting import property_get
    return property_get(key, properties, domain="bilibili")

def get_cookie():
    return None