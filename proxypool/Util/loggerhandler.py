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
import logging

from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')


class LogHandler(logging.Logger):
    def __init__(self, name='mainlogger', level=DEBUG, file_rotation=True, stream=True, **kwargs):
        self.name = name
        logging.Logger.__init__(self, self.name, level=level)

        #self.logger.propagate = False
        self.setLevel(level)
        if stream:
            self._set_stream_handler()
        if file_rotation:
            self._set_file__rotating_handler()
        if 'time_rotation_file' in kwargs and kwargs['time_rotation_file']:
            self._set_time_rotating_handler()

    def _set_file__rotating_handler(self, level=None):
        file_name = os.path.join(LOG_PATH, '{}.log'.format(self.name))
        file_handler = RotatingFileHandler(file_name,
                                           maxBytes = 50*1024*1024,
                                           backupCount=5,
                                           encoding='utf-8')
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s [pid:%(process)d]%(message)s')
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def _set_stream_handler(self, level=None):
        stream_handler = logging.StreamHandler()
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)
        pass

    def _set_time_rotating_handler(self, level=None):
        file_name = os.path.join(LOG_PATH, '{}.log'.format(self.name))
        time_handler = logging.handlers.TimedRotatingFileHandler(file_name,
                                                                 when='h',
                                                                 interval=1,
                                                                 backupCount=24)
        if not level:
            time_handler.setLevel(self.level)
        else:
            time_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
        time_handler.setFormatter(formatter)
        time_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
        self.addHandler(time_handler)




if __name__ == '__main__':
    log = LogHandler('test')
    log.info('this is a test msg')
    # log1 = LogHandler()
    # log1.info('this is a test msg')
