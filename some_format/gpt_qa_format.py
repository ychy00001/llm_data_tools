# -*- coding: utf-8 -*-
import json
import operator as op
import os
import pandas as pd

BASE_FILE = "./data/alpine_corpus.csv"
FORMAT_FILE = "./data/alpine_corpus_format.json"


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


TEMPLATE_NO_INPUT = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Response:"
TEMPLATE_WITH_INPUT = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Input:\n{}\n\n### Response:"
TEMPLATE_CHAT = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.\n\n{}"

if __name__ == '__main__':
    data_pd = pd.read_csv(BASE_FILE)
    total_lie = 0
    with open(FORMAT_FILE, "a", encoding='utf-8') as f:
        # 遍历csv数据
        for index, row in data_pd.iterrows():
            if int(index) % 100 == 0:
                print(f"已处理：{index}行")
            if isinstance(row.q,str) is not True or isinstance(row.a,str) is not True:
                continue
            prompt = row.q.strip()
            output = row.a.strip()

            # 处理异常数据
            if prompt.isspace() or output.isspace() or len(prompt) == 0 or len(output) == 0:
                continue

            # 结束符为？ ?的移除
            last_char = output[-1]
            if last_char == "?" or last_char == "？":
                continue

            # prompt内容过滤
            if op.contains(prompt, "照片") or \
                    op.contains(prompt, "图片"):
                continue
            # 响应内容过滤
            if op.contains(output, "抱歉") or \
                    op.contains(output, "语言模型") or \
                    op.contains(output, "无法确定"):
                continue
            template = TEMPLATE_NO_INPUT
            # 格式化写入文件
            result = dict(
                prompt=template.format(prompt),
                output=output
            )
            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
            total_lie += 1

    os.rename(FORMAT_FILE, FORMAT_FILE + "_" + str(total_lie))
