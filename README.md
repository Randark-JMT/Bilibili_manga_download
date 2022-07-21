![程序图标](https://raw.githubusercontent.com/Randark-JMT/Bilibili_manga_download/dev-tkinker/main.ico "ico")
# *JMT* 漫画下载器
哔哩哔哩漫画下载工具， 支持范围下载

***新版本浴火重生（Tkinter的火），但是说明文件还没写好，自己摸索着用用看吧！***

~~欸，就是懒，懒得写~~

## 项目特点
1：拥有图形界面（易用程度大幅度提升） <br />
2：支持多样的下载范围自定义 <br />
3：支持付费漫画下载（前提是已经购买的漫画）

## 使用说明
漫画id内填入B漫的id，如链接为`https://manga.bilibili.com/detail/mc28241` ,则id为`28241`
漫画范围，填`0`则是会尝试下载所有章节，`14-16`表示下载14到16，`58`表示下载序号为58，可用逗号隔开不同的下载范围

## TODO
> 就目前而言，请使用release中的二进制版本，仓库中的代码还在进行开发，并非最终版本。预计未来会加上其他平台的支持，如鹰角网络
- 增加高级设置，如手动输入SESSDATA和网络代理 <br />
- 优化扫码登录的方案 <br />
- 整合设置数据为json对象，并生成设置文件 <br />
- 尝试引入双线程下载加速
- 写使用说明

## 其他项目引用
图片解析部分来自 https://github.com/flaribbit/bilibili-manga-spider <br />
下载逻辑参考 https://github.com/xuruoyu/bilibili_manga_downloader
