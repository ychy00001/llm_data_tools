import sys
import os
import json
import time
import shutil
import hashlib
from json.decoder import JSONDecodeError
from multiprocessing import Pool

sys.path.append("..")
from common.logger import Logger
from common.utils import get_all_files
os.makedirs("./log", exist_ok=True)
log = Logger('./log/red_pajamas.log', level='debug')


def process_log(current_percent, percent_step, file_name, current_line, line_count, repeat_count, error_count,
                blank_count, dirty):
    percent = current_line / line_count * 100
    if percent > current_percent:
        current_percent += percent_step
        log.logger.info(f"已完成{int(percent)}%")
    if percent == 100:
        log.logger.info(
            f"处理完成：{file_name} , 总行数：{current_line}, 重复行数：{repeat_count}, JSON异常行数：{error_count}, 脏数据：{dirty}")
    return current_percent


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def run(job):
    file_item = job[0]
    file_item_format = job[1]
    base_file_name = os.path.basename(file_item)

    # 跳过整个文件
    if base_file_name in skip_dict.keys() and skip_dict[base_file_name] == "all":
        log.logger.info(f"\n文件：{base_file_name}已完成，跳过！")
        return

    # 计算总行数
    line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])

    current_line = 0
    repeat = 0
    error = 0
    dirty = 0
    blank = 0
    # 进度条记录
    percent_step = 10
    current_percent = 0
    total_dirty_info = {}
    # 读取数据
    with open(file_item_format, "a", encoding='utf-8') as f:
        for item_line in open(file_item, 'r', encoding='utf8'):
            try:
                line_json = json.loads(item_line, strict=False)
            except JSONDecodeError as e:
                error += 1
                log.logger.error(f'JSON解析异常：{item_line}')
                current_percent = process_log(current_percent, percent_step, file_item, current_line, line_count,
                                              repeat,
                                              error, blank, dirty)
                continue
            # 跳过行数
            if base_file_name in skip_dict.keys():
                if skip_dict[base_file_name] > current_line:
                    current_percent = process_log(current_percent, percent_step, file_item, current_line, line_count,
                                                  repeat, error, blank, dirty)
                    continue
                elif skip_dict[base_file_name] == current_line:
                    log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")

            text = line_json["text"]
            meta = line_json["meta"]
            lang = "en"
            title = ""
            subset = "RedPajama"
            # book
            if "short_book_title" in meta:
                title = meta["short_book_title"]
                subset = "book"
            # c4
            if "language" in meta:
                lang = meta["language"]

            # 子集
            if "source" in meta:
                subset = meta["source"]

            if not text.startswith(title):
                text = title + "\n\n" + text


            current_line += 1
            # 写入文件
            result = {
                "text": text,
                "meta": {
                    "source": "RedPajama-Data",
                    "subset": subset,
                    "type": subset,
                    "title": title,
                    "lang": lang,
                    "fileIdx": base_file_name,
                    "idx": current_line,  # 本文件内的数据序号，类似于行数
                    "titleKey": title if title == "" else hashlib.md5(
                        title.encode(encoding='utf-8')).hexdigest(),  # text的hash,
                    "id": hashlib.md5(text.encode(encoding='utf-8')).hexdigest(),  # text的hash
                    "timestamp": int(round(time.time() * 1000))
                }
            }

            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
            current_percent = process_log(current_percent, percent_step, file_item,
                                          current_line, line_count, repeat, error, blank, dirty)
    log.logger.info(f"总信息：{total_dirty_info}")


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("请设置待清洗目录")
    # pre_file = sys.argv[1]
    pre_file = "RedPajama"
    # 无最后斜杠
    base_dir = "/data/project/llm_data_tools/data/" + pre_file

    # Get all jobs.
    # Each job corresponds to a file ends with .gz, with middle or head in it
    #
    jobs = get_all_files(base_dir, suffix1="_format")
    # print("TOTAL # JOBS:", len(jobs))
    # 线程池数
    pool_num = len(jobs)
    if pool_num > 50:
        pool_num = 50
    # 跳过文件
    skip_dict = {
    }

    with Pool(pool_num) as p:
        p.map(run, jobs)


    # 无最后斜杠
    # base_dir = "/data/project/llm_data_tools/data/RedPajama"
    # format_dir = base_dir + "_format/"
    # # 跳过文件
    # skip_dict = {
    # }
    # log.logger.info("———— 开始 ————")
    # process(base_dir, format_dir, "", "")
    # log.logger.info("———— 结束 ————")
