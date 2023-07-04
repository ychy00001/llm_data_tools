# -*- coding: utf-8 -*-
import time
from common.log import logger

def get_time(func):
    def inner(*arg, **kwarg):
        s_time = time.time() * 1000
        res = func(*arg, **kwarg)
        e_time = time.time() * 1000
        logger.debug('方法：{} 耗时：{}毫秒'.format(func.__qualname__ , e_time - s_time))
        return res

    return inner
