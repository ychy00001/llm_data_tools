import sys
import os
import re
import json
import time
import hashlib
import psycopg2
import shutil
import traceback
from psycopg2.errors import UniqueViolation
from psycopg2.errors import InvalidTextRepresentation
import pyarrow as pa
import pyarrow.parquet as pq
from json.decoder import JSONDecodeError

'''
pip install pyarrow
pip install fastparquet
'''
sys.path.append("..")
from common.logger import Logger

# 用来配置的变量
base_dir = "/data/project/llm_data_tools/data/falcon_web"
format_dir = base_dir + "_format/"
back_dir = base_dir + "_back/"
# 跳过文件
skip_dict = {
}

# 读取back_dir目录文件 拼接skip_dict跳过文件
back_list = os.listdir(back_dir)
for list_item in back_list:
    skip_dict[list_item] = "all"

# shutil.rmtree(format_dir)
os.makedirs(format_dir, exist_ok=True)

log = Logger('./log/falcon_web.log', level='debug')

conn = psycopg2.connect(database="postgres", user="admin", password="qewr1234", host="172.17.0.1", port="8432")
log.logger.info("Opened database successfully")

cur = conn.cursor()


def add_db(url, content, dump, file_name):
    sql = """INSERT INTO falcon_web (url,content, file_name, origin) VALUES (%s, %s, %s, %s)"""
    params = (url[:1024], content, file_name, dump)
    cur.execute(sql, params)
    conn.commit()


def move_to_back(file):
    move_file(base_dir, back_dir, file)


def move_file(src_path, dst_path, file):
    try:
        # cmd = 'chmod -R +x ' + src_path
        # os.popen(cmd)
        f_src = os.path.join(src_path, file)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        f_dst = os.path.join(dst_path, file)
        shutil.move(f_src, f_dst)
    except Exception as e:
        print('move_file ERROR: ', e)
        traceback.print_exc()


def process_log(current_percent, percent_step, file_name, current_line, line_count, repeat_count, error_count,
                blank_count, total_count, valid_count):
    percent = current_line / line_count * 100
    if percent > current_percent:
        current_percent += percent_step
        log.logger.info(f"已完成{int(percent)}%")
    if percent == 100:
        log.logger.info(
            f"处理完成：{file_name} , 总行数：{current_line}, 有效行数：{valid_count}, 重复行数：{repeat_count}, 无效行数：{error_count}, 空行数：{blank_count}, 总处理行数：{total_count}")
    return current_percent


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
    idx_1 = 0
    idx_2 = 0
    for file_item in deduplicate_file:
        base_file_name = os.path.basename(file_item)
        # 跳过整个文件
        file_count += 1
        if base_file_name in skip_dict.keys() and skip_dict[base_file_name] == "all":
            log.logger.info(f"\n文件：{base_file_name}已完成，跳过！")
            continue

        log.logger.info(f"\n处理第{file_count}个文件: {file_item}")

        # 读取数据
        df = pq.read_table(file_item).to_pandas()

        # 计算总行数
        # line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])
        line_count = len(df)

        i = 0
        new_idx = 0
        repeat = 0
        error = 0
        blank = 0
        # 进度条记录
        percent_step = 20
        current_percent = 0
        # 对于每一行，通过列名name访问对应的元素
        for index, row in df.iterrows():
            with open(format_dir + "2021.json", "a", encoding='utf-8') as f1, open(format_dir + "2022.json", "a",
                                                                                   encoding='utf-8') as f2:
                i += 1
                # 跳过行数
                if base_file_name in skip_dict.keys():
                    if skip_dict[base_file_name] > i:
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line, valid_count=new_idx)
                        continue
                    elif skip_dict[base_file_name] == i:
                        log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")
                total_line += 1

                line = row
                url = row['url']
                content = row['content']
                dump = row['dump']

                # 移除不是2022和2021年的数据
                dump_year_search = re.search(r'[0-9]{4}', dump, re.M | re.I)
                if dump_year_search:
                    dump_year = dump_year_search.group()
                    if dump_year != "2021" and dump_year != "2022":
                        error += 1
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line, valid_count=new_idx)
                        continue
                else:
                    error += 1
                    log.logger.warning(f'无日期信息：{line[:500]}...')
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line, valid_count=new_idx)
                    continue

                # 写入数据库 跳过数据库的重复异常
                try:
                    add_db(url, content, dump, base_file_name)
                except UniqueViolation as e:
                    repeat += 1
                    if len(line) > 500:
                        line = line[:500]
                    log.logger.warning(f'重复数据：{line}')
                    conn.rollback()
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line, valid_count=new_idx)
                    continue
                except InvalidTextRepresentation as e1:
                    error += 1
                    log.logger.warning(f'数据库json解析异常：{line[:500]}...')
                    conn.rollback()
                    current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                  error, blank, total_line, valid_count=new_idx)
                    continue

                # 写入文件
                new_idx += 1
                dump_year = dump_year_search.group()
                if dump_year == "2021":
                    idx_1 += 1
                    result = {
                        "text": content,
                        "meta": {
                            "source": "falcon-refinedweb",
                            "subset": dump,
                            "type": "common_crawl",
                            "title": url,
                            "lang": "en",
                            "fileIdx": base_file_name,
                            "idx": idx_1,  # 本文件内的数据序号，类似于行数
                            "titleKey": hashlib.md5(url.encode(encoding='utf-8')).hexdigest(),
                            "id": hashlib.md5(content.encode(encoding='utf-8')).hexdigest(),  # text的hash
                            "timestamp": int(round(time.time() * 1000))
                        }
                    }
                    data = json.dumps(result, ensure_ascii=False)
                    f1.write(data)
                    f1.write("\n")
                elif dump_year == "2022":
                    idx_2 += 1
                    result = {
                        "text": content,
                        "meta": {
                            "source": "falcon-refinedweb",
                            "subset": dump,
                            "type": "common_crawl",
                            "title": url,
                            "lang": "en",
                            "fileIdx": base_file_name,
                            "idx": idx_2,  # 本文件内的数据序号，类似于行数
                            "titleKey": hashlib.md5(url.encode(encoding='utf-8')).hexdigest(),
                            "id": hashlib.md5(content.encode(encoding='utf-8')).hexdigest(),  # text的hash
                            "timestamp": int(round(time.time() * 1000))
                        }
                    }
                    data = json.dumps(result, ensure_ascii=False)
                    f2.write(data)
                    f2.write("\n")
                current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat, error,
                                              blank, total_line, valid_count=new_idx)
            # 移走当前文件到back文件
        move_to_back(base_file_name)
    log.logger.info("———— 结束 ————")
