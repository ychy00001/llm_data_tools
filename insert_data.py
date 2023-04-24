# -*- coding: utf-8 -*-
import json
from service.chat_prompt_service import ChatPromptService

if __name__ == '__main__':
    testService = ChatPromptService()
    count = 0
    with open('./data/total_all_chat_prompt.json', 'r') as prompt_file:
        prompt_data = json.load(prompt_file)
        for item in prompt_data:
            prompt = item["prompt"]
            target = item["target"]
            testService.insert(prompt, target)
            count += 1
            print(f"已处理:{count}条数据")
