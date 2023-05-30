# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
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

def process_content(text):
    # 移除图片链接 ![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)
    # 移除广告连接  [填写信息](http://cn.mikecrm.com/aIDshQc)
    # 移除特殊广告链接1 [芥末堆网](//www.jiemodui.com)
    # 移除特殊广告链接2 [芥末堆内容合作](/Cooperation)
    text = re.sub(r'!?\[.*?\]\([a-zA-z://]*?[^\s]*?\)', "", text)
    # 移除.png .jpeg .jpg图片链接
    text = re.sub(r'[a-zA-z]+://[^\s]*.[png|jpg|jpeg]', "", text)
    return text

def data_filter(data_str: str):
    # 替换  cwRong
    data_str = data_str.replace("cwRong", "RongGPT")
    # 移除图片 广告
    data_str = process_content(data_str)
    # 替换<br/>为\n
    data_str = data_str.replace("<br/>", "\\n")
    # 替换<br>
    data_str = data_str.replace("<br>", " ")
    data_str = data_str.replace("<p>", "")
    data_str = data_str.replace("</p>", "")
    data_str = re.sub(r'<u>[^\s\s]*</u>?', "", data_str)
    data_str = data_str.replace("<u>", "")
    data_str = data_str.replace("</u>", "")
    data_str = data_str.replace("; ; ; ; ; ; ; ; ; ;", "")
    data_str = data_str.replace("; ; ; ; ; ; ", "")
    data_str = data_str.replace("; ; ; ; ", "")
    data_str = data_str.replace("( ; ; 　)", "( )")
    data_str = data_str.replace("（ ; ; ; ）", "( )")
    data_str = data_str.replace("\\\\_", "( )")
    data_str = data_str.replace("\\\\\\\\\\\\", "( )")
    data_str = data_str.replace("; ; ;", ";")
    # 替换&nbsp为空格
    data_str = data_str.replace("&nbsp", " ")
    data_str = data_str.replace("�", "")
    data_str = data_str.replace("�", "")
    return data_str


def truncate_str(text: str):
    # 截取4000长度
    if len(text) > 4000:
        text = text[:4000]
    return text





TEMPLATE_NO_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nUser:{}\n\nAssistant:"
TEMPLATE_WITH_INPUT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nHistory:{}\n\nUser:{}\n\nAssistant:"
TEMPLATE_CONTEXT_CHAT = "If you are a artificial intelligence assistant assistant whose name is CongRong. CongRong is a conversational language model that is developed by CloudWalk.It is designed to be helpful,honest and harmless.Please answer the user questions based on the user asks and descriptions.\n\n\nContext: {}\n\nHistory:{}\n\nUser:{}\n\nAssistant:"

''' 还需要移除的数据
; ; ; ; ; ; ; ; ; ; 655 substitutions on 229 lines
; ; ; ; ; ;  486 substitutions on 307 lines
<u> ; ; ; ;</u> 1284 substitutions on 636 lines
\\_ 661 substitutions on 32 lines
 ; ; ; ; 632 substitutions on 435 lines
 ( ; ; 　) 1
 （ ; ; ; ）---> ( )291 substitutions on 289 lines
\r\n 1601 substitutions on 1601 lines
\r\n 1852 substitutions on 1596 lines
\r\n 259 substitutions on 75 lines
\r 17782 substitutions on 1704 lines
; ; ;
'''
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
                data_item = json.load(fcc_file)

            mkdir(format_dir)
            with open(format_file, "a", encoding='utf-8') as f:
                print(f"正在处理：{f_name}")
                # 遍历JSON数据
                total_lie = 0
                history = ""
                context = ""
                m_type = data_item["type"]
                raw_content = data_item["question_info"]["raw_content"]
                question = raw_content["title"]
                output = data_item["answer_info"]["raw_content"]
                solution_info = data_item["solution_info"]

                # 构建问题
                if not isinstance(question, str):
                    raw_content = question["question_info"]["raw_content"]
                    question = raw_content["title"]

                if m_type == "选择题":
                    for opt_key in raw_content:
                        if opt_key.startswith("option_") and len(raw_content[opt_key]) > 0:
                            new_key = opt_key[-1]
                            question = question + "\n" + new_key.upper() + ":" + raw_content[opt_key]

                # 构建答案
                solution_str = ""
                for item in solution_info:
                    solution_str += item["solution_info"]
                output = solution_str + output

                if history == "[]":
                    history = ""
                if is_not_blank(history):
                    history = json.loads(history)

                # 处理异常数据
                if is_blank(question) or is_blank(output):
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
        new_file = format_file + "_" + str(total_lie)
        print(f"处理完成：{new_file}")
        os.rename(format_file, new_file)
