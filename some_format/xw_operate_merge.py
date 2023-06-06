# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
import os
import re
import common.filter as filter

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
    # 读取数据
    fcc_data = []
    fcc_data_item = {"history": "", "question": "", "context": "", "output": ""}
    count_total = 0
    count_format = 0
    with open("./data/xw_operate/1.q", 'r', encoding='utf-8') as q_file, \
            open("./data/xw_operate/1.a", 'r', encoding='utf-8') as a_file:
        q_line = q_file.readline()  # 调用文件的 readline()方法
        a_line = a_file.readline()  # 调用文件的 readline()方法
        while q_line:
            count_total += 1
            # 解析问题和答案
            q_line = q_line.strip()
            a_line = a_line.strip()
            a_line = a_line.replace("\\n", "\n")
            if filter.is_blank(a_line):
                q_line = q_file.readline()  # 调用文件的 readline()方法
                a_line = a_file.readline()  # 调用文件的 readline()方法
                continue
            fcc_data_item["question"] = q_line
            if a_line.endswith("\""):
                a_line = a_line[:-1]
            fcc_data_item["output"] = a_line
            count_format += 1
            fcc_data.append(fcc_data_item)
            fcc_data_item = {"history": "", "question": "", "context": "", "output": ""}

            q_line = q_file.readline()  # 调用文件的 readline()方法
            a_line = a_file.readline()  # 调用文件的 readline()方法
            print(f"总行数:{count_total}, 格式化行数:{count_format}")

    format_dir = "./data/xw_operate_format"
    format_file = "./data/xw_operate_format/artificial_data.json"
    mkdir(format_dir)
    with open(format_file, "a", encoding='utf-8') as f:
        # 遍历JSON数据
        total_lie = 0
        for data_item in fcc_data:
            history = data_item["history"]
            question = data_item["question"].strip()
            context = data_item["context"].strip()
            output = data_item["output"].strip()

            if history == "[]":
                history = ""
            if filter.is_not_blank(history):
                history = json.loads(history)

            if filter.is_continue(question, output):
                continue

            # 根据数据选择合适的模版
            if filter.is_not_blank(history) and filter.is_not_blank(context):
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
            elif filter.is_not_blank(history):
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
            elif filter.is_not_blank(context):
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
            result = filter.result_filter(result)
            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
            total_lie += 1
    print(f"处理完成：{format_file}")
    os.rename(format_file, format_file + "_" + str(total_lie))
