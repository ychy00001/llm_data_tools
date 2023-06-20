import sys
import os
import json
import time
import shutil
from json.decoder import JSONDecodeError
import jieba_fast as jieba
import random

sys.path.append("../../")
from common.logger import Logger
import pandas as pd
from enum import Enum


class PROCESS_TYPE(Enum):
    BAD = "bad"
    GOOD = "good"


format_dir = "./data/"
total_file = "somedata.total"
shuffle_file = "somedata.shuffle"
# 跳过文件
skip_dict = {
}

os.makedirs("./log", exist_ok=True)
log = Logger('./log/content_dirty_clean.log', level='debug')


def process_log(current_percent, percent_step, file_name, current_line, line_count, repeat_count, error_count,
                blank_count, total_count, dirty, total_dirty):
    percent = current_line / line_count * 100
    if percent > current_percent:
        current_percent += percent_step
        log.logger.info(f"已完成{int(percent)}%")
    if percent == 100:
        log.logger.info(
            f"处理完成：{file_name} , 总行数：{current_line}, 重复行数：{repeat_count}, JSON异常行数：{error_count}, 脏数据：{dirty}, 总处理行数：{total_count} 总脏数据：{total_dirty}")
    return current_percent


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def process(base_dir, local_format_dir, process_type: PROCESS_TYPE):
    '''
    process_type：处理数据类型
    '''
    # shutil.rmtree(local_format_dir)
    os.makedirs(local_format_dir, exist_ok=True)
    # 获取待处理文件或者文件夹
    deduplicate_file = [f"{base_dir}/{i}" for i in os.listdir(base_dir)]
    # -- 待去重文件列表 = []
    log.logger.info(f"\n总共{len(deduplicate_file)}个文件或文件夹")

    # 实际处理
    file_count = 0
    total_line = 0
    total_dirty = 0
    for file_item in deduplicate_file:
        base_file_name = os.path.basename(file_item)
        if os.path.isdir(file_item):
            # sub_format_dir = local_format_dir + "/" + base_file_name + "/"
            # subset = os.path.basename(base_dir)
            process(file_item, local_format_dir, process_type)
        else:
            # 跳过整个文件
            if base_file_name in skip_dict.keys() and skip_dict[base_file_name] == "all":
                log.logger.info(f"\n文件：{base_file_name}已完成，跳过！")
                continue

            file_count += 1
            log.logger.info(f"\n处理{base_dir}第{file_count}个文件: {file_item}")

            # 计算总行数
            line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])
            # line_count = len(process_data)

            i = 0
            repeat = 0
            error = 0
            dirty = 0
            blank = 0
            # 进度条记录
            percent_step = 20
            current_percent = 0
            # 读取数据
            with open(local_format_dir + "somedata.total", "a", encoding='utf-8') as f:
                for item_line in open(file_item, 'r', encoding='utf8'):
                    try:
                        line_json = json.loads(item_line, strict=False)
                    except JSONDecodeError as e:
                        error += 1
                        log.logger.error(f'JSON解析异常：{item_line}')
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line, dirty, total_dirty)
                        continue
                    i += 1
                    total_line += 1
                    # 跳过行数
                    if base_file_name in skip_dict.keys():
                        if skip_dict[base_file_name] > i:
                            current_percent = process_log(current_percent, percent_step, file_item, i, line_count,
                                                          repeat,
                                                          error, blank, total_line, dirty, total_dirty)
                            continue
                        elif skip_dict[base_file_name] == i:
                            log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")

                    text = line_json["text"]
                    meta = line_json["meta"]
                    title = meta["title"]

                    if not text.startswith(title):
                        text = title + "\n\n" + text

                    # jieba分词 使用全模式 词更符合逻辑
                    seg_list = jieba.cut(text, cut_all=True)

                    # 写入文件
                    result = f"__label__{process_type.value} {' '.join(seg_list)}"
                    f.write(result)
                    f.write("\n")
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error,
                                                  blank, total_line, dirty, total_dirty)


def main(exec_type):
    base_dir = f"./raw_data_{exec_type.value}/"
    log.logger.info("———— 开始 ————")
    process(base_dir, format_dir, exec_type)
    log.logger.info("———— 结束 ————")


def shuffle(in_file, out_file):
    import os
    import random
    out = open(out_file, 'w')
    lines = []
    with open(in_file, 'r') as infile:
        for line in infile:
            lines.append(line)
    random.shuffle(lines)
    for line in lines:
        out.write(line)
    out.close()


def split_train_test_valid(input_path, input_file, train_pro, test_pro):
    # read file
    df_flow = pd.read_table(input_path + input_file, header=None)

    # define the ratios 6:2:2
    train_len = int(len(df_flow) * train_pro)
    test_len = int(len(df_flow) * test_pro)

    # split the dataframe
    idx = list(df_flow.index)
    random.shuffle(idx)  # 将index列表打乱
    df_train = df_flow.loc[idx[:train_len]]
    df_test = df_flow.loc[idx[train_len:train_len + test_len]]
    df_valid = df_flow.loc[idx[train_len + test_len:]]  # 剩下的就是valid

    # output
    df_train.to_csv(input_path + 'train.txt', header=False, index=False, sep='\t')
    df_test.to_csv(input_path + 'test.txt', header=False, index=False, sep='\t')
    df_valid.to_csv(input_path + 'valid.txt', header=False, index=False, sep='\t')


if __name__ == '__main__':
    # main(PROCESS_TYPE.BAD)
    # main(PROCESS_TYPE.GOOD)
    # 打乱文件(切分时候就打乱了)
    # shuffle(format_dir + total_file, format_dir + shuffle_file)
    # 切分文件
    split_train_test_valid(format_dir, total_file, 0.6, 0.2)
