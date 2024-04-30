import sys
import os
import json
import time
import shutil
import hashlib

sys.path.append("..")
from common.logger import Logger

os.makedirs("./log", exist_ok=True)
log = Logger('./log/csl.log', level='debug')


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


def process(base_dir, local_format_dir, source, subset):
    # shutil.rmtree(local_format_dir)
    os.makedirs(local_format_dir, exist_ok=True)
    # 获取待处理文件或者文件夹
    deduplicate_file = [f"{base_dir}/{i}" for i in os.listdir(base_dir)]
    # -- 待去重文件列表 = []
    log.logger.info(f"\n总共{len(deduplicate_file)}个文件或文件夹")

    # 实际处理
    file_count = 0
    total_line = 0
    for file_item in deduplicate_file:
        base_file_name = os.path.basename(file_item)
        if os.path.isdir(file_item):
            sub_format_dir = local_format_dir + "/" + base_file_name + "/"
            subset = os.path.basename(base_dir)
            process(file_item, sub_format_dir, source, subset)
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
            blank = 0
            # 进度条记录n%打印
            percent_step = 20
            current_percent = 0
            # 读取数据
            with open(local_format_dir + base_file_name, "a", encoding='utf-8') as f:
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

                    text = line_json["abstract"]
                    category = line_json["category"]
                    discipline = line_json["discipline"]
                    title = line_json["title"]
                    # 把引号去掉  100字符不要  关键词删除：笔者
                    text = text.replace("\"", "")

                    lang = "zh"
                    if base_file_name == "csl.gt.063023.jsonl":
                        lang = "en"

                    # 写入文件
                    result = {
                        "text": text,
                        "meta": {
                            "source": "csl",
                            "subset": category,
                            "type": discipline,
                            "title": title,
                            "lang": lang,
                            "fileIdx": base_file_name,
                            "idx": i,  # 本文件内的数据序号，类似于行数
                            "titleKey": hashlib.md5(title.encode(encoding='utf-8')).hexdigest(),  # text的hash,
                            "id": hashlib.md5(text.encode(encoding='utf-8')).hexdigest(),  # text的hash
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
    # 无最后斜杠
    base_dir = "/data/project/llm_data_tools/data/csl"
    format_dir = base_dir + "_format/"
    # 跳过文件
    skip_dict = {
    }
    log.logger.info("———— 开始 ————")
    process(base_dir, format_dir, "", "")
    log.logger.info("———— 结束 ————")
