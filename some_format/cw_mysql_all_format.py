# -*- coding: utf-8 -*-
import json
import common.filter as filter
import os

BASE_DIR = "./data/last"

CATEGORY_TOTAL = {
    "OpenQA": 200,
    "MRC": 200,
    "AncientPoem": 200,
    "NLI": 200,
    "NER": 200,
    "Couplet": 500,
    "JinYongGeneration": 500,
    "KeywordRecognition": 500,
    "LyricGeneration": 500,
    "Composition": 500,
    "ClassicalChinese": 500,
    "TextCorrection": 1000,
    "SentimentAnalyze": 200,
    "TextMatching": 200,
    "MusicComment": 200,
    "Dictionary": 200,
    "ProseGeneration": 200,
    "StoryGeneration": 1000,
    "Program": 974,

    "诗词": 1500,
    "诗词赏析": 1500,
    "人物介绍": 1500,

    "逻辑思维训练": 310,
}

CATEGORY_COUNT = {
    "OpenQA": 0,
    "MRC": 0,
    "AncientPoem": 0,
    "NLI": 0,
    "NER": 0,
    "Couplet": 0,
    "JinYongGeneration": 0,
    "KeywordRecognition": 0,
    "LyricGeneration": 0,
    "Composition": 0,
    "ClassicalChinese": 0,
    "TextCorrection": 0,
    "SentimentAnalyze": 0,
    "TextMatching": 0,
    "MusicComment": 0,
    "Dictionary": 0,
    "ProseGeneration": 0,
    "StoryGeneration": 0,
    "Program": 0,
    "诗词": 0,
    "诗词赏析": 0,
    "人物介绍": 0,

    "逻辑思维训练": 0,
}


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
        if f_name.endswith(".sql-all.json"):
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
                for data_item in fcc_data["RECORDS"]:
                    history = data_item["history"]
                    question = data_item["question"].strip()
                    context = data_item["context"].strip()
                    output = data_item["answer"].strip()
                    meta = data_item["meta"].strip()
                    category = data_item["category"].strip()

                    hit_flag = False
                    # 逻辑思维训练 cot数据   generic fun数据
                    if category == "逻辑思维训练" or category == "generic":
                        hit_flag = True

                    # 移除较少的笑话数据
                    if category == "generic" and len(output) < 20:
                        hit_flag = False

                    # meta是GPT 4的放行 (t_zbench_data数据)  t_3rd_company_show数据
                    if meta == "GPT - 4" or meta == "t_3rd_company_show":
                        hit_flag = True

                    if not hit_flag:
                        continue

                    if history == "[]":
                        history = ""
                    if filter.is_not_blank(history):
                        history = json.loads(history)

                    # 处理异常数据
                    if filter.is_continue(question, output):
                        continue

                    # 结束符为？ ?的移除
                    # last_char = output[-1]
                    # if last_char == "?" or last_char == "？":
                    #     continue

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
            new_file = format_file + "_" + str(total_lie)
            print(f"处理完成：{new_file}")
            os.rename(format_file, new_file)
