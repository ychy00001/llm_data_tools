import os
import json
import psycopg2
import time
from psycopg2.errors import UniqueViolation
from psycopg2.errors import InvalidTextRepresentation
from json.decoder import JSONDecodeError
import sys
import hashlib
import shutil

sys.path.append("../..")
from common.logger import Logger

log = Logger('baike.log', level='debug')

# 用来配置的变量
base_dir = "/data/project/llm_data_tools/data/baike"
format_dir = base_dir + "_format/"
# 跳过文件
skip_dict = {
    "baike176c0308ce594e2c849fbeea94ab9c45.1594438.json": "all",
    "baike230a279e68e04a75aaf3c4c799cbdeff.2176770.json": "all",
    "baike32da45a4aafe48ad871bf32d77b30aa6.1250257.json": "all",
    "baike5c1452a033994ab1ad2459f960937dbe.1547858.json": "all",
    "baike61b596feb4c140f3ab818c3f42fa2304.2685029.json": "all",
    "baike64522cea7e664847a1f49ab49378bfc8.2121590.json": "all",
    "baike84139a4586834993a9022921788ab86e.1778133.json": "all",
    "baikea9ae1667ded94ab893fbc0e75af48468.1993496.json": "all",
    "baikec0930378054a44d38e7ffc2076bdae0f.2466292.json": "all",
    "baikee60dfbcd58044191a56993882ebe6b38.1885192.json": 1229402,
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


def add_db(title, desc, summary, basic_info, other_info, additional_info, file_name):
    sql = """INSERT INTO baike (title,"desc",summary,basic_info,other_info,additional_info, file_name, origin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    params = (
        title, desc, summary, json.dumps(basic_info, ensure_ascii=False), json.dumps(other_info, ensure_ascii=False),
        additional_info, file_name, "buy_baike")
    cur.execute(sql, params)
    conn.commit()


def format_result_str(title, desc, summary, basic_info, other_info):
    basic_info_str = list_str(basic_info, "")
    other_info_str = list_str(other_info, "")
    return f'{title}\n\n{desc}\n{summary}\n{basic_info_str}\n{other_info_str}'


# 该方法不太可行
def list_str_test(info_list):
    json_str = json.dumps(info_list, ensure_ascii=False)
    json_str = json_str.replace("{", "")
    json_str = json_str.replace("}", "")
    json_str = json_str.replace("[", "")
    json_str = json_str.replace("]", "")
    json_str = json_str.replace("\"key\":", "")
    json_str = json_str.replace("\"value\":", "")
    json_str = json_str.replace("\"introduction\",", "")
    json_str = json_str.replace("\"", "")
    json_str = json_str.replace(" ", "")
    json_str = json_str.replace("0:", "")
    json_str = json_str.replace("1:", "")
    return json_str


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def list_str(info_list, start_str):
    for index, info_item in enumerate(info_list):
        if isinstance(info_item, list):
            start_str = list_str(info_item, start_str)
        else:
            if 'key' in info_item:
                key = info_item['key']
                value = info_item['value']
                if key != "introduction" and key != "tables":
                    start_str += f"{key},"
                if isinstance(value, list):
                    start_str = list_str(value, start_str)
                else:
                    start_str += f"{value},"
            else:
                # 非key的情况
                keys = info_item.keys()
                if is_contains_chinese(''.join(keys)):
                    # 存在中文 拼接 key, value
                    for dic_k in info_item:

                        start_str += f"{dic_k},"
                        if isinstance(info_item[dic_k], list):
                            start_str = list_str(info_item[dic_k], start_str)
                        else:
                            start_str += f"{info_item[dic_k]},"
                else:
                    # 非中文 拼接value
                    for dic_k in info_item:
                        if isinstance(info_item[dic_k], list):
                            start_str = list_str(info_item[dic_k], start_str)
                        else:
                            start_str += f"{info_item[dic_k]},"

    return start_str[:-1]


def process_bar(num, total):
    rate = float(num) / total
    ratenum = int(100 * rate)
    r = '\r进度:[{}{}]{}%'.format('*' * ratenum, ' ' * (100 - ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()


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
        percent_step = 5
        current_percent = 0
        for item_line in open(file_item, 'r', encoding='utf8'):
            # 读取、分行、去重、写入
            with open(format_dir + base_file_name, "a", encoding='utf-8') as f:
                i += 1
                if base_file_name in skip_dict.keys():
                    if skip_dict[base_file_name] > i:
                        current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat,
                                                      error, blank, total_line)
                        continue
                    elif skip_dict[base_file_name] == i:
                        log.logger.info(f"\n文件：{base_file_name}跳过:{skip_dict[base_file_name]}行")
                total_line += 1
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

                title = line_json["title"]
                desc = line_json["desc"]
                summary = line_json["summary"]
                basic_info = line_json["basic_info"]
                other_info = line_json["other_info"]
                additional_info = line_json["additional_info"]

                # 写入数据库 TODO 跳过数据库的重复异常
                try:
                    add_db(title, desc, summary, basic_info, other_info, additional_info, base_file_name)
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
                format_text = format_result_str(title, desc, summary, basic_info, other_info)
                result = {
                    "text": format_text,
                    "meta": {
                        "source": "baidu_baike",
                        "subset": "buy_baike_20M",
                        "type": "baike",
                        "title": title,
                        "lang": "zh",
                        "fileIdx": base_file_name,
                        "idx": i,  # 本文件内的数据序号，类似于行数
                        "titleKey": hashlib.md5(title.encode(encoding='utf-8')).hexdigest(),
                        "id": hashlib.md5(format_text.encode(encoding='utf-8')).hexdigest(),  # text的hash
                        "timestamp": int(round(time.time() * 1000))
                    }
                }
                data = json.dumps(result, ensure_ascii=False)
                f.write(data)
                f.write("\n")
                current_percent = process_log(current_percent, percent_step, file_item, i, line_count, repeat, error,
                                              blank, total_line)
    conn.close()
    log.logger.info("———— 结束 ————")
