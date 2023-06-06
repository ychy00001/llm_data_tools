# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService

if __name__ == '__main__':
    testService = ChatPromptService()
    page_size = 1000
    total = 0
    with open("./data/format_2m_data.json", "a", encoding='utf-8') as f:
        for i in range(20001):
            page = i + 1
            total = total + 1000
            print(f"page：{page}， page_size：{page_size} \n 当前已处理数据：{total}")
            datalist = testService.select_data(page, page_size)
            for k in datalist:
                result = dict(
                    prompt=k.prompt,
                    output=k.target
                )
                data = json.dumps(result, ensure_ascii=False)
                f.write(data)
                f.write("\n")
