# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
from json import JSONDecodeError
import os
import re

BASE_DIR = "./data/7ke_json"


def iter_dir(base):
    # 递归遍历所有目录
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname, f


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(f"---  mkdir new folder：{path}  ---")


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def is_not_blank(it):
    return not is_blank(it)


def data_filter(data_str: str):
    # 替换  cwRong
    data_str = data_str.replace("cwRong", "RongGPT")
    # 移除图片 广告
    data_str = process_content(data_str)
    # 替换<br/>为\n
    data_str = data_str.replace("<br/>", "\\n")
    # 替换&nbsp为空格
    data_str = data_str.replace("&nbsp", " ")
    return data_str


def process_content(text):
    # 移除图片链接 ![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)
    # 移除广告连接  [填写信息](http://cn.mikecrm.com/aIDshQc)
    # 移除特殊广告链接1 [芥末堆网](//www.jiemodui.com)
    # 移除特殊广告链接2 [芥末堆内容合作](/Cooperation)
    text = re.sub(r'!?\[.*?\]\([a-zA-z://]*?[^\s]*?\)', "", text)
    # 移除.png .jpeg .jpg图片链接
    text = re.sub(r'[a-zA-z]+://[^\s]*.[png|jpg|jpeg]', "", text)
    # 截取4000长度
    # if len(text) > 4000:
    #     text = text[:4000]
    return text


def merge():
    dir = BASE_DIR + "_format"
    total_name = dir + "/total-rm.json"
    count = 0
    total_list = []
    for f_name, name in iter_dir(dir):
        if f_name.endswith(".json_1"):
            with open(f_name, 'r', encoding='utf-8') as t_f:
                line_a = t_f.readline()
                if line_a and len(line_a) > 0:
                    try:
                        if "<br>" in line_a or "<td>" in line_a or "<table>" in line_a:
                            continue
                        total_list.append(json.loads(line_a))
                    except JSONDecodeError:
                        print(f_name)
    with open(total_name, "w", encoding='utf-8') as f:
        for result in total_list:
            if is_blank(result):
                continue
            count += 1
            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
    new_name = total_name + "_" + str(count)
    os.rename(total_name, new_name)
    print(f"merge success: file {new_name}")


TEMPLATE_NO_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nUser:{}\n\nAssistant:"
TEMPLATE_WITH_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nHistory:{}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nHistory:{}\n\nUser:{}\n\nAssistant:"

if __name__ == '__main__':
    # 合并文件
    merge()
