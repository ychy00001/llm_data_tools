import re
import os
from flashtext import KeywordProcessor
import sys
from common.utils import cut_sent
from common.utils import check_str_count
from common.utils import str_char_info, is_zh_en, word_count, traditional2simplified, Ban2Quan, Quan2Ban
from common.full_half_char_util import convert as fh_convert, HF_PUNCTUATION, FH_PUNCTUATION, FH_COMMON_PUNCTUATION, \
    HF_COMMON_PUNCTUATION, FH_PUNCTUATION_MAP
from common.ner_tool import NerTool
from common.log import logger
from common.timer import get_time
from common.simhash_tool import SimhashTool

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


def process_content(text):
    # 移除图片链接 ![\\](http://www.duozhi.com/uploadfile/2017/0526/20170526092512491.png)
    # 移除广告连接  [填写信息](http://cn.mikecrm.com/aIDshQc)
    # 移除特殊广告链接1 [芥末堆网](//www.jiemodui.com)
    # 移除特殊广告链接2 [芥末堆内容合作](/Cooperation)
    text = re.sub(r'!?\[.*?\]\([a-zA-z://]*?[^\s]*?\)', "", text)
    # 移除.png .jpeg .jpg图片链接
    text = re.sub(r'[a-zA-z]+://[^\s]*.[png|jpg|jpeg]', "", text)
    return text


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


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def truncate_str(txt, length):
    # 截取4000长度
    if len(txt) > length:
        txt = txt[:len]
    return txt


############################脏词判断##############
def preprocess_news_title_content(title, content):
    '''
    新闻统一内容基础处理
    '''
    # 移除头尾的作者 编辑信息
    author_news_keywords = ["作者", "发布", "版", "记者", "编辑", "研报", "学者", "链接"]
    content_split = content.split("\n")
    if len(content_split) > 1:
        for kw in author_news_keywords:
            if content_split[0] != "" and kw in content_split[0]:
                content_split[0] = ""
            if content_split[-1] != "" and kw in content_split[-1]:
                content_split[-1] = ""
    content = "\n".join(content_split)

    # 匹配异常的头尾信息 （重点处理了Wudao_news里面的内容）
    content = re.sub(r'\(图源[\s\S]+?\)', "", content)
    content = re.sub(r'特别声明:以上文章内容[\s\S]+?请于作品发表后的30日内与.*?联系。', "", content)
    content = re.sub(r'\(新华网[\s\S]+?\)', "", content)
    content = re.sub(r'新华网[\s\S]+? 文\s', "", content)
    content = re.sub(r'\S+? / 文', "", content)
    content = re.sub(r'文 / \S+? (\s*?>\S+? )?', "", content)
    content = re.sub(r'\([^\(]*?关注[\s\S]*?分享\)', "", content)
    content = re.sub(r'[「#【\[][^「#【\[]+?[\]」#】]', "", content)
    # 放在最后
    count = 3
    while content.startswith("(") and count > 0:
        content = re.sub(r'^[\(][^\(]*?[\)]', "", content)
        count = count - 1
    content = content.replace("图片来源网络", "")
    content = content.replace("(图片来源于网络)", "")
    content = content.replace(r'xyy', "")
    content = content.replace(r'小密语录:', "")
    content = content.replace(r'(干货)', "")
    content = content.replace(r'图/', "")

    title = re.sub(r'[「#【\[][^「#【\[]+?[\]」#】]', "", title)
    # 放在最后
    count = 3
    while title.startswith("(") and count > 0:
        title = re.sub(r'^[\(][^\(]*?[\)]', "", title)
        count = count - 1
    title = title.replace(r'(干货)', "")

    content = content.strip()
    title = title.strip()
    return title, content


