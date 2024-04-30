import sys
import os
import json
import time
import hashlib

sys.path.append("..")
from common.logger import Logger
from common.filter import preprocess_title_content, is_not_blank
from multiprocessing import Pool
from common.utils import get_all_files

os.makedirs("./log", exist_ok=True)
log = Logger('./log/wiki_hf.log', level='debug')


def process_log(current_percent, percent_step, file_name, current_line, line_count, repeat_count, error_count,
                blank_count, total_count):
    percent = current_line / line_count * 100
    if percent > current_percent:
        current_percent += percent_step
        log.logger.info(f"已完成{int(percent)}%")
    if percent == 100:
        log.logger.info(
            f"处理完成：{file_name} , 总行数：{current_line}, 重复行数：{repeat_count}, JSON异常行数：{error_count}, 空行数：{blank_count}, 总处理行数：{total_count}")
    return current_percent


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def run(job):
    file_item = job[0]
    file_item_format = job[1]
    base_file_name = os.path.basename(file_item)
    # 实际处理
    total_line = 0
    # 跳过整个文件
    if base_file_name in skip_dict.keys() and skip_dict[base_file_name] == "all":
        log.logger.info(f"\n文件：{base_file_name}已完成，跳过！")
        return

    # 计算总行数
    line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])

    i = 0
    repeat = 0
    error = 0
    blank = 0
    # 进度条记录
    percent_step = 20
    current_percent = 0
    with open(file_item_format, "a", encoding='utf-8') as f:
        for item_line in open(file_item, 'r', encoding='utf8'):
            line_json = json.loads(item_line, strict=False)
            i += 1
            # 跳过行数
            if base_file_name in skip_dict.keys():
                if skip_dict[base_file_name] > i:
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count,
                                                  repeat,
                                                  error, blank, total_line)
                    continue
                elif skip_dict[base_file_name] == i:
                    log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")
            total_line += 1

            content = line_json["content"].strip()
            title = line_json["title"].strip()

            # 写入文件
            result = {
                "text": content,
                "meta": {
                    "source": source,
                    "subset": subset,
                    "type": "wiki",
                    "title": title,
                    "lang": "zh",
                    "fileIdx": base_file_name,
                    "idx": i,  # 本文件内的数据序号，类似于行数
                    "titleKey": title if title == "" else hashlib.md5(
                        title.encode(encoding='utf-8')).hexdigest(),  # text的hash,
                    "id": hashlib.md5(content.encode(encoding='utf-8')).hexdigest(),  # text的hash
                    "timestamp": int(round(time.time() * 1000))
                }
            }
            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
            current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                          error,
                                          blank, total_line)


if __name__ == '__main__':
    # nohup python wudao_dirty_clean_multi.py > log/wudao_dirty_muti.out 2>&1 &
    # pre_file = "WanJuan1.0/TextBook-cn_format"
    source = "suolyer"
    subset = "wiki_zh"
    # 无最后斜杠
    base_dir = "/data/project/llm_data_tools/data" + "/" + source + "_" + subset
    # Get all jobs.
    # Each job corresponds to a file ends with .gz, with middle or head in it
    #
    jobs = get_all_files(base_dir, suffix1="_format")
    # print("TOTAL # JOBS:", len(jobs))
    # 线程池数
    pool_num = len(jobs)
    if pool_num > 120:
        pool_num = 120
    # 跳过文件
    skip_dict = {
    }
    # log.logger.info("———— 开始 ————")
    # process(base_dir, format_dir, dirty_dir, "", "")
    # log.logger.info("———— 结束 ————")
    with Pool(pool_num) as p:
        p.map(run, jobs)
