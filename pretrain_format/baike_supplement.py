import os
import json
import psycopg2
import time
from psycopg2.errors import UniqueViolation
from psycopg2.errors import InvalidTextRepresentation
from json.decoder import JSONDecodeError
import sys
import re
import hashlib
import shutil

sys.path.append("..")
from common.logger import Logger
from common.filter import is_contains_chinese

# 已自己百科的数据为基准，补充研究院的百科数据

log = Logger('./log/baike_supplement_part2.log', level='debug')

# 用来配置的变量
base_dir = "/data/project/llm_data_tools/data/baidu_baike_self_format_part2"
format_dir = base_dir + "_format/"
# 跳过文件
skip_dict = {
}

# shutil.rmtree(format_dir)
os.makedirs(format_dir, exist_ok=True)

conn = psycopg2.connect(database="postgres", user="admin", password="qewr1234", host="172.17.0.1", port="8432")
log.logger.info("Opened database successfully")

cur = conn.cursor()


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def select_count_from_db(title):
    sql = f"""SELECT COUNT(*) FROM baike WHERE title=%s"""
    cur.execute(sql,(title,))
    conn.commit()
    result = cur.fetchall()
    return result[0][0]


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


def filter_content(text):
    text = re.sub(r'\[[0-9]*\]', "", text)
    return text


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

        # 计算总行数
        line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])

        i = 0
        repeat = 0
        error = 0
        blank = 0
        # 进度条记录
        percent_step = 10
        current_percent = 0
        for item_line in open(file_item, 'r', encoding='utf-8'):
            # 读取、分行、去重、写入
            with open(format_dir + base_file_name, "a", encoding='utf-8') as f:
                i += 1
                total_line += 1
                if base_file_name in skip_dict.keys():
                    if skip_dict[base_file_name] > i:
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line)
                        continue
                    elif skip_dict[base_file_name] == i:
                        log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")
                line = item_line.strip()

                if is_blank(line):
                    blank += 1
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line)
                    continue
                try:
                    line_json = json.loads(line, strict=False)
                except JSONDecodeError as e:
                    error += 1
                    log.logger.error(f'JSON解析异常：{line}')
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line)
                    continue

                title = line_json["meta"]["title"]

                # 判断买的baike数据是否存在该title
                try:
                    select_count = select_count_from_db(title)
                    if select_count > 0:
                        repeat += 1
                        if len(line) > 500:
                            line = line[:500]
                        log.logger.warning(f'重复数据：{line}')
                        conn.rollback()
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line)
                        continue
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
                    log.logger.warning(f'数据库json解析异常：{line[:300]}')
                    conn.rollback()
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line)
                    continue

                # 写入文件
                data = json.dumps(line_json, ensure_ascii=False)
                f.write(data)
                f.write("\n")
                current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat, error,
                                              blank, total_line)
    conn.close()
    log.logger.info("———— 结束 ————")