def preprocess_title_content(title, content, lang="zh"):
    # 内容预处理
    content = re.sub(r'\n{3,}', "\n", content)
    content = re.sub(r'\.{6,}', ".", content)
    content = re.sub(r'\s{3,}', " ", content)
    content = re.sub(r'_{3,}', "_", content)
    content = re.sub(r'-{3,}', "-", content)
    content = re.sub(r'={3,}', "=", content)
    content = re.sub(r'!+', "!", content)
    content = re.sub(r'！+', "！", content)
    content = re.sub(r'~+', "~", content)

    # 移除特殊符号 <U+0097>等
    format_content = ''
    for char in content:
        if '\u0080' <= char <= '\u009F':
            continue
        format_content += char
    content = format_content

    # 繁体转减简体
    content = traditional2simplified(content)
    title = traditional2simplified(title)

    # 半角转全角
    if lang == "zh":
        # 半角符号转全角符号*、#、-、|移除
        content = fh_convert(content, HF_COMMON_PUNCTUATION, HF_PUNCTUATION, FH_PUNCTUATION_MAP, skip="*#-|")
        title = fh_convert(title, HF_COMMON_PUNCTUATION, HF_PUNCTUATION, FH_PUNCTUATION_MAP, skip="*#-|")
    else:
        # 全角符号转半角符号 *、#、-、|移除
        content = fh_convert(content, FH_COMMON_PUNCTUATION, FH_PUNCTUATION, skip="*#-|")
        title = fh_convert(title, FH_COMMON_PUNCTUATION, FH_PUNCTUATION, skip="*#-|")

    content = content.strip()
    title = title.strip()
    return title, content


dirty_char_processor = KeywordProcessor(case_sensitive=True)
novel_char_processor = KeywordProcessor(case_sensitive=True)
# 基础脏词  移除掉的关键词："来源：" "日报道" "刚刚过去的20" "视频" "图片"
dirty_list = ["catIdx=", "px", "（）", "display=", "hn=", "rm=", "rthumb", "jenolan", "f=y", "下图", "配图",
              "PS：", "表格", "(图)", "网络赌博", "组图", "图二", "原标题", "[微博]", "请访问", "[1]", "大家好", "一起来看一下",
              "www", "●", "◆", "★", "☆", "http", "https", ".org", ".com", ".jpg", "www", "内容简介",
              "<img", "time=", "美女零距离", "KTV包厢", "……………", "", "更新日期", "目录", "前言", "应用介绍",
              "下载即送", "张)", "软件功能", "删档", "f=t", "\n\n\n\n\n", "笔者", "WWW", "HTTP", "name=", "𫇴", "1. \n  2", "专家简介",
              "在线", "秒杀", "【精品", "报讯", "记者", "小编", "网友", "网报", "简书", "须知", "图片来自", "|\n|",
              "请登录", "热线", "订阅", "往期推荐", "phone number", "下载链接", "大乐透", "体彩", "双色球", "福彩", "开奖",
              "▋", "卐", "┣", "推荐阅读", "友情链接", "您的位置", "门票优惠", "下一篇", "图片来源", "来源：", "培训", "当前位置",
              "咨询", "下载", "会员", "资料图", "点赞", "老铁", "推广", "免注册", "———————"]
ai_list = ["作为AI", "作为 AI", "一个AI", "AI语言模型"]
# 无用小说 "道法自然"  "修炼" "乾坤"  "古装", "言情", "佛门"， "重生"
novel_dirty_list = ["玄幻", "仙侠", "撒糖", "霸道总裁", "暖男", "三角恋", "白马王子", "婊", "侍寝",
                    "妖兽", "银狐", "白蛇", "鬼医", "圣手", "宠妻", "钛合金", "仙侠", "仙界", "修仙", "灵根", "筑基", "元婴",
                    "散仙", "剑修", "灵兽", "法宝", "剑灵", "道侣", "灵石", "剑诀", "阵法", "仙术", "逆天", "仙帝",
                    "天劫", "魔修", "空间戒指", "长生", "雷劫", "三千大道", "飞剑", "炼丹炉", "灵气复苏", "剑意",
                    "虚无境", "诛仙", "羽化", "少年老成", "神识", "天眼", "灵台清明", "仙阵", "虚灵", "世界法则", "六道轮回",
                    "吸血鬼", "后宫", "小说网", "网络小说", "起点网", "小说阅读网", "恐怖小说", "VIP章", "起点中文", "原创小说", "文学网",
                    "连载", "小说网", "网游类小说", "都市言情", "网络作家", "晋江文学城", "转载", "原创", "网文", "重磅消息"]
# r'(\w ){4,}'   a o d o a u
# r"[0-9]\.[\s\S]{,10}[0-9]\."    1. \n  2. \n  3. \n  4.
regex_list = [r'(\w ){4,}', r"(\w\.[\s\S]{,7}){5,}"]
title_dirty = ["报告", "站", "|", "注意", "招聘", "祝贺", "好文"]

dirty_char_processor.add_keywords_from_list(dirty_list + ai_list)
novel_char_processor.add_keywords_from_list(novel_dirty_list)
ywz_data = open(f"{os.path.dirname(os.path.abspath(__file__))}/../yanwenzi/data/yanwenzi.json", "r",
                encoding="utf-8").read()
