# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
import os
import re

BASE_DIR = "./data/tools"


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


def is_blank(*params):
    for it in params:
        if (isinstance(it, str) and it.isspace()) or len(it) == 0:
            return True
    return False


def is_not_blank(*params):
    return not is_blank(params)


def data_filter(data_str: str):
    # 替换  cwRong
    data_str = data_str.replace("cwRong", "RongGPT")
    return data_str


TEMPLATE_NO_INPUT = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Response:"
TEMPLATE_WITH_INPUT = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.History:{}\n\nUser:{}\nnAssistant"
TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:{}\nHistory:{}\n\nUser:{}\n\nAssistant:"

if __name__ == '__main__':
    for f_name, name in iter_dir(BASE_DIR):
        if f_name.endswith(".json"):
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
                    history = data_item["history"]
                    question = data_item["question"].strip()
                    context = data_item["context"].strip()
                    output = data_item["output"].strip()

                    # 处理异常数据
                    if is_blank(question, output):
                        continue

                    # 结束符为？ ?的移除
                    last_char = output[-1]
                    if last_char == "?" or last_char == "？":
                        continue

                    # 根据数据选择合适的模版
                    if is_not_blank(history) and is_not_blank(context):
                        history_str = ""
                        for his_it in history:
                            user = "User:" + his_it["User"].strip() + "\n\n"
                            assistant = "Assistant:" + his_it["Assistant"].strip() + "\n\n"
                            history_str = history_str + user + assistant
                        template = TEMPLATE_CONTEXT_CHAT
                        # 格式化写入文件
                        result = dict(
                            prompt=template.format(context, history_str, question),
                            output=output
                        )
                    elif is_not_blank(history):
                        history_str = ""
                        for his_it in history:
                            user = "User:" + his_it["User"].strip() + "\n\n"
                            assistant = "Assistant:" + his_it["Assistant"].strip() + "\n\n"
                            history_str = history_str + user + assistant
                        template = TEMPLATE_CHAT
                        # 格式化写入文件
                        result = dict(
                            prompt=template.format(history_str, question),
                            output=output
                        )
                    elif is_not_blank(context):
                        template = TEMPLATE_WITH_INPUT
                        # 格式化写入文件
                        result = dict(
                            prompt=template.format(context, question),
                            output=output
                        )
                    else:
                        template = TEMPLATE_NO_INPUT
                        # 格式化写入文件
                        result = dict(
                            prompt=template.format(question),
                            output=output
                        )
                    data = json.dumps(result, ensure_ascii=False)
                    data = data_filter(data)
                    f.write(data)
                    f.write("\n")
                    total_lie += 1
            print(f"处理完成：{f_name}")
            os.rename(format_file, format_file + "_" + str(total_lie))
