# -*- coding: utf-8 -*-
import hashlib


def sh1_encrypt(data):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(data.encode("utf8"))
    encrypts = sha.hexdigest()
    return encrypts
