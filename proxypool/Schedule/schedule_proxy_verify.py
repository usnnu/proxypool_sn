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
import sys
import time

from threading import Thread
from queue import Queue

sys.path.append('../')

from proxypool.Manager.crawler_manage import CrawlerManager
from proxypool.Util.loggerhandler import LogHandler
from proxypool.Util.util_function import  validUsefulProxy

FALT_COUNT = 0 # 如果代理的分值低于它，删除

class ProxyValidSchedule(CrawlerManager, object):
    """
    从可用代理池中读取代理并验证可用性。如果可用则
    每次取分值最低的一半元素
    类中使用queue
    """
    def __init__(self):
        CrawlerManager.__init__(self)
        self.queue = Queue()
        self.log = LogHandler('proxy_verify')

    def __valid_proxy(self, thread_num=20):
        """
        验证代理可用性
        :param thread_num: 线程数
        :return:
        """
        thread_list = list()
        for i in range(thread_num):
            thread_list.append(ProxyCheck(self.queue))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def main(self):
        self.putqueue()
        while True:
            if not self.queue.empty():
                self.log.info('start valid useful_proxy.')
                self.__valid_proxy()
                self.log.info('可用代理队列验证完成，等待10分钟！')
                time.sleep(60*10)
            else:
                self.log.info('可用代理队列为空！等待10分钟！')
                time.sleep(60 * 5)
                self.putqueue()

    # 将可用代理表中的后面一半放入队列
    def putqueue(self):
        num_t = self.db.zcard(self.useful_proxy_queue)//2
        if num_t < 1000:
            num_t = (num_t+1)*2
        for i in self.db.zrange(self.useful_proxy_queue, 0, num_t):
            self.queue.put(i)




# 执行测试的类
class ProxyCheck(CrawlerManager, Thread):
    def __init__(self, queue):
        CrawlerManager.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_verify')
        self.queue = queue

    def run(self):
        while self.queue.qsize():
            proxy = self.queue.get()
            if validUsefulProxy(proxy):
                self.db.zincrby(self.useful_proxy_queue, proxy, 1)
                self.log.info('ProxyCheck: {} validation pass.'.format(proxy))
            else:
                self.log.info('ProxyCheck: {} validation fail.'.format(proxy))
                if self.db.zscore(self.useful_proxy_queue, proxy) < FALT_COUNT:
                    self.log.info('ProxyCheck: {} fail too many times, delete!'.format(proxy))
                    self.db.zrem(self.useful_proxy_queue, proxy)
            self.queue.task_done()


# 模块运行函数
def run():
    p = ProxyValidSchedule()
    p.main()


if __name__ == '__main__':
    run()
