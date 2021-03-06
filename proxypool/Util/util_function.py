#coding:utf-8

"""
----------------------------------------
    file name:
    description:
    
author:
    date:
    

----------------------------------------
    change:
    
----------------------------------------

"""

__author__ = 'my'

import requests
import time
from lxml import etree

from proxypool.Util.WebRequest import WebRequest


def robustCrawl(func):
    def decorate(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            # logger.errro('')
            pass


def verifyProxyFormat(proxy):
    """
    check the style of proxy.
    :param proxy:
    :return:
    """
    import re
    verify_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def getHtmlTree(url, **kwargs):
    """
    get html tree
    :param url:
    :param kwargs:
    :return:
    """
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()
    time.sleep(2)
    html = wr.get(url=url, header=header).content
    return etree.HTML(html)


def tcpConnect(proxy):
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


def validUsefulProxy(proxy):
    """
    检查代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf-8')
    proxies = {'http': 'http://{proxy}'.format(proxy=proxy)}
    try:
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200:
            return True
    except Exception as e:
        return False
