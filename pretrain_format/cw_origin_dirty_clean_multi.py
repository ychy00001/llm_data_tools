import sys
import os
import json
import time
import shutil
from json.decoder import JSONDecodeError
from multiprocessing import Pool

sys.path.append("..")
from common.logger import Logger
from common.filter import is_dirty_cw, preprocess_title_content
from common.utils import get_all_files
import hashlib

os.makedirs("./log", exist_ok=True)
log = Logger('./log/cw_origin_dirty_clean_multi.log', level='info')


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


def run(job):
    file_item = job[0]
    file_item_format = job[1]
    file_item_dirty = job[2]
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
    with open(file_item_format, "a", encoding='utf-8') as f, open(
            file_item_dirty, "a", encoding='utf-8') as f1:
        with open(file_item, 'r', encoding='utf-8') as fcc_file:
            fcc_data = json.load(fcc_file)

        result_data = []
        for line_json in fcc_data:
            item_line = json.dumps(line_json, ensure_ascii=False)
            # 跳过行数
            if base_file_name in skip_dict.keys():
                if skip_dict[base_file_name] > current_line:
                    current_percent = process_log(current_percent, percent_step, file_item, current_line, line_count,
                                                  repeat, error, blank, dirty)
                    continue
                elif skip_dict[base_file_name] == current_line:
                    log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")

            title = line_json["question"]
            text = line_json["output"]
            source = line_json["source"]
            lang = line_json["lang"]

            dirty_type = is_dirty_cw(title, text)
            if dirty_type:
                if dirty_type in total_dirty_info.keys():
                    total_dirty_info[dirty_type] = total_dirty_info[dirty_type] + 1
                else:
                    total_dirty_info[dirty_type] = 1

                log.logger.debug(f'脏数据{dirty_type}：{item_line[:200]}')
                f1.write(dirty_type + " " + item_line +"\n")
                current_percent = process_log(current_percent, percent_step, file_item, current_line, line_count,
                                              repeat,
                                              error, blank, dirty)
                continue

            current_line += 1

            # if not text.startswith(title):
            #     text = title + "\n\n" + text
            # # 写入文件
            # result = {
            #     "text": text,
            #     "meta": {
            #         "source": "qa",
            #         "subset": source,
            #         "type": "qa",
            #         "title": title,
            #         "lang": lang,
            #         "fileIdx": base_file_name,
            #         "idx": current_line,  # 本文件内的数据序号，类似于行数
            #         "titleKey": hashlib.md5(title.encode(encoding='utf-8')).hexdigest(),  # text的hash,
            #         "id": hashlib.md5(text.encode(encoding='utf-8')).hexdigest(),  # text的hash
            #         "timestamp": int(round(time.time() * 1000))
            #     }
            # }

            # data = json.dumps(result, ensure_ascii=False)
            # f.write(data)
            # f.write("\n")
            result_data.append(line_json)
            current_percent = process_log(current_percent, percent_step, file_item,
                                          current_line, line_count, repeat, error, blank, dirty)
        data = json.dumps(result_data, ensure_ascii=False)
        f.write(data)

    log.logger.info(f"总信息：{total_dirty_info}")


if __name__ == '__main__':
    # nohup python cw_origin_dirty_clean_multi.py > log/cw_origin_dirty_muti.out 2>&1 &
    # if len(sys.argv) < 2:
    #     print("请设置待清洗目录")
    # pre_file = sys.argv[1]
    pre_file = "cw"
    # 无最后斜杠
    base_dir = "/data/project/llm_data_tools/data/" + pre_file

    # Get all jobs.
    # Each job corresponds to a file ends with .gz, with middle or head in it
    #
    jobs = get_all_files(base_dir, suffix1="_clean_origin", suffix2="_dirty_origin")
    # print("TOTAL # JOBS:", len(jobs))
    # 线程池数
    pool_num = len(jobs)
    if pool_num > 50:
        pool_num = 50
    # 跳过文件
    skip_dict = {
    }
    # log.logger.info("———— 开始 ————")
    # process(base_dir, format_dir, dirty_dir, "", "")
    # log.logger.info("———— 结束 ————")
    with Pool(pool_num) as p:
        p.map(run, jobs)
