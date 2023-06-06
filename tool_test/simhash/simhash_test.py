from simhash import Simhash, SimhashIndex
from multiprocessing import Pool
import re
import os

# 多协程控制
n_jobs = 2
width = 5
hash_k = 23
max_hash_len = 0


def split_list(list, n):
    length = len(list)
    return [list[i * length // n: (i + 1) * length // n] for i in range(n)]


def get_features(s):
    '''
    根据宽度特征抽取
    print(get_features("我在家里写作业"))
    ['我在家里写作', '在家里写作业']
    '''
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def find_match(args):
    i, index = args
    value_dict = {}
    for item in i:
        flag = 1
        try:
            now_list = index.get_near_dups(item[1])
            for x in now_list:
                if int(x) >= int(item[0]):
                    continue
                flag = 0
                break
            value_dict[item[0]] = flag
        except:
            value_dict[item[0]] = flag
    return value_dict


if __name__ == '__main__':
    # 获取内容hash值
    hashes = []
    members = []
    with open("./simhash/test_data.txt", "r") as f:
        lines = f.readlines()
        for idx, i in enumerate(lines):
            try:
                member = i
                if max_hash_len == 0:
                    hashes.append((str(idx), Simhash(get_features(i))))
                else:
                    hashes.append((str(idx), Simhash(get_features(i[:max_hash_len]))))
                members.append(member)
            except:
                continue
    print(f" hashes:{hashes}")
    print(f" members:{members}")
    # 初始化hash索引  k=海明距离 越大表示相似内容判断的误差越大，就是将更大不太相似的判断为相似
    index = SimhashIndex(hashes, k=hash_k)
    print("Finish building index!")

    # 数据分片
    n_hashes = split_list(hashes, n_jobs)

    # 执行
    with Pool(n_jobs) as p:
        temp_dict = p.map(find_match, [(i, index) for i in n_hashes])
    value_dict = {}
    for dict in temp_dict:
        for i in dict:
            value_dict[i] = dict[i]
    print("Finish finding matches!")
    print(f"result: {value_dict}")

    mem_hashes = list(zip(members, hashes))
    # 查看相似文本
    for mem, a_hash in mem_hashes:
        if value_dict[a_hash[0]] != 1:
            print(f"相似段落：{mem}")
