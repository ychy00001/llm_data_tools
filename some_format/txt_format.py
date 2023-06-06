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

if __name__ == '__main__':
    for f_name, name in iter_dir(BASE_DIR):
        if f_name.endswith(".txt"):
            # 获取输出文件及文件夹
            format_file = f_name.replace(BASE_DIR, BASE_DIR + "_format")
            format_dir = format_file.replace(name, "")
            if os.path.exists(format_file):
                print(f"文件已格式化完成：{f_name}。跳过！")
                continue
            else:
                print(f"找到文件{f_name}")
            # 读取数据
            fcc_data = []
            fcc_data_item = {"history": "", "question": "", "context": "", "output": ""}
            count_total = 0
            count_format = 0
            with open(f_name, 'r', encoding='utf-8') as fcc_file:
                question = ""
                answer = ""
                line = fcc_file.readline()  # 调用文件的 readline()方法
                print(f"行: {line}")
                while line:
                    count_total += 1
                    # 解析问题和答案
                    line = line.strip()
                    # 移除task行, 移除空行
                    if line.startswith("task") or is_blank(line):
                        print(f"跳过: {line}")
                        line = fcc_file.readline()
                        continue
                    count_format += 1
                    if line.startswith("答"):
                        line = re.sub(r'^答[：:]\s*', "", line)
                        fcc_data_item["output"] = line.strip()
                        # 存储问题和答案
                        fcc_data.append(fcc_data_item)
                        fcc_data_item = {"history": "", "question": "", "context": "", "output": ""}
                    else:
                        line = re.sub(r'^[0-9].\s*', "", line)
                        fcc_data_item["question"] = line.strip()

                    line = fcc_file.readline()
                    print(f"总行数:{count_total}, 格式化行数:{count_format}")
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
                    if is_blank(question) or is_blank(output):
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
            print(f"处理完成：{f_name}, 行：{total_lie}")
            os.rename(format_file, format_file + "_" + str(total_lie))
