#coding:utf-8

"""
----------------------------------------
description:

author: sss

date:
----------------------------------------
change:
    
----------------------------------------

"""
__author__ = 'sss'


import unittest
import requests
from proxypool.Api.proxy_api import run
from threading import Thread


class TestCaseWebApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('starting webapi...')
        thread = Thread(target=run)
        thread.daemon = True
        thread.start()
        print('webapi is running...')

    #  主页面测试
    def test_webapi_mainpage(self):
        url = 'http://localhost:8080/'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, 'main page test failed.')

    #  get页面测试
    def test_webapi_get(self):
        url = 'http://localhost:8080/get'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, 'get page test failed.')

    #  delete页面测试
    def test_webapi_delete(self):
        url = 'http://localhost:8080/delete?proxy=5.6.4.3:453'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, 'delete page test failed.')

    #  status页面测试
    def test_webapi_status(self):
        url = 'http://localhost:8080/status'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, 'satus page test failed.')


def start_test():
    print('test start')
    unittest.main()
    print('test end.')


if __name__ == '__main__':
    start_test()
