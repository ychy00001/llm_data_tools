# -*- coding: utf-8 -*-
import json
import common.filter as filter
import random
import sys
from service.chat_prompt_service import ChatPromptService
import os
import re

BASE_DIR = "./data/last"


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


TEMPLATE_NO_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nUser:{}\n\nAssistant:"
TEMPLATE_WITH_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nHistory:{}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nHistory:{}\n\nUser:{}\n\nAssistant:"

if __name__ == '__main__':
    for f_name, name in iter_dir(BASE_DIR):
        if f_name.endswith(".json.1"):
            # 获取输出文件及文件夹
            format_file = f_name.replace(BASE_DIR, BASE_DIR + "_format")
            format_dir = format_file.replace(name, "")
            if os.path.exists(format_file):
                print(f"文件已格式化完成：{f_name}。跳过！")
                continue
            # 读取数据
            with open(f_name, 'r', encoding='utf-8') as fcc_file:
                fcc_data = json.load(fcc_file)

            mkdir(format_dir)
            with open(format_file, "a", encoding='utf-8') as f:
                print(f"正在处理：{f_name}")
                # 遍历JSON数据
                total_lie = 0
                for data_item in fcc_data:
                    question = data_item["instruction"].strip()
                    context = data_item["input"].strip()
                    output = data_item["output"].strip()
                    question += "\n" + context

                    # 处理异常数据
                    if filter.is_continue(question, output):
                        continue

                    # 结束符为？ ?的移除
                    last_char = output[-1]
                    if last_char == "?" or last_char == "？":
                        continue

                    # 根据数据选择合适的模版
                    template = TEMPLATE_NO_INPUT
                    # 格式化写入文件
                    result = dict(
                        prompt=template.format(question),
                        output=output
                    )
                    result = filter.result_filter(result)
                    data = json.dumps(result, ensure_ascii=False)
                    f.write(data)
                    f.write("\n")
                    total_lie += 1
            print(f"处理完成：{f_name}")
            os.rename(format_file, format_file + "_" + str(total_lie))
