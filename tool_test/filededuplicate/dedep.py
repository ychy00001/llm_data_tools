import os
import json
import psycopg2

# 用来配置的变量
base_dir = "./baike"
conn = psycopg2.connect(database="postgres", user="postgres", password="qewr1234", host="172.17.0.1", port="15432")
print("Opened database successfully")

cur = conn.cursor()


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def add_db(title, desc, summary, basic_info, other_info, additional_info):
    cur.execute(f"INSERT INTO baike (title,'desc',summary,basic_info,other_info,additional_info) " +
                f"VALUES ('{title}', '{desc}', '{summary}', '{basic_info}', '{other_info}', '{additional_info}' )")
    conn.commit()
    pass


if __name__ == '__main__':
    print("———— 开始 ————")

    # 获取待去重文件
    deduplicate_file = [f"{base_dir}/{i}" for i in os.listdir(base_dir)]
    # -- 待去重文件列表 = []
    print(f"\n总共{len(deduplicate_file)}个文件")

    # 实际处理
    file_count = 0
    for file_item in deduplicate_file:
        file_count += 1
        print(f"\n处理第{file_count}个文件")

        # 计算总行数
        line_count = int(os.popen('wc -l %s' % file_item).read().split()[0])

        # 读取、分行、去重、写入
        i = 0
        for item_line in open(file_item):
            i += 1
            line = item_line.strip()
            if is_blank(line):
                continue

            line_json = json.loads(line)

            title = line_json["title"]
            desc = line_json["desc"]
            summary = line_json["summary"]
            basic_info = line_json["basic_info"]
            other_info = line_json["other_info"]
            additional_info = line_json["additional_info"]

            # 写入数据库 忽略重复异常
            add_db(title, desc, summary, basic_info, other_info, additional_info)

            percent = i / line_count * 10
            if percent == int(percent):
                print(f"已完成{int(percent) * 10}%")

    print("———— 结束 ————")
