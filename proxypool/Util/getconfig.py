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

import os
from proxypool.Util.utilClass import ConfigParse



class GetConfig(object):
    """
    get config from config.ini
    """
    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'config.ini')
        self.config_file = ConfigParse()
        self.config_file.read(self.config_path)

    @property
    def db_type(self):
        return self.config_file.get('DB', 'type')

    @property
    def db_name(self):
        return self.config_file.get('DB', 'name')

    @property
    def db_host(self):
        return self.config_file.get('DB', 'host')

    @property
    def db_port(self):
        return self.config_file.get('DB', 'port')

    @property
    def db_password(self):
        return self.config_file.get('DB', 'password')

    @property
    def proxy_spider_not_use(self):
        return self.config_file.options('ProxySpider_not_use')

    @property
    def host_ip(self):
        return self.config_file.get('API', 'ip')

    @property
    def host_port(self):
        return self.config_file.get('API', 'port')

    @property
    def processes(self):
        return self.config_file.get('API', 'processes')

config = GetConfig()

if __name__ == '__main__':
    gg = GetConfig()
    for _ in dir(gg):
        if not _.startswith('__'):
            print(_)