ywz_data = eval(ywz_data)
ywz = Yanwenzi(ywz_data)


def is_dirty_exam(title, content):
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    result, dirty_char_list = contains_yanwenzi(content)
    if result:
        return f"存在颜文字\t{dirty_char_list}\t"
    result, dirty_char_list = contains_emoji(content)
    if result:
        return f"存在emoji表情\t{dirty_char_list}\t"

    return False


def is_dirty_web(title, content):
    '''
    爬取网页数据清洗
    '''
    # result, dirty_char_list = contains_sort_content(content, min_content=1000, min_cent=4)
    # if result:
    #     return f"存在内容太短\t{dirty_char_list}\t"
    # result, dirty_char_list = contain_dirty_title(title, content)
    # if result:
    #     return f"存在脏标题\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_dirty_novel_char(title, content)
    # if result:
    #     return f"存在脏小说\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_yanwenzi(content)
    # if result:
    #     return f"存在颜文字\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_emoji(content)
    # if result:
    #     return f"存在emoji表情\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_repeat_char(content)
    # if result:
    #     return f"存在重复字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_err_char(content)
    # if result:
    #     return f"存在异常字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_en_char(content)
    # if result:
    #     return f"存在英文字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_sim_sent(content)
    # if result:
    #     return f"存在相似段落\t{dirty_char_list}\t"
    return False


def is_dirty_book(title, content):
    # 存在月日的信息的数据
    dirty_char_processor.add_keywords_from_list(["mathrm"])

    result, dirty_char_list = contains_sort_content(content, min_content=800)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    result, dirty_char_list = contain_dirty_title(title, content)
    if result:
        return f"存在脏标题\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_novel_char(title, content)
    if result:
        return f"存在脏小说\t{dirty_char_list}\t"
    result, dirty_char_list = contains_yanwenzi(content)
    if result:
        return f"存在颜文字\t{dirty_char_list}\t"
    result, dirty_char_list = contains_emoji(content)
    if result:
        return f"存在emoji表情\t{dirty_char_list}\t"
    result, dirty_char_list = contains_repeat_char(content)
    if result:
        return f"存在重复字符\t{dirty_char_list}\t"
    result, dirty_char_list = contains_err_char(content)
    if result:
        return f"存在异常字符\t{dirty_char_list}\t"
    result, dirty_char_list = contains_en_char(content)
    if result:
        return f"存在英文字符过多\t{dirty_char_list}\t"
    return False


def is_dirty_news(title, content):
    # 存在月日的信息的数据
    dirty_char_processor.remove_keywords_from_list(["记者"])

    result, dirty_char_list = contains_sort_content(content, min_content=800)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    result, dirty_char_list = contain_dirty_title(title, content)
    if result:
        return f"存在脏标题\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_novel_char(title, content)
    if result:
        return f"存在脏小说\t{dirty_char_list}\t"
    result, dirty_char_list = contains_yanwenzi(content)
    if result:
        return f"存在颜文字\t{dirty_char_list}\t"
    result, dirty_char_list = contains_emoji(content)
    if result:
        return f"存在emoji表情\t{dirty_char_list}\t"
    result, dirty_char_list = contains_repeat_char(content)
    if result:
        return f"存在重复字符\t{dirty_char_list}\t"
    result, dirty_char_list = contains_err_char(content)
    if result:
        return f"存在异常字符\t{dirty_char_list}\t"
    result, dirty_char_list = contains_en_char(content)
    if result:
        return f"存在英文字符过多\t{dirty_char_list}\t"
    result, dirty_char_list = contains_sim_sent(content)
    if result:
        return f"存在相似段落\t{dirty_char_list}\t"
    return False


def is_dirty_wudao(title, content):
    # 存在月日的信息的数据
    regex_list.extend([r'\d{1,2}月\d{1,2}日'])
    dirty_char_processor.add_keywords_from_list(["目前", "今日", "今年", "请输入", "门票", "二维码", "公众号", "介绍"])

    result, dirty_char_list = contains_sort_content(content, min_content=800)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    result, dirty_char_list = contain_dirty_title(title, content)
    if result:
        return f"存在脏标题\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_novel_char(title, content)
    if result:
        return f"存在脏小说\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_yanwenzi(content)
    # if result:
    #     return f"存在颜文字\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_emoji(content)
    # if result:
    #     return f"存在emoji表情\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_repeat_char(content)
    # if result:
    #     return f"存在重复字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_err_char(content)
    # if result:
    #     return f"存在异常字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_en_char(content)
    # if result:
    #     return f"存在英文字符过多\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_sim_sent(content)
    # if result:
    #     return f"存在相似段落\t{dirty_char_list}\t"
    return False


