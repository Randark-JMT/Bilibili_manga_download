download_path = './B站漫画下载'
cookie_file = './B站漫画下载/cookie.txt'
url_ImageToken = str('https://www.bilibilicomics.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web')
url_GetImageIndex = str('https://www.bilibilicomics.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web')
url_GetEpisode = str('https://www.bilibilicomics.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web')
url_ComicDetail = str("https://www.bilibilicomics.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web")
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json;charset=UTF-8",
    "origin": 'https://www.bilibilicomics.com',
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.61 Safari/537.36",
    "cookie": "SESSDATA=d31a5ac5%2C1641642785%2C43b27%2A71"
}
headers_cdn = {
    'Host': 'manga.hdslb.com',
    'Origin': 'https://www.bilibilicomics.com',
}
