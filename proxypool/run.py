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
import sys
from multiprocessing import Process

sys.path.append('.')
sys.path.append('..')

from proxypool.Api.proxy_api import run as PROXY_API_RUN
from proxypool.Schedule.schedule_proxy_verify import run as PROXY_VALID_RUN
from proxypool.Schedule.schedule_proxy_add import run as PROXY_ADD_RUN


def run():
    p_list = []

    p1 = Process(target=PROXY_VALID_RUN, name='ProxyValidRun')
    p_list.append(p1)
    p2 = Process(target=PROXY_ADD_RUN, name='ProxyAddRun')
    p_list.append(p2)
    p3 = Process(target=PROXY_API_RUN, name='ProxyApiRun')
    p_list.append(p3)

    for _ in p_list:
        _.daemon = True
        _.start()

    time.sleep(5)
    for _ in p_list:
        _.join()

    for _ in p_list:
        print(_)



if __name__ == '__main__':
    run()