def is_dirty_law(title, content):
    # 移除这些脏词
    remove_dirty_char = ["管理规定", "管理办法", "更新日期", "目录", "前言", "晨报网"]
    dirty_char_processor.remove_keywords_from_list(remove_dirty_char)
    result, dirty_char_list = contains_sort_content(content, 200, 1)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_regexp(title, content)
    if result:
        return f"存在异常正则匹配\t{dirty_char_list}\t"
    result, dirty_char_list = contains_yanwenzi(content)
    if result:
        return f"存在颜文字\t{dirty_char_list}\t"
    result, dirty_char_list = contains_emoji(content)
    if result:
        return f"存在emoji表情\t{dirty_char_list}\t"
    result, dirty_char_list = contains_repeat_char(content)
    if result:
        return f"存在重复字符\t{dirty_char_list}\t"
    result, dirty_char_list = contains_err_char(content)
    if result:
        return f"存在异常字符\t{dirty_char_list}\t"
    return False


def is_dirty_medical(title, content):
    # 医疗数据清洗
    result, dirty_char_list = contains_sort_content(content, 290, 1)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_dirty_char(title, content)
    # if result:
    #     return f"存在脏词\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_dirty_regexp(title, content)
    # if result:
    #     return f"存在异常正则匹配\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_yanwenzi(content)
    # if result:
    #     return f"存在颜文字\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_emoji(content)
    # if result:
    #     return f"存在emoji表情\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_repeat_char(content)
    # if result:
    #     return f"存在重复字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_err_char(content)
    # if result:
    #     return f"存在异常字符\t{dirty_char_list}\t"
    return False


def is_dirty_cw(title, content):
    result, dirty_char_list = contains_sort_content(content, 200, 3)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    result, dirty_char_list = contain_dirty_title(title, content)
    if result:
        return f"存在脏标题\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"


def is_dirty_code(starts, content):
    if starts < 30:
        return f"星数太少\t{30}\t"
    result, dirty_char_list = contains_sort_content(content, 1500, 40)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"


def is_dirty_csl(title, content):
    # csl数据清理规则
    result, dirty_char_list = contains_sort_content(content, 40, 1)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"
    result, dirty_char_list = contain_dirty_title(title, content)
    if result:
        return f"存在脏标题\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"
    result, dirty_char_list = contains_dirty_regexp(title, content)
    if result:
        return f"存在异常正则匹配\t{dirty_char_list}\t"
    result, dirty_char_list = contains_yanwenzi(content)
    if result:
        return f"存在颜文字\t{dirty_char_list}\t"
    result, dirty_char_list = contains_emoji(content)
    if result:
        return f"存在emoji表情\t{dirty_char_list}\t"
    result, dirty_char_list = contains_repeat_char(content)
    if result:
        return f"存在重复字符\t{dirty_char_list}\t"
    result, dirty_char_list = contains_err_char(content)
    if result:
        return f"存在异常字符\t{dirty_char_list}\t"
    return False


def is_dirty_redpajama(title, content):
    # redpajam 清理
    result, dirty_char_list = contains_sort_content(content, min_content=50, min_cent=3)
    if result:
        return f"存在内容太短\t{dirty_char_list}\t"

    result, dirty_char_list = contains_dirty_char(title, content)
    if result:
        return f"存在脏词\t{dirty_char_list}\t"

    result, dirty_char_list = contains_dirty_regexp(title, content)
    if result:
        return f"存在异常正则匹配\t{dirty_char_list}\t"

    result, dirty_char_list = contains_emoji(content)
    if result:
        return f"存在emoji表情\t{dirty_char_list}\t"

    result, dirty_char_list = contains_repeat_char(content)
    if result:
        return f"存在重复字符\t{dirty_char_list}\t"

    result, dirty_char_list = contains_err_char(content)
    if result:
        return f"存在异常字符\t{dirty_char_list}\t"

    result, dirty_char_list = contains_zh_char(content)
    if result:
        return f"存在中文字符\t{dirty_char_list}\t"

    result, dirty_char_list = contains_sim_sent(content, max_sim_cent_count=4)
    if result:
        return f"存在相似段落\t{dirty_char_list}\t"
    return False


