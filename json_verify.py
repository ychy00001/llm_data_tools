# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
from json import JSONDecodeError
import os
import re

BASE_DIR = "./data/last_format/code"


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


if __name__ == '__main__':
    count = 0
    total_list = []
    for f_name, name in iter_dir(BASE_DIR):
        if f_name:
            with open(f_name, 'r', encoding='utf-8') as t_f:
                line_a = t_f.readline()
                while line_a:
                    try:
                        count += 1
                        std_obj = json.loads(line_a)
                        if count == 156:
                            print(std_obj)
                        print(f"line: {count} prompt: {len(std_obj['prompt'])}  output: {len(std_obj['output'])}")
                        total_list.append(json.loads(line_a, strict=False))
                    except JSONDecodeError:
                        print(f_name)
                    line_a = t_f.readline()
    print(f"success!  total line: {count}")
