# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService


def random_ids(start, end, count):
    # 从start 到 end 中 随机生成数据[start, x, x, x, end] 包头包尾
    return random.sample(range(start, end), count)


if __name__ == '__main__':
    # 总数据2924613   3082轮+最后一轮
    # 生成924613个id
    # 一次随机500个随机值，然后更新数据库
    testService = ChatPromptService()
    count = 300
    total = 0
    total_loop = 9740
    for i in range(total_loop):
        # start : 1 end:300
        start = total + 1
        end = start + count - 1
        print(f"当前轮数：{i}, 开始：{start}， 结束：{end} \n 当前已处理数据：{total}, 每轮处理数据：{count}, 每轮删除数据:{int(count / 3)}")
        del_ids = random_ids(start, end, int(count / 3))
        testService.del_data(del_ids)
        total += count
