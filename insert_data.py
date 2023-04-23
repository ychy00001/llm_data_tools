# -*- coding: utf-8 -*-
import common.config as config
from service.chat_prompt_service import ChatPromptService

if __name__ == '__main__':
    testService = ChatPromptService()
    testResult = testService.insert("aaa", "bbb")
    print(testResult)
