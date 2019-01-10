# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Description :   used for check getFreeProxy.py检查爬虫模块情况，主要是现有多少个爬虫及每个爬虫能否运行
   Author :        sss
   date：          2018/12/10
-------------------------------------------------
   Change: 2019/01/10
-------------------------------------------------
"""
__author__ = 'sss'


import time
from proxypool.ProxyGetter.proxy_spider import ProxySpider
from proxypool.Util.util_function import verifyProxyFormat
from proxypool.Util.loggerhandler import LogHandler


log = LogHandler('crawl_func_check')


class CrawlFuncCheck(object):
    """
    1.列出spider情况
    2.检测每个网站爬虫能否正常运行
    """
    @staticmethod
    def info_all_spiders():
        crawls_list = [x for x in dir(ProxySpider) if x.startswith('free')]
        print('目前有{}个爬虫：'.format(len(crawls_list)), crawls_list)
        print('\n\n\n帮助文档：')

        for _ in crawls_list:
            doc = getattr(ProxySpider, _).__doc__
            print("######" + _ + '######\n' + doc.strip())

    @staticmethod
    def check_all_get_functions():
        """
        检查getFreeProxy所有代理获取函数运行情况
        Returns:
            None
        """
        import inspect
        member_list = inspect.getmembers(ProxySpider, predicate=inspect.isfunction)
        proxy_count_dict = dict()
        for func_name, func in member_list:
            log.info(u"开始运行 {}".format(func_name))
            try:
                proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
                proxy_count_dict[func_name] = len(proxy_list)
            except Exception as e:
                log.info(u"代理获取函数 {} 运行出错!".format(func_name))
                log.error(str(e))
        log.info(u"所有函数运行完毕 " + "***" * 5)
        for func_name, func in member_list:
            log.info(u"函数 {n}, 获取到代理数: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))

    @staticmethod
    def check_single_get_function(func):
        """
        检查指定的getFreeProxy某个function运行情况
        Args:
            func: getFreeProxy中某个可调用方法

        Returns:
            None
        """
        func_name = getattr(func, '__name__', "None")
        log.info("start running func: {}".format(func_name))
        count = 0
        start_time = time.time()
        for proxy in func():
            if verifyProxyFormat(proxy):
                log.info("{} fetch proxy: {}".format(func_name, proxy))
                count += 1
        log.info("{n} completed, fetch proxy number: {c}, time cost:{time}s"
                 .format(n=func_name, c=count, time=time.time()-start_time))
        

if __name__ == '__main__':
    p = CrawlFuncCheck()
    p.info_all_spiders()
    # p.check_all_get_proxy()
    # p.check_single_get_function(GetFreeProxy.freeProxySecond)
