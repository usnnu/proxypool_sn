#coding:utf-8

"""
----------------------------------------
description:测试suite

author: sss

date:
----------------------------------------
change:
    
----------------------------------------

"""
__author__ = 'sss'

import unittest
#from test.test_webapi import TestCaseWebApi


def run_suite():
    suite = unittest.TestSuite()
    # 添加单个测试用例
    suite.addTest(TestCaseWebApi('test_webapi_mainpage'))
    # 添加多个测试用例
    # suite.addTests([TestCase_WebApi('test_webapi_get')])

    # 声明
    runner = unittest.TextTestRunner()
    runner.run(suite)

def run_testloader():
    print('use TestLoader')
    suite = unittest.defaultTestLoader.discover('.', pattern='test_unittest_*.py', top_level_dir=None)
    print(suite)
    runner = unittest.TextTestRunner()
    runner.run(suite)



if __name__ == '__main__':
    # run_suite()
    run_testloader()
    pass







