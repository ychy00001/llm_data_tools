import sys
import os
import json
import time
import shutil
from json.decoder import JSONDecodeError
from multiprocessing import Pool

sys.path.append("..")
from common.logger import Logger
from common.filter import is_dirty

os.makedirs("./log", exist_ok=True)
log = Logger('./log/content_dirty_clean_multi.log', level='info')


def process_log(current_percent, percent_step, file_name, current_line, line_count, repeat_count, error_count,
                blank_count, dirty):
    percent = current_line / line_count * 100
    if percent > current_percent:
        current_percent += percent_step
        log.logger.info(f"已完成{int(percent)}%")
    if percent == 100:
        log.logger.info(
            f"处理完成：{file_name} , 总行数：{current_line}, 重复行数：{repeat_count}, JSON异常行数：{error_count}, 脏数据：{dirty}, 总处理行数：{total_count} 总脏数据：{total_dirty}")
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
    percent_step = 20
    current_percent = 0
    # 读取数据
    with open(file_item_format, "a", encoding='utf-8') as f, open(
            file_item_dirty, "a", encoding='utf-8') as f1:
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

            dirty_type = is_dirty(meta["title"], text)
            if dirty_type:
                dirty += 1
                log.logger.error(f'脏数据{dirty_type}：{item_line[:200]}')
                f1.write(item_line)
                current_percent = process_log(current_percent, percent_step, file_item, current_line, line_count,
                                              repeat,
                                              error, blank, dirty)
                continue

            current_line += 1
            # 写入文件
            result = {
                "text": text,
                "meta": {
                    "source": meta["source"],
                    "subset": meta["subset"],
                    "type": meta["type"],
                    "title": meta["title"],
                    "lang": meta["lang"],
                    "fileIdx": meta["fileIdx"],
                    "idx": current_line,  # 本文件内的数据序号，类似于行数
                    "titleKey": meta["titleKey"],
                    "id": meta["id"],  # text的hash
                    "timestamp": meta["timestamp"]
                }
            }

            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
            current_percent = process_log(current_percent, percent_step, file_item,
                                          current_line, line_count, repeat, error, blank, dirty)


def get_all_files(file_dir):
    '''
    获取所有文件，同时返回文件对应的格式化以及清楚的脏数据
    return: [(file_path, file_format_path, file_dirty_path), ()....]
    '''
    files = []
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            format_path = file_path.replace(file_dir, file_dir + "_clean")
            dirty_path = file_path.replace(file_dir, file_dir + "_dirty")
            make_file_dir(format_path)
            make_file_dir(dirty_path)
            files.append((file_path, format_path, dirty_path))
    return files


def make_file_dir(file_path):
    '''
    根据文件创建其路径的目录
    '''
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


if __name__ == '__main__':
    # 无最后斜杠
    base_dir = "/data/project/llm_data_tools/data/baike_supplement_no_longtail_sif"

    # 线程池数
    pool_num = 50
    # Get all jobs.
    # Each job corresponds to a file ends with .gz, with middle or head in it
    #
    jobs = get_all_files(base_dir)
    # print("TOTAL # JOBS:", len(jobs))

    # 跳过文件
    skip_dict = {
    }
    # log.logger.info("———— 开始 ————")
    # process(base_dir, format_dir, dirty_dir, "", "")
    # log.logger.info("———— 结束 ————")
    with Pool(pool_num) as p:
        p.map(run, jobs)
