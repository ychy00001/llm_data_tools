import re
import os
from flashtext import KeywordProcessor
import sys
from common.utils import check_str_count
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
# 基础脏词
dirty_list_1 = ["catIdx=", "px", "（）", "display=", "hn=", "rm=", "rthumb", "jenolan", "right", "f=y", "图片", "下图", "配图",
                "PS：", "表格", "回购", "来源：", "(图)", "网络赌博", "视频", "今年", "今日", "公布", "组图", "刚刚过去的20", "北京时间",
                "目前", "日报道", "原标题", "沪指", "下跌", "股票", "昨日", "[微博]", "请访问", "[1]", "大家好", "一起来看一下", "对于此事",
                "www", "参考来源", "相关条目", "参考著作", "●", "◆", "★", "☆","http", ".org", ".com", ".jpg", "via", "www.", "<img",
                "time="]
# 无用小说
dirty_list_2 = ["玄幻", "仙侠", "都市", "撒糖", "纠缠", "明星", "霸道", "总裁", "暖男", "偶像", "三角恋", "偶然相遇", "白马王子", "婊", "侍寝", "苍天",
                "妖兽", "银狐", "白蛇", "鬼医", "圣手", "邪王", "宠妻", "钛合金", "修炼", "仙侠", "仙界", "修仙", "灵根", "筑基", "金丹", "元婴",
                "散仙", "道家", "剑修", "丹药", "灵兽", "法宝", "剑灵", "道侣", "灵石", "剑诀", "阵法", "仙术", "重生", "逆天", "仙帝",
                "天劫", "魔修", "空间戒指", "五行", "长生", "道法自然", "乾坤", "雷劫", "三千大道", "飞剑", "炼丹炉", "灵气复苏", "剑意",
                "虚无境", "诛仙", "羽化", "少年老成", "佛门", "神识", "天眼", "灵台清明", "仙阵", "丹田", "虚灵", "世界法则", "六道轮回",
                "穿越", "魔术师", "魔法", "吸血鬼", "古装", "言情", "后宫", "至尊", "小说网", "网络小说", "起点网", "小说阅读网"]
dirty_list = dirty_list_1 + dirty_list_2

dirty_char_processor.add_keywords_from_list(dirty_list)
ywz_data = open(f"{os.path.dirname(os.path.abspath(__file__))}/../yanwenzi/data/yanwenzi.json", "r",
                encoding="utf-8").read()
ywz_data = eval(ywz_data)
ywz = Yanwenzi(ywz_data)


def is_dirty(title, content):
    if contains_dirty_char(title, content):
        return "存在脏词"
    if contain_chemical_equation(content):
        return "存在化学符号"
    if contain_dirty_novel(content):
        return "存在脏小说"
    if contains_yanwenzi(content):
        return "存在颜文字"
    if contains_repeat_char(content):
        return "存在重复字符"
    if contains_emoji(content):
        return "存在emoji表情"
    if contain_dirty_person(title, content):
        return "存在无名人物"
    if contains_sim_sent(content):
        return "存在相似段落"
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
    tool = NerTool()
    res = tool.get_ner_zh(title)
    if len(res) > 1 and res[1] \
            and res[1][0] \
            and res[1][0][0] \
            and res[1][0][0][2] \
            and (
            res[1][0][0][2] == "person" or res[1][0][0][2] == "company" or res[1][0][0][2] =="org"):
        # 识别为名字则判断简介是否小于阈值
        if len(content) < 600:
            return True
    else:
        # 不是中文人名, 使用英文实体检测是否为英文人名
        res = tool.get_ner_en(title)
        if len(res) > 0 and res[0] and res[0][1] \
                and (res[0][1] == "PERSON" or res[0][1] == "COMPANY"):
            # 识别为名字则判断简介是否小于阈值
            if len(content) < 600:
                return True
    return False


@get_time
def contains_sim_sent(content):
    '''
    判断是否存在在相同的句子
    '''
    simtool = SimhashTool()
    # 获取一段文本中相似的的句子
    list = simtool.get_sim_sent(content)
    if len(list) > 1:
        return True
    return False


@get_time
def contain_dirty_novel(content):
    '''
    部分数据切分时，把小说内容切分开一半
    '''
    sub_content = content[:50]
    if re.search('第.*?章', sub_content):
        return True
    return False


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
def contains_dirty_char(title, content):
    if title == "基本资料" or title == "注":
        return True
    if title == "真．三国无双7 Blast" or title == "例如":
        return True
    if title.startswith("电视动画版") or title.startswith("注："):
        return True
    if '其他名称' in content:
        return True
    if '今年' in content:
        return True
    dirty_found = dirty_char_processor.extract_keywords(content)
    if len(dirty_found) > 0:
        return True
    return False


@get_time
def contains_yanwenzi(content):
    result = ywz.detect(content)
    if len(result) > 0:
        return True
    return False


@get_time
def contains_repeat_char(content):
    """检查某句话中是否有过多的某字符（多出现于wiki的表格中）"""
    for space in ["-", "\t", "/", "_", "！", "~", "－"]:
        # num_space = content.count(space)
        num_space = check_str_count(content, space)
        if num_space > 7 or (num_space > 2 and num_space > len(content) // 10):
            return True
    return False


@get_time
def contains_emoji(text):
    emoji_list = emoji.emoji_list(text)
    if len(emoji_list) > 0:
        return True
    return False
############################脏词判断##############
