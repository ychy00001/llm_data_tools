# -*- coding: utf-8 -*-
import logging
import sys
import os


def _get_logger():
    log = logging.getLogger('log')
    if os.getenv('LOG_LEVEL') == "DEBUG":
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.setFormatter(logging.Formatter('[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s',
                                                  datefmt='%Y-%m-%d %H:%M:%S'))
    log.addHandler(console_handle)
    return log


# 日志句柄
logger = _get_logger()
