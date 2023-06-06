# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
import os
import re

BASE_DIR = "./data/05_11"


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
    return data_str


def process_content(text):
    # 移除图片链接 ![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)
    # 移除广告连接  [填写信息](http://cn.mikecrm.com/aIDshQc)
    # 移除特殊广告链接1 [芥末堆网](//www.jiemodui.com)
    # 移除特殊广告链接2 [芥末堆内容合作](/Cooperation)
    text = re.sub(r'!?\[.*?\]\([a-zA-z://]*?[^\s]*?\)', "", text)

    # 截取4000长度
    if len(text) > 4000:
        text = text[:4000]
    return text


TEMPLATE_NO_INPUT = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Response:"
TEMPLATE_WITH_INPUT = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.History:{}\n\nUser:{}\nnAssistant"
TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:{}\nHistory:{}\n\nUser:{}\n\nAssistant:"


def unique_list(list_obj, primary_key):
    list_obj_dict = {i.get(primary_key): i for i in list_obj}
    list_obj = list(list_obj_dict.values())
    return list_obj


def test1():
    # 合并两个文件 去重
    fcc_data = []
    with open("./data/05_11_format/qa_cw_excel.json_1587", 'r', encoding='utf-8') as a_file, \
            open("./data/05_11_format/cw_self.txt_6329", 'r', encoding='utf-8') as b_file:
        line_a = a_file.readline()
        while line_a:
            fcc_data.append(json.loads(line_a))
            line_a = a_file.readline()
        line_b = b_file.readline()
        while line_b:
            fcc_data.append(json.loads(line_b))
            line_b = b_file.readline()
        fcc_data = unique_list(fcc_data, 'prompt')

    format_dir = "./data/05_11_format"
    format_file = "./data/05_11_format/cw_self_cw_excel_total.json"
    mkdir(format_dir)
    with open(format_file, "a", encoding='utf-8') as f:
        # 遍历JSON数据
        total_lie = 0
        for data_item in fcc_data:
            f.write(json.dumps(data_item))
            f.write("\n")
            total_lie += 1
    print(f"处理完成")
    os.rename(format_file, format_file + "_" + str(total_lie))


def test2():
    f_b = open("./data/05_11_format/self_chat_20230426.json_93")
    f_b_lines = f_b.read()
    f_b.close()

    # 一个文件移除另一个文件中存在的数据 a文件中移除b文件可能存在的数据
    fcc_data = []
    with open("./data/05_11_format/cw_self_cw_excel_total.json_6560", 'r', encoding='utf-8') as a_file:
        line_a = a_file.readline()
        while line_a:
            line_a_doc = json.loads(line_a)
            if line_a_doc["prompt"] in f_b_lines:
                line_a = a_file.readline()
                continue
            fcc_data.append(line_a_doc)
            line_a = a_file.readline()

    format_dir = "./data/05_11_format"
    format_file = "./data/05_11_format/cw_self_cw_excel_total_deduplicate.json"
    mkdir(format_dir)
    with open(format_file, "a", encoding='utf-8') as f:
        # 遍历JSON数据
        total_lie = 0
        for data_item in fcc_data:
            f.write(json.dumps(data_item, ensure_ascii=False))
            f.write("\n")
            total_lie += 1
    print(f"处理完成")
    os.rename(format_file, format_file + "_" + str(total_lie))


if __name__ == '__main__':
    # 合并两个文件 去重
    # test1()
    test2()
