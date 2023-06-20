import re
from flashtext import KeywordProcessor
import sys
sys.path.append("..")
from yanwenzi.yanwenzi import Yanwenzi
import emoji


def is_continue(question, answer):
    if is_blank(question) or is_blank(answer):
        return True
    if len(question) + len(answer) > 2048:
        return True
    return False


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def is_not_blank(it):
    return not is_blank(it)


def process_content(text):
    # 移除图片链接 ![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)
    # 移除广告连接  [填写信息](http://cn.mikecrm.com/aIDshQc)
    # 移除特殊广告链接1 [芥末堆网](//www.jiemodui.com)
    # 移除特殊广告链接2 [芥末堆内容合作](/Cooperation)
    text = re.sub(r'!?\[.*?\]\([a-zA-z://]*?[^\s]*?\)', "", text)
    # 移除.png .jpeg .jpg图片链接
    text = re.sub(r'[a-zA-z]+://[^\s]*.[png|jpg|jpeg]', "", text)
    return text


def result_filter(result: dict):
    result['prompt'] = data_filter(result['prompt'])
    result['output'] = data_filter(result['output'])
    return result


def data_filter(data_str: str):
    # 替换  cwRong
    data_str = data_str.replace("cwRong", "RongGPT")
    # 移除图片 广告
    data_str = process_content(data_str)
    data_str = process_7ke(data_str)
    # 处理特殊字符
    data_str = data_str.replace("�", "")
    data_str = data_str.replace("", "")
    return data_str


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def process_7ke(data_str: str):
    # 替换<br/>为\n
    data_str = data_str.replace("<br/>", "\\n")
    # 替换<br>
    data_str = data_str.replace("<br>", " ")
    data_str = data_str.replace("<p>", "")
    data_str = data_str.replace("</p>", "")
    data_str = re.sub(r'<u>[^\s\s]*</u>?', "", data_str)
    data_str = data_str.replace("<u>", "")
    data_str = data_str.replace("</u>", "")
    data_str = data_str.replace("; ; ; ; ; ; ; ; ; ;", "")
    data_str = data_str.replace("; ; ; ; ; ; ", "")
    data_str = data_str.replace("; ; ; ; ", "")
    data_str = data_str.replace("( ; ; 　)", "( )")
    data_str = data_str.replace("（ ; ; ; ）", "( )")
    data_str = data_str.replace("\\\\_", "( )")
    data_str = data_str.replace("\\\\\\\\\\\\", "( )")
    data_str = data_str.replace("; ; ;", ";")
    # 替换&nbsp为空格
    data_str = data_str.replace("&nbsp", " ")
    return data_str


def truncate_str(txt, length):
    # 截取4000长度
    if len(txt) > length:
        txt = txt[:len]
    return txt


############################脏词判断##############

dirty_char_processor = KeywordProcessor(case_sensitive=True)
dirty_list = ["catIdx=", "px", "（）", "display=", "hn=", "rm=", "rthumb", "jenolan", "right", "f=y", "图片", "下图", "配图",
              "PS：", "表格", "回购", "来源：", "(图)", "网络赌博", "视频", "今年", "今日", "公布", "组图", "刚刚过去的20", "北京时间",
              "目前", "日报道", "原标题", "沪指", "下跌", "股票", "昨日", "[微博]", "请访问", "[1]", "大家好", "一起来看一下", "对于此事",
              "www"]
dirty_char_processor.add_keywords_from_list(dirty_list)

ywz_data = open("../yanwenzi/data/yanwenzi.json", "r", encoding="utf-8").read()
ywz_data = eval(ywz_data)
ywz = Yanwenzi(ywz_data)


def is_dirty(title, content):
    return contains_dirty_char(title, content) or contains_yanwenzi(content) or contains_repeat_char(
        content) or contains_emoji(content)


def contains_dirty_char(title, content):
    if title == "基本资料" or title == "注":
        return True
    if title == "真．三国无双7 Blast" or title == "例如":
        return True
    if title.startswith("电视动画版") or title.startswith("注："):
        return True
    if '今年' in content:
        return True
    dirty_found = dirty_char_processor.extract_keywords(content)
    if len(dirty_found) > 0:
        return True
    return False


def contains_yanwenzi(content):
    result = ywz.detect(content)
    if len(result) > 0:
        return True
    return False


def contains_repeat_char(content):
    """检查某句话中是否有过多的某字符（多出现于wiki的表格中）"""
    for space in ["-", "\n", "\t", "/", "_", "！", "~"]:
        num_space = content.count(space)
        if num_space > 7 or (num_space > 2 and num_space > len(content) // 10):
            return True
    return False


def contains_emoji(text):
    emoji_list = emoji.emoji_list(text)
    print(emoji_list)
    if len(emoji_list) > 0:
        return True
    return False
############################脏词判断##############
