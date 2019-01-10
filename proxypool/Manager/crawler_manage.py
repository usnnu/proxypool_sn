#coding:utf-8

"""
----------------------------------------
    description:
    author:sss
    date:
----------------------------------------
    change:
    
----------------------------------------

"""

__author__ = 'my'


# from DB.redis_client import RedisClient

from proxypool.Util.getconfig import config
from proxypool.Util.loggerhandler import LogHandler
from redis import Redis


class CrawlerManager(object):
    """
    proxy manager
    是代理池的信息、管理类,对API提供接口。
    DB分两个table/key/collection:
    1.raw_proxy:原始代理数据，刚从网站中抓取后存放于此；目前使用redis 的set；
    2.useful_proxy：可用代理数据，验证后存放于此；目前使用redis 的sort set；

    关于代理的轮换策略，通过分值实现：
    1.初始化，入库时会给出一个初始分值，每取用一次会减1；
    2.恢复：在定时验证可用性时如果验证成功会恢复到初始分值。
    3.删除：定时验证可用性时如果验证失败则删除。
    （目前如此，也可以使用在验证失败时减2分，然后在0分时删除。）

    class ProxyRefreshSchedule:定时从网站抓取更新
    class ProxyValidSchedule：定时验证可用库中代理可用性
    """

    def __init__(self):
        self.db = Redis(host=config.db_host,
                        port=int(config.db_port),
                        db=0,
                        password=config.db_password,
                        decode_responses=True)
        self.raw_proxy_queue = 'raw_proxy'
        self.useful_proxy_queue = 'useful_proxy'
        #self.log = LogHandler()

    def get_proxy(self, num=0):
        """
        return a useful proxy
        从可用库中返回一个代理，关键是选择方法，不能老用前面的，也不能每次加载所有的数据再随机
        目前默认是使用zrevrange(0,0)
        :return:
        """
        proxy = self.db.zrevrange(self.useful_proxy_queue, 0, num)
        for _ in proxy:
            self.db.zincrby(self.useful_proxy_queue, _, -1)
        if proxy:
            return proxy
        else:
            return None

    def delete(self, proxy):
        if self.db.zrem(self.useful_proxy_queue, proxy):
            return '删除成功！'
        else:
            return '删除异常（可能该代理不存在）。'

    def get_status(self):
        """
        获取当前原始表和可用表中的代理数，因为数值随时可能变化，可能会有一定偏差。
        :return:
        """
        total_raw_proxy = self.db.zcard(self.raw_proxy_queue)
        total_useful_proxy = self.db.zcard(self.useful_proxy_queue)
        return (total_raw_proxy, total_useful_proxy)


if __name__ == '__main__':
    pp = CrawlerManager()
