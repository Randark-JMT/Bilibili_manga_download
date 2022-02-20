# -*- coding: utf-8 -*-
# -*- author:Mute-a -*-
# -*- link:https://blog.csdn.net/qq_18303993/article/details/114481841 -*-
import qrcode
import settings
import traceback
from threading import Thread
import time
import requests
from io import BytesIO
import http.cookiejar as cookielib
from PIL import Image

requests.packages.urllib3.disable_warnings()

headers = {'User-Agent': settings.headers["user-agent"], 'Referer': "https://www.bilibili.com/"}
headerss = {'User-Agent': settings.headers["user-agent"], 'Host': 'passport.bilibili.com', 'Referer': "https://passport.bilibili.com/login"}


class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


def islogin(session, log_out):
    try:
        session.cookies.load(ignore_discard=True)
    except Exception:
        pass
    try:
        loginurl = session.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
    except Exception:
        log_out("--+--+--+-- 错误 网络通信时出错 --+--+--+--")
        errmsg = traceback.format_exc(limit=3).split("\n")[-2].split(": ")
        log_out(errmsg[0] + "-" + errmsg[1])
        if errmsg[0] == "requests.exceptions.ProxyError":
            log_out("请检查网络连接情况，并尝试关闭网络代理")
        log_out("0xe1")
        return None
    if loginurl['code'] == 0:
        log_out('Cookies值有效，' + loginurl['data']['uname'] + '，已登录！')
        return session, True
    else:
        log_out('Cookies值已经失效，请重新扫码登录！')
        return session, False


def bzlogin(log_out):
    """
    在用户的临时文件夹内生成登陆二维码，并用默认程序打开二维码
    """
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename=settings.cookie_file)
    session, status = islogin(session, log_out)  # status为是否登录的储存位
    if not status:
        try:
            getlogin = session.get('https://passport.bilibili.com/qrcode/getLoginUrl', headers=headers).json()
        except Exception:
            log_out("--+--+--+-- 错误 网络通信时出错 --+--+--+--")
            errmsg = traceback.format_exc(limit=3).split("\n")[-2].split(": ")
            log_out(errmsg[0] + "-" + errmsg[1])
            if errmsg[0] == "requests.exceptions.ProxyError":
                log_out("请检查网络连接情况，并尝试关闭网络代理")
            log_out("0xe1")
            return None
        loginurl = requests.get(getlogin['data']['url'], headers=headers).url
        oauthKey = getlogin['data']['oauthKey']
        qr = qrcode.QRCode()
        qr.add_data(loginurl)
        img = qr.make_image()
        a = BytesIO()
        img.save(a, 'png')
        png = a.getvalue()
        a.close()
        showpng(png).start()
        while 1:
            qrcodedata = session.post('https://passport.bilibili.com/qrcode/getLoginInfo', data={'oauthKey': oauthKey, 'gourl': 'https://www.bilibili.com/'}, headers=headerss).json()
            if '-4' in str(qrcodedata['data']):
                log_out('二维码未失效，请及时扫码！')
            elif '-5' in str(qrcodedata['data']):
                log_out('已扫码，请确认！')
            elif '-2' in str(qrcodedata['data']):
                log_out('二维码已失效，请重新运行程序！')
            elif 'True' in str(qrcodedata['status']):
                log_out('已确认，登入成功！')
                session.get(qrcodedata['data']['url'], headers=headers)
                islogin(session, log_out)
                break
            else:
                log_out('其他：' + qrcodedata)
            time.sleep(2)
        session.cookies.save()
    log_out("0xe1")


if __name__ == '__main__':
    bzlogin(print)
