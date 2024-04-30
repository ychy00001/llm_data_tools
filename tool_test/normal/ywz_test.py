import sys
import json
import emoji

sys.path.append("../..")
from yanwenzi.yanwenzi import Yanwenzi


def contains_emoji(text):
    emoji_list = emoji.emoji_list(text)
    if len(emoji_list) > 0:
        return True
    return False


# if __name__ == '__main__':
#     json_data = open("../../yanwenzi/data/yanwenzi.json", "r", encoding="utf-8").read()
#     json_data = eval(json_data)
#     ywz = Yanwenzi(json_data)
#     # result = ywz.detect("作品简介\n新手上道咯！~~！~！~！~{PS：万能女主，有可能O(∩_∩)O~跟动画有些8一样哈！}本人强烈的不喜欢砖头`不喜欢的表看！！！！")
#     result = ywz.detect(
#         "配图和表格的说明应该过滤掉，比如：“股市技术指标实战:原理、方法、技巧与实\n\n图5-12　绵世股份2014年8月26日筹码分布图\n\n对于本例而言，图5-12右侧为此股在2014年8月26日的静态筹码分布图。此时的股价仍处于没有启动阶段，而且在前期经历了长时间的震荡走势，使得市场的平均持仓成本几乎完全位于此时的10元以下的价位，”")
#     if len(result):
#         print("存在颜文字")
#     else:
#         print("没有颜文字")


if __name__ == '__main__':
    result = "配图和表格的说明应该过滤掉，👍比如：“股市技术指标实战:原理、方法、技巧与实\n\n图5-12　绵世股份2014年8月26日筹码分布图\n\n对于本例而言，图5-12右侧为此股在2014年8月26日的静态筹码分布图。此时的股价仍处于没有启动阶段，而且在前期经历了长时间的震荡走势，使得市场的平均持仓成本几乎完全位于此时的10元以下的价位，”"
    if contains_emoji(result):
        print("包含emoji")
    else:
        print("没有包含emoji")
