![程序图标](https://raw.githubusercontent.com/Randark-JMT/Bilibili_manga_download/dev-tkinker/main.ico "ico")
# B站外国区漫画下载器
此版本面对https://www.bilibilicomics.com/ 下载漫画<br />
哔哩哔哩漫画下载工具， 支持范围下载
## 项目特点
1：拥有图形界面（易用程度大幅度提升） <br />
2：支持多样的下载范围自定义 <br />
3：支持付费漫画下载（前提是已经购买的漫画）
## 如何获取软件
#### 1、下载源码
运行环境为：Python 3.x <br />
在cmd、powershell或BASH中输入此代码安装依赖：```pip3 install -r  requirements.txt```<br />
然后执行 ```python3 main.py```来运行程序
#### 2、直接运行exe版本
下载Releases中的exe文件直接运行<br />
注意：目前本软件只在Win10上，并安装有c++ 2015-2019依赖库时，才能完美运行
## 使用方法
请跟随气泡提示输入相关数据后运行
## 待办
TODO：界面性能优化（下载时界面卡顿）
_这个准备开多线程，在学了_<br />
TODO：界面添加一个双层进度条
_这个先研究一下需下载的文件数量_<br />
TODO：换一种界面框架
_准备同步开发一个基于pyQt框架的GUI，也在学_
## 其他项目引用
图片解析部分来自 https://github.com/flaribbit/bilibili-manga-spider <br />
下载逻辑参考 https://github.com/xuruoyu/bilibili_manga_downloader
