import sys
import os
import json
import time
import shutil
import hashlib
from json.decoder import JSONDecodeError

sys.path.append("..")
from common.logger import Logger
from common.filter import is_dirty

os.makedirs("./log", exist_ok=True)
log = Logger('./log/pretrain_clean.log', level='debug')


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


def process_dirty(dirty_file, text, meta):
    result = {
        "text": text,
        "meta": meta
    }
    dirty_data = json.dumps(result, ensure_ascii=False)
    dirty_file.write(dirty_data)
    dirty_file.write("\n")


def process(base_dir, local_format_dir, local_dirty_dir, source, subset):
    # shutil.rmtree(local_format_dir)
    os.makedirs(local_format_dir, exist_ok=True)
    os.makedirs(local_dirty_dir, exist_ok=True)
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
            sub_format_dir = local_format_dir + "/" + base_file_name + "/"
            sub_dirty_dir = local_dirty_dir + "/" + base_file_name + "/"
            subset = os.path.basename(base_dir)
            process(file_item, sub_format_dir, sub_dirty_dir, source, subset)
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
            idx = 0
            repeat = 0
            error = 0
            dirty = 0
            blank = 0
            # 进度条记录
            percent_step = 20
            current_percent = 0
            # 读取数据
            with open(local_format_dir + base_file_name, "a", encoding='utf-8') as f, open(
                    local_dirty_dir + base_file_name, "a", encoding='utf-8') as dirty_file:
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

                    if is_dirty(meta["title"], text):
                        dirty += 1
                        total_dirty += 1
                        log.logger.error(f'脏数据：{item_line[:200]}')
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line, dirty, total_dirty)
                        process_dirty(dirty_file, text, meta)
                        continue

                    # 写入文件
                    idx += 1
                    result = {
                        "text": text,
                        "meta": {
                            "source": meta["source"],
                            "subset": meta["subset"],
                            "type": meta["type"],
                            "title": meta["title"],
                            "lang": meta["lang"],
                            "fileIdx": meta["fileIdx"],
                            "idx": idx,  # 本文件内的数据序号，类似于行数
                            "titleKey": hashlib.md5(meta["title"].encode(encoding='utf-8')).hexdigest(),
                            "id": meta["id"],  # text的hash
                            "timestamp": meta["timestamp"]
                        }
                    }
                    data = json.dumps(result, ensure_ascii=False)
                    f.write(data)
                    f.write("\n")
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error,
                                                  blank, total_line, dirty, total_dirty)


if __name__ == '__main__':
    # 无最后斜杠
    base_dir = "/data/project/llm_data_tools/data/news_2023_clean"
    format_dir = base_dir + "_ready/"
    dirty_dir = base_dir + "_dirty/"

    # 跳过文件
    skip_dict = {
    }
    log.logger.info("———— 开始 ————")
    process(base_dir, format_dir, dirty_dir, "", "")
    log.logger.info("———— 结束 ————")
