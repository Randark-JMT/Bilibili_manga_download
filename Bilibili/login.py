# -*- coding: utf-8 -*-
import qrcode
from threading import Thread
import time
import requests
from io import BytesIO
from PIL import Image
import json

import setting
import settings

requests.packages.urllib3.disable_warnings()


class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


def islogin(log_out):
    from setting import properties_global
    settings.headers["Cookie"] = "SESSDATA=" + str(settings.property_bilibili_get("cookie", properties_global))
    loginurl = requests.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=settings.headers).json()
    if loginurl['code'] == 0:
        log_out('Cookies值有效，' + loginurl['data']['uname'] + '，已登录！')
        return True
    else:
        log_out('Cookies值已经失效，请重新扫码登录！')
        return False


def bzlogin(log_out):
    from setting import properties_global
    status = islogin(log_out)
    if not status:
        getlogin = requests.get('https://passport.bilibili.com/qrcode/getLoginUrl', headers=settings.headers).json()
        loginurl = requests.get(getlogin['data']['url'], headers=settings.headers).url
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
            qrcodedata = requests.post(tokenurl, data={'oauthKey': oauthKey, 'gourl': 'https://www.bilibili.com/'}, headers=settings.headers_login)
            if qrcodedata.json()['data'] == -4:
                log_out('二维码未失效，请扫码！')
            elif qrcodedata.json()['data'] == -5:
                log_out('已扫码，请确认！')
            elif qrcodedata.json()['data'] == -2:
                log_out('二维码已失效，请重新运行！')
            elif qrcodedata.json()['status']:
                log_out('已确认，登入成功！')
                log_out(requests.get(qrcodedata.json()['data']['url'], headers=settings.headers))
                sessdata = str(qrcodedata.cookies.get_dict(".Bilibili.com")["SESSDATA"])
                log_out(sessdata)
                settings.property_bilibili_put("cookie", sessdata, properties_global)
                break
            else:
                log_out('其他：', qrcodedata.text)
            time.sleep(1)
        log_out("请关闭二维码窗口")


if __name__ == '__main__':
    text = setting.settintfile_read()
    if len(text) > 0:
        setting.properties_global = json.loads(text)


    def log_out_test(message, code=None):
        if code is None:
            print(message)


    bzlogin(log_out_test)
