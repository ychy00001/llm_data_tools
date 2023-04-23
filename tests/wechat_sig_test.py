# -*- coding: utf-8 -*-
from common.utils import sh1_encrypt

if __name__ == '__main__':
    signature = "8fa39f80ceaef83d4c3b8f3f7b7fbfd41c739293"
    nonce = "xoaosajfj"
    timestamp = "1929383"
    token = "weixin"

    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = ''.join(tmp_arr)
    tmp_signature = sh1_encrypt(tmp_str)

    if signature == tmp_signature:
        print("True,{}", tmp_signature)
    else:
        print("False,{}", tmp_signature)