def is_dirty(title, content):
    result, dirty_char_list = contains_limit_content(content, min_content=1000, max_content=1500)
    if result:
        return f"存在限制内容\t{dirty_char_list}\t"
    # wiki 百科 清理规则
    # result, dirty_char_list = contains_sort_content(content, min_content=2000)
    # if result:
    #     return f"存在内容太短\t{dirty_char_list}\t"
    # result, dirty_char_list = contain_dirty_title(title, content)
    # if result:
    #     return f"存在脏标题\t{dirty_char_list}\t"
    # result, dirty_char_list = contain_err_num(title, content)
    # if result:
    #     return f"存在异常数字标题\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_dirty_char(title, content)
    # if result:
    #     return f"存在脏词\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_dirty_novel_char(title, content)
    # if result:
    #     return f"存在脏小说\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_yanwenzi(content)
    # if result:
    #     return f"存在颜文字\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_emoji(content)
    # if result:
    #     return f"存在emoji表情\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_repeat_char(content)
    # if result:
    #     return f"存在重复字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_err_char(content)
    # if result:
    #     return f"存在异常字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_en_char(content)
    # if result:
    #     return f"存在英文字符\t{dirty_char_list}\t"
    # result, dirty_char_list = contains_sim_sent(content)
    # if result:
    #     return f"存在相似段落\t{dirty_char_list}\t"
    #
    # if contain_chemical_equation(content):
    #     return "存在化学符号\t"
    # if contain_cut_novel(content):
    #     return "存在切分小说\t"
    # if contain_dirty_person(title, content):
    #     return "存在无名人物或公司\t"
    return False


# def contains_less_text(content):
#     if len(content) < 3000:
#         return True
#     return False

@get_time
def contain_dirty_person(title, content):
    '''
    人名检测，存在人名，并且content长度小于200则删除
    中文使用FoolNLTK
    英文使用StanfordCoreNLP
    '''
    if is_blank(title):
        return False
    # 基础人名检测 格式为 ：梁丁心，女，汉族，1982年8月生，山东乐陵人  切前30个字符都好分隔
    simple_head = content[:30]
    str_list = simple_head.split('，')
    if len(str_list) > 2 \
            and (str_list[1] == '男' or str_list[1] == '女'):
        return True

    tool = NerTool()
    res = tool.get_ner_zh(title)
    if len(res) > 1 and res[1] \
            and res[1][0] \
            and res[1][0][0] \
            and res[1][0][0][2] \
            and res[1][0][0][3] == title \
            and (
            res[1][0][0][2] == "person" or res[1][0][0][2] == "company" or res[1][0][0][2] == "org"):
        # 识别为名字则判断简介是否小于阈值
        if len(content) < 1000:
            return True
    else:
        # 不是中文人名, 使用英文实体检测是否为英文人名
        res = tool.get_ner_en(title)
        if len(res) > 0 and res[0] and res[0][1] \
                and (res[0][1] == "PERSON" or res[0][1] == "COMPANY"):
            # 识别为名字则判断简介是否小于阈值
            if len(content) < 1000:
                return True
    return False


@get_time
def contains_sim_sent(content, max_sim_cent_count=3):
    '''
    判断是否存在在相同的句子
    '''
    simtool = SimhashTool()
    # 获取一段文本中相似的的句子
    list = simtool.get_sim_sent(content)
    logger.debug(f"相似段落：{list}")
    if len(list) > max_sim_cent_count:
        return True, list
    return False, None


@get_time
def contains_err_char(content, proportion=0.2):
    '''
    判断句子是否存在过多标签符号
    '''
    str_info = str_char_info(content)
    total_len = str_info[0]
    punctuation_len = str_info[5]
    space_len = str_info[3]
    if (punctuation_len + space_len) / total_len > proportion:
        return True, "符号超过20%"
    return False, None


@get_time
def contains_en_char(content):
    '''
    判断句子中英比例失衡
    '''
    str_info = str_char_info(content)
    total_len = str_info[0]
    zh_len = str_info[1]
    en_len = str_info[2]
    punctuation_len = str_info[5]
    if en_len > 0 and zh_len > 0 and en_len / zh_len > 0.8:
        return True, "英中比例>0.8"
    return False, None


@get_time
def contains_zh_char(content):
    '''
    判断句子是否存在过多标签符号
    判断句子中英比例失衡
    '''
    str_info = str_char_info(content)
    total_len = str_info[0]
    zh_len = str_info[1]
    en_len = str_info[2]
    punctuation_len = str_info[5]
    if en_len > 0 and zh_len > 0 and zh_len / en_len > 0.8:
        return True, "中英比例>0.8"
    return False, None


