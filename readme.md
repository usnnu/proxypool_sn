爬虫IP代理池
=========

### 下载安装
* 下载源码
···git clone git@github.com:usnnu/proxypool.git···


* 安装依赖:

```shell
pip install -r requirements.txt
```

* 配置Config.ini:

```shell
[DB]
;Configure the database information # DB参数配置，这里使用的是redis
host = 127.0.0.1
port = 6379
password = ***

# spider选择，设置为1意为不使用这一spider
[ProxySpider_not_use]
freeProxyWallFirst = 1
freeProxyWallSecond = 1
freeProxyWallThird = 1

[API]
# API config http://127.0.0.1:5010
# The ip specified when starting the web API
ip = 0.0.0.0
# he port on which to run the web API
port = 8080

```

* 启动:
```shell
# 如果你的依赖已经安全完成并且具备运行条件,可以直接在Run下运行main.py
# 到Run目录下:
>>>python main.py
```
### 使用

　　启动过几分钟后就能看到抓取到的代理IP，你可以直接到数据库中查看，推荐一个[SSDB可视化工具](https://github.com/jhao104/SSDBAdmin)。

　　也可以通过api访问http://127.0.0.1:5010 查看。

* Api

| api | method | Description | arg|
| ----| ---- | ---- | ----|
| / | GET | api介绍 | None |
| /get | GET | 随机获取一个代理 | None|
| /status | GET | 查看代理数量 |None|
| /delete | GET | 删除代理  |proxy=host:ip|


### 项目参考文档：

  项目参考以下项目/文档，非常感谢作者的分享。
  1.https://github.com/jhao104/proxy_pool
  2.https://github.com/Germey/ProxyPool
