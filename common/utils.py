# -*- coding: utf-8 -*-
import hashlib
import re
import string
import os
import zhconv

PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

def Ban2Quan(content):
    """
    半角转全角
    """
    content = content.decode('utf-8')
    last_char = ''
    next_chat = ''
    for index in range(len(content)):
        current_char = content[index]
        if (index + 1) < len(content):
            next_chat = content[index + 1]
        if current_char == '.' and last_char.isdigit() and next_chat.isdigit():
            continue
        if current_char in string.punctuation:
            content = content.replace(current_char, B2Q(current_char))
    return content


def Quan2Ban(content):
    """
    半角转全角
    """
    content = content.decode('utf-8')
    for c in content:
        if c in string.punctuation:
            content = content.replace(c, Q2B(c))
    return content


def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


def B2Q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def traditional2simplified(key_str):
    """ 将key_str中的繁体字转为简体字

    :param key_str: str, 需要做简繁体转换的字符串
    :return: str, key_str对应的简体字
    """
    return zhconv.convert(key_str, 'zh-hans')


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
    para = re.sub('([。！？.\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


def str_char_info(str):
    '''
    找出字符串中的中英文、空格、数字、标点符号个数
    return 总长度[0] 中文[1]  英文[2] 空格[3] 数字[4] 标点格式[5]
    '''

    count_en = count_dg = count_sp = count_zh = count_pu = 0
    s_len = len(str)
    for c in str:
        if c in string.ascii_letters:
            count_en += 1
        elif c.isdigit():
            count_dg += 1
        elif c.isspace():
            count_sp += 1
        elif c.isalpha():
            count_zh += 1
        else:
            count_pu += 1
    total_chars = count_zh + count_en + count_sp + count_dg + count_pu
    return s_len, count_zh, count_en, count_sp, count_dg, count_pu


def get_all_files(file_dir, suffix1="_clean", suffix2=""):
    '''
    获取所有文件，同时返回文件对应的格式化以及清楚的脏数据
    return: [(file_path, file_format_path, file_dirty_path), ()....]
    '''
    files = []
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            format_path = file_path.replace(file_dir, file_dir + suffix1)
            make_file_dir(format_path)

            dirty_path = None
            if suffix2 != "":
                dirty_path = file_path.replace(file_dir, file_dir + suffix2)
                make_file_dir(dirty_path)
            files.append((file_path, format_path, dirty_path))
    return files


def make_file_dir(file_path):
    '''
    根据文件创建其路径的目录
    '''
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


def get_en_world_count(content):
    '''
    获取英文单词数量
    '''
    world_list = content.split(" ")
    return len(world_list)


def is_zh_en(content):
    '''
    判断句子是中文还是英文句子,截取前200个字符
    return: zh 中文
            en 英文
            unknow 未知
    '''
    zh_list = []
    en_list = []
    for char in content[:300]:
        if '\u4e00' <= char <= '\u9fff':
            zh_list.append(char)
        elif ('\u0041' <= char <= '\u005a') or ('\u0061' <= char <= '\u007a'):
            en_list.append(char)
    zh_len = len(zh_list)
    en_len = get_en_world_count(content)
    if zh_len > 0 and zh_len > en_len:
        return 'zh'
    elif en_len > 0 and en_len > zh_len:
        return 'en'
    return 'unknown'


def word_count(content):
    '''
    获取文本单词、字个数
    '''
    content_type = is_zh_en(content)
    wold_len = len(content)
    if content_type == 'en':
        wold_len = get_en_world_count(content)
    return wold_len


def truncate_content(content, length: int):
    '''
    根据中英文不同，截取内容长度
    '''
    content_type = is_zh_en(content)
    if content_type == 'en':
        en_list = content.split(" ")
        return " ".join(en_list[:length])
    return content[:length]
