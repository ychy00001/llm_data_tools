# -*- coding: utf-8 -*-
import json
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


OLD_TEMPLATE_NO_INPUT = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Response:"
OLD_TEMPLATE_WITH_INPUT = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:"
OLD_TEMPLATE_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.History:{}\n\nUser:{}\nnAssistant"
OLD_TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:{}\nHistory:{}\n\nUser:{}\n\nAssistant:"

TEMPLATE_NO_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nUser:{}\n\nAssistant:"
TEMPLATE_WITH_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nHistory:{}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nHistory:{}\n\nUser:{}\n\nAssistant:"

if __name__ == '__main__':
    for f_name, name in iter_dir(BASE_DIR):
        if f_name.endswith(".json.old"):
            # 获取输出文件及文件夹
            format_file = f_name.replace(BASE_DIR, BASE_DIR + "_format")
            format_dir = format_file.replace(name, "")
            if os.path.exists(format_file):
                print(f"文件已格式化完成：{f_name}。跳过！")
                continue
            fcc_data = []
            # 读取数据
            with open(f_name, 'r', encoding='utf-8') as fcc_file:
                line = fcc_file.readline()
                while line:
                    if filter.is_not_blank(line):
                        fcc_data.append(json.loads(line))
                    line = fcc_file.readline()

            mkdir(format_dir)
            with open(format_file, "a", encoding='utf-8') as f:
                print(f"正在处理：{f_name}")
                # 遍历JSON数据
                total_lie = 0
                for data_item in fcc_data:
                    prompt = data_item["prompt"].strip()
                    output = data_item["output"].strip()

                    history = ""
                    question = ""
                    context = ""
                    match_history_content_list = re.findall(
                        r"If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:([\s\S]*)\nHistory:([\s\S]*)\n\nUser:([\s\S]+)\n\nAssistant:",
                        prompt)
                    flag = True
                    if flag and len(match_history_content_list) == 1 and len(match_history_content_list[0]) == 3:
                        context = match_history_content_list[0][0]
                        history = match_history_content_list[0][1]
                        question = match_history_content_list[0][2]
                        flag = False

                    match_history_list = re.findall(
                        r"If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.History:([\s\S]*)\n\nUser:([\s\S]+)\nnAssistant",
                        prompt)
                    if flag and len(match_history_list) == 1 and len(match_history_list[0]) == 2:
                        history = match_history_list[0][0]
                        question = match_history_list[0][1]
                        flag = False

                    match_input_list = re.findall(
                        r"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n([\s\S]*)\n\n### Input:\n([\s\S]+)\n\n### Response:",
                        prompt)
                    if flag and len(match_input_list) == 1 and len(match_input_list[0]) == 2:
                        context = match_input_list[0][0]
                        question = match_input_list[0][1]
                        flag = False

                    match_normal_list = re.findall(
                        r"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n([\s\S]+)\n\n### Response:",
                        prompt)
                    if flag and len(match_normal_list) == 1:
                        question = match_normal_list[0]
                        flag = False

                    if history == "[]":
                        history = ""

                    # 处理异常数据
                    if filter.is_continue(question, output):
                        continue
                    # 根据数据选择合适的模版
                    if filter.is_not_blank(history) and filter.is_not_blank(context):
                        template = TEMPLATE_CONTEXT_CHAT
                        # 格式化写入文件
                        result = dict(
                            prompt=template.format(context, history, question),
                            output=output
                        )
                    elif filter.is_not_blank(history):
                        template = TEMPLATE_CHAT
                        # 格式化写入文件
                        result = dict(
                            prompt=template.format(history, question),
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
            new_name = format_file + "_" + str(total_lie)
            print(f"处理完成：{new_name}")
            os.rename(format_file, new_name)
