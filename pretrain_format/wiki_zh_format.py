import sys
import os
import json
import time
import hashlib
import psycopg2
import shutil
from psycopg2.errors import UniqueViolation
from psycopg2.errors import InvalidTextRepresentation
from json.decoder import JSONDecodeError

sys.path.append("..")
from common.logger import Logger

# 用来配置的变量
base_dir = "/data/project/llm_data_tools/data/wiki_zh"
format_dir = base_dir + "_format/"
# 跳过文件
skip_dict = {
}

# shutil.rmtree(format_dir)
os.makedirs(format_dir, exist_ok=True)

log = Logger('./log/wiki_zh.log', level='debug')

conn = psycopg2.connect(database="postgres", user="admin", password="qewr1234", host="172.17.0.1", port="8432")
log.logger.info("Opened database successfully")

cur = conn.cursor()


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


def add_db(title, content, file_name):
    sql = """INSERT INTO wiki_zh (title,content, file_name, origin) VALUES (%s, %s, %s, %s)"""
    params = (title, content, file_name, "wiki_zh")
    cur.execute(sql, params)
    conn.commit()


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


if __name__ == '__main__':

    log.logger.info("———— 开始 ————")
    # 获取待去重文件
    deduplicate_file = [f"{base_dir}/{i}" for i in os.listdir(base_dir)]
    # -- 待去重文件列表 = []
    log.logger.info(f"\n总共{len(deduplicate_file)}个文件")

    # 实际处理
    file_count = 0
    total_line = 0
    for file_item in deduplicate_file:
        base_file_name = os.path.basename(file_item)
        # 跳过整个文件
        if base_file_name in skip_dict.keys() and skip_dict[base_file_name] == "all":
            log.logger.info(f"\n文件：{base_file_name}已完成，跳过！")
            continue

        file_count += 1
        log.logger.info(f"\n处理第{file_count}个文件: {file_item}")

        # 读取原始谁
        # 读取数据
        with open(file_item, 'r', encoding='utf-8') as fcc_file:
            process_data = json.load(fcc_file)

        # 计算总行数
        # line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])
        line_count = len(process_data)

        i = 0
        repeat = 0
        error = 0
        blank = 0
        # 进度条记录
        percent_step = 20
        current_percent = 0
        for data_item in process_data:
            with open(format_dir + base_file_name, "a", encoding='utf-8') as f:
                i += 1
                # 跳过行数
                if base_file_name in skip_dict.keys():
                    if skip_dict[base_file_name] > i:
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line)
                        continue
                    elif skip_dict[base_file_name] == i:
                        log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")
                total_line += 1
                line = json.dumps(data_item, ensure_ascii=False)
                title = data_item["title"].strip()
                content = data_item["content"].strip()

                # 写入数据库 跳过数据库的重复异常
                try:
                    add_db(title, content, base_file_name)
                except UniqueViolation as e:
                    repeat += 1
                    if len(line) > 500:
                        line = line[:500]
                    log.logger.warning(f'重复数据：{line}')
                    conn.rollback()
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line)
                    continue
                except InvalidTextRepresentation as e1:
                    error += 1
                    if len(line) > 500:
                        log.logger.warning(f'数据库json解析异常：{line[:500]}...')
                    else:
                        log.logger.warning(f'数据库json解析异常：{line}')
                    conn.rollback()
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line)
                    continue

                # 写入文件
                if not content.startswith(title):
                    content = title + "\n\n" + content

                result = {
                    "text": content,
                    "meta": {
                        "source": "wiki_zh",
                        "subset": "wiki_zh_20230520",
                        "type": "baike",
                        "title": title,
                        "lang": "zh",
                        "fileIdx": base_file_name,
                        "idx": i,  # 本文件内的数据序号，类似于行数
                        "titleKey": hashlib.md5(title.encode(encoding='utf-8')).hexdigest(),
                        "id": hashlib.md5(content.encode(encoding='utf-8')).hexdigest(),  # text的hash
                        "timestamp": int(round(time.time() * 1000))
                    }
                }
                data = json.dumps(result, ensure_ascii=False)
                f.write(data)
                f.write("\n")
                current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat, error,
                                              blank, total_line)

    log.logger.info("———— 结束 ————")
