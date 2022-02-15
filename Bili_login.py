# -*- coding: utf-8 -*-
# -*- author:Mute-a -*-
# -*- link:https://blog.csdn.net/qq_18303993/article/details/114481841 -*-
import qrcode
import settings
from threading import Thread
import time
import requests
from io import BytesIO
import http.cookiejar as cookielib
from PIL import Image
import os

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


def islogin(session, log_append):
    try:
        session.cookies.load(ignore_discard=True)
    except Exception:
        pass
    loginurl = session.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
    if loginurl['code'] == 0:
        log_append('Cookies值有效，' + loginurl['data']['uname'] + '，已登录！')
        return session, True
    else:
        log_append('Cookies值已经失效，请重新扫码登录！')
        return session, False


def bzlogin(log_append):
    """
    在用户的临时文件夹内生成登陆二维码，并用默认程序打开二维码
    """
    if not os.path.exists(settings.cookie_file):
        with open(settings.cookie_file, 'w') as f:
            f.write("")
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename=settings.cookie_file)
    session, status = islogin(session, log_append)
    if not status:
        getlogin = session.get('https://passport.bilibili.com/qrcode/getLoginUrl', headers=headers).json()
        loginurl = requests.get(getlogin['data']['url'], headers=headers).url
        oauthKey = getlogin['data']['oauthKey']
        qr = qrcode.QRCode()
        qr.add_data(loginurl)
        img = qr.make_image()
        a = BytesIO()
        img.save(a, 'png')
        png = a.getvalue()
        a.close()
        t = showpng(png)
        t.start()
        tokenurl = 'https://passport.bilibili.com/qrcode/getLoginInfo'
        while 1:
            qrcodedata = session.post(tokenurl, data={'oauthKey': oauthKey, 'gourl': 'https://www.bilibili.com/'}, headers=headerss).json()
            # log_append(qrcodedata)
            if '-4' in str(qrcodedata['data']):
                log_append('二维码未失效，请扫码！')
            elif '-5' in str(qrcodedata['data']):
                log_append('已扫码，请确认！')
            elif '-2' in str(qrcodedata['data']):
                log_append('二维码已失效，请重新运行程序！')
            elif 'True' in str(qrcodedata['status']):
                log_append('已确认，登入成功！')
                session.get(qrcodedata['data']['url'], headers=headers)
                break
            else:
                log_append('其他：' + qrcodedata)
            time.sleep(2)
        session.cookies.save()


if __name__ == '__main__':
    bzlogin()
