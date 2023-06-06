# -*- coding: utf-8 -*-
import json
import random
import sys
from service.chat_prompt_service import ChatPromptService
import os
import re


def process_content(text):
    # 移除图片链接 ![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)
    # 移除广告连接  [填写信息](http://cn.mikecrm.com/aIDshQc)
    # 移除特殊广告链接1 [芥末堆网](//www.jiemodui.com)
    # 移除特殊广告链接2 [芥末堆内容合作](/Cooperation)
    text = re.sub(r'!?\[.*?\]\([a-zA-z://]*?[^\s]*?\)', "", text)

    # 截取4000长度
    if len(text) > 4000:
        text = text[:4000]
    return text


'''
处理摘要数据：
summary{{方直科技拟以自有资金1.2亿元共同投资设立嘉道方直投资基金}}
text{{多知网5月26日消息，今日，方直科技发公告，拟用自有资金人民币1.2亿元，与深圳嘉道谷投资管理有限公司、深圳嘉道功程股权投资基金（有限合伙）共同发起设立嘉道方直教育产业投资基金（暂定名）。该基金认缴出资总规模为人民币3.01亿元。基金的出资方式具体如下：![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)出资进度方面，基金合伙人的出资应于基金成立之日起四年内分四期缴足，每期缴付7525万元；各基金合伙人每期按其出资比例缴付。合伙期限为11年，投资目标为教育领域初创期或成长期企业。截止公告披露日，深圳嘉道谷投资管理有限公司股权结构如下:![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092525724.png)截止公告披露日，深圳嘉道功程股权投资基金产权结构如下:![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092538802.png)公告还披露，方直科技将探索在中小学教育、在线教育、非学历教育、学前教育、留学咨询等教育行业其他分支领域的投资。方直科技2016年营业收入9691万元，营业利润1432万元，归属于普通股股东的净利润1847万元。（多知网 黎珊）}}
'''
TEMPLATE1 = "根据提供的上下文进行总结。上下文：{}，总结："
TEMPLATE2 = "请分析下述文本，给出文本的摘要内容。文本：{}，摘要："
TEMPLATE3 = "根据上下文尽可能的回答用户所提交的问题。上下文：{},问题：根据上文给出合理且概括全面的摘要信息。回答："
TEMPLATE4 = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.\n\n\n\nUser:根据给定的文本生成摘要信息。\n\nText: {}\n\nAssistant:"
TEMPLATE5 = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\nWrite a summary from the input text\n\n### Input:\n{}\n\n### Response:"
TEMPLATE_LIST = [TEMPLATE1, TEMPLATE2, TEMPLATE3, TEMPLATE4, TEMPLATE5]

if __name__ == '__main__':
    # 一共24500个文件
    with open("./data/abstract_24500_data.json", "a", encoding='utf-8') as f:
        for i in range(24500):
            file_name = f"./data/chinese_abstractive_corpus/copus/{i + 1}.txt"
            if os.path.exists(file_name) is False:
                print(f"文件：{file_name}不存在")
                continue
            print(f"process：{file_name}")

            # 读文件
            r_f = open(file_name)
            line = r_f.readline()
            count = 1
            while line and count <= 2:
                if count == 1:
                    # summary
                    summary = line[9:len(line) - 3]
                else:
                    # text
                    content = line[6:len(line) - 2]
                line = r_f.readline()
                count += 1
            r_f.close()

            summary = summary.strip()
            content = process_content(content).strip()
            template_index = random.randint(0, 4)

            # 处理异常数据
            if content.isspace() or summary.isspace() or len(content) == 0 or len(summary) == 0:
                continue
            # 结束符为？ ?的移除
            last_char = summary[-1]
            if last_char == "?" or last_char == "？":
                continue

            # 格式化写入文件
            result = dict(
                prompt=TEMPLATE_LIST[template_index].format(content),
                output=summary
            )
            data = json.dumps(result, ensure_ascii=False)
            f.write(data)
            f.write("\n")