@get_time
def contains_limit_content(content, min_content=100, max_content=1500):
    # 根据中英文判断长度，英文以单词数，中文以个数判断
    wold_len = word_count(content)
    if wold_len < min_content or wold_len > max_content:
        return True, f"<content_len <{min_content} > {max_content}"
    return False, None


@get_time
def contains_sort_content(content, min_content=100, min_cent=3):
    '''
    内容太短，基于长度和句子长度 综合判断
    '''
    sent_list = cut_sent(content)
    normal_list = []
    for item in sent_list:
        if len(item) > 2:
            normal_list.append(item)

    # 根据中英文判断长度，英文以单词数，中文以个数判断
    wold_len = word_count(content)
    if wold_len < min_content:
        return True, f"content_len<{min_content}"
    if len(normal_list) < min_cent:
        return True, f"sentence_len<{min_cent}"
    return False, None


@get_time
def contain_cut_novel(content):
    '''
    部分数据切分时，把小说内容切分开一半
    '''
    sub_content = content[:200]
    if re.search('第.*?章', sub_content):
        return True
    return False


@get_time
def contain_err_num(title, content):
    '''
    标题有异常数字,移除年的判断，因为可能有年名称的数据
    '''
    # year_obj = re.search(r'[0-9]{4}', title)
    # if year_obj and (int(year_obj.group()) < 2021 or int(year_obj.group()) > 2023):
    #     return True, year_obj.group()
    num_obj = re.search(r'[0-9]', title)
    if num_obj and num_obj.group() and ("植物" in content or "版" in title):
        return True, "植物书籍编号"
    return False, None


def contain_dirty_title(title, content):
    '''
    脏词标题
    '''
    for item in title_dirty:
        if item in title:
            return True, item
    return False, None


@get_time
def contain_chemical_equation(content):
    '''
    判断是否存在化学方程式，当前使用数据集的逻辑来判断，没有用化学方程式的规则判断
    四聚甘氨酸是一种化学物质，化学式为C8H14N4O5。
    乙基叠氮乙酸酯是一种化学物质，化学式是C4H7N3O2。
    L(-)-甲基磺酰乙酯是一种化学物质，分子式是C6H12O5S。
    所有文本类似该样式，则规则为截取前100个字符，看是否存在"是一种化学物质"的文字
    '''
    sub_content = content[:50]
    if re.search('是一种化学物质', sub_content):
        return True
    return False


@get_time
def contains_dirty_novel_char(title, content):
    dirty_found = novel_char_processor.extract_keywords(content)
    logger.debug("脏小说词：%s", dirty_found)
    if len(dirty_found) > 0:
        return True, dirty_found
    return False, None


@get_time
def contains_dirty_regexp(title, content):
    for i in regex_list:
        searchObj = re.search(i, content, re.M | re.I)
        if searchObj:
            logger.debug("异常正则匹配：%s", searchObj.group())
            return True, searchObj.group().replace("\n", " ")
    return False, None


@get_time
def contains_dirty_char(title, content):
    if title == "基本资料" or title == "注":
        return True, "title=基本资料 或 注"
    if title == "真．三国无双7 Blast" or title == "例如":
        return True, "title=真三国无双 或 例如"
    if title.startswith("电视动画版") or title.startswith("注："):
        return True, "title=电视动画版 或 注："
    if '其他名称' in content:
        return True, "其他名称"
    dirty_found = dirty_char_processor.extract_keywords(content)
    logger.debug("脏词：%s", dirty_found)
    if len(dirty_found) > 0:
        return True, dirty_found
    return False, None


@get_time
def contains_yanwenzi(content):
    result = ywz.detect(content)
    if len(result) > 0:
        return True, result
    return False, None


@get_time
def contains_repeat_char(content):
    """检查某句话中是否有过多的某字符（多出现于wiki的表格中）"""
    for space in ["\t\t", "//", "__", "~~", "－－", "··", "!!"]:
        # num_space = content.count(space)
        num_space = check_str_count(content, space)
        if num_space > 5 or (num_space > 1 and num_space > len(content) // 10):
            return True, space
    return False, None


@get_time
def contains_emoji(text):
    try:
        emoji_list = emoji.distinct_emoji_list(text)
        normal_list = []
        for i in emoji_list:
            # 书中好多Copyright信息
            if i == "©":
                continue
            normal_list.append(i)
        if len(normal_list) > 0:
            return True, normal_list
        return False, None
    except IndexError:
        return False, None
############################脏词判断##############
