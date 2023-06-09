# -*- coding: utf-8 -*-
import hashlib
import re


def sh1_encrypt(data):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(data.encode("utf8"))
    encrypts = sha.hexdigest()
    return encrypts


def check_str_count(str_source, str_check):
    '''
    检查字符串中某个字符存在的个数
    str_source：源字符串；
    str_check：要检查字符
    '''
    splits = str_source.split(str_check)  # 返回拆分数组
    return len(splits) - 1  # 返回拆分次数-1


def cut_sent(para):
    '''
    句子切分
    示例：cut_sent("`emmm....`我说，`看看这个分句行不行吧。`")
    '''
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")
