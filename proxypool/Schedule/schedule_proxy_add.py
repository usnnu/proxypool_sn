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


import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler

from proxypool.Util.util_function import validUsefulProxy
from proxypool.Manager.crawler_manage import CrawlerManager
from proxypool.Util.loggerhandler import LogHandler
from proxypool.Util.util_function import verifyProxyFormat
from proxypool.ProxyGetter.proxy_spider import ProxySpider
from proxypool.Util.getconfig import config


class ProxyRefreshSchedule(CrawlerManager):
    """
    定时运行爬虫类，从网站获取新的代理。
    """
    def __init__(self):
        CrawlerManager.__init__(self)
        self.log = LogHandler('proxy_add')

    def get_new_proxy(self):
        spider_list = [x for x in dir(ProxySpider) if x.startswith('free')]
        spider_list_not_use = config.proxy_spider_not_use
        self.log.info('开始获取新的代理：{}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        for _ in [x for x in spider_list if x not in spider_list_not_use]:
            try:
                self.log.info('{}:start get proxy.'.format(_))
                proxy_list = getattr(ProxySpider, _.strip())()
                valid_proxy_count = 0
                for proxy in proxy_list:
                    proxy = proxy.strip()
                    if proxy and verifyProxyFormat(proxy):
                        self.db.sadd(self.raw_proxy_queue, proxy)
                        valid_proxy_count += 1
                self.log.info('{}:获取可用代理数：{}。'.format(_, valid_proxy_count))
            except Exception as e:
                self.log.error('{}: failed.'.format(_))
                self.log.exception('error')
                continue
        self.log.info('新的代理获取完成于：{}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))

    def verify_proxy(self, proxy):
        """
        验证代理其可用性，
        可用放入useful，初始分值为10；
        不可用代理被丢弃。
        valid_proxy_count_t用于计数：验证通过的代理数。
        :return:
        """
        if validUsefulProxy(proxy):
            self.db.zadd(self.useful_proxy_queue, proxy, 10)
            self.db.incr('valid_proxy_count_t', 1)

    def verfiy_proxy_threads(self, thread_num_max=20):
        """
        检验新代理，多线程，
        """
        self.db.set('valid_proxy_count_t', 0)
        total_num = self.db.scard(self.raw_proxy_queue)
        if total_num == 0:
            return
        self.log.info('开始验证新代理：')
        while True:
            if threading.active_count() <= thread_num_max:
                proxy = self.db.spop(self.raw_proxy_queue)
                if proxy is None:
                    break
                if self.db.zscore(self.useful_proxy_queue, proxy) is None:
                    thread_t = threading.Thread(target=self.verify_proxy, args=(proxy,), name='verify_proxy')
                    thread_t.daemon = True
                    thread_t.start()

        for _ in threading.enumerate():
            if _.name == 'verify_proxy':
                _.join()
        count = self.db.get('valid_proxy_count_t')
        self.log.info('本次校验{}个代理，{}个有效。'.format(total_num, count))


def fetch_new_proxy_run():
    p = ProxyRefreshSchedule()
    p.get_new_proxy()


def verify_proxy_threads_run():
    p = ProxyRefreshSchedule()
    # 获取新代理
    p.verfiy_proxy_threads()


# 模块调用入口
def run():
    #LogHandler().info('Rfresh module init...')
    scheduler = BackgroundScheduler()
    # 不用太快, 网站更新速度比较慢, 太快会加大验证压力, 导致raw_proxy积压
    scheduler.add_job(fetch_new_proxy_run, 'interval', minutes=10, id="fetch_proxy")
    scheduler.add_job(verify_proxy_threads_run, "interval", minutes=2)  # 每2分钟检查一次
    scheduler.start()

    fetch_new_proxy_run()

    while True:
        time.sleep(3)


if __name__ == '__main__':
    run()
