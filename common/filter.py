import re


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
