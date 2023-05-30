import re


def is_blank(it):
    if not it or (isinstance(it, str) and it.isspace()) or len(it) == 0:
        return True
    return False


def is_not_blank(it):
    return not is_blank(it)


if __name__ == '__main__':
    # "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:(.*)\\nHistory:(.*)\\n\\nUser:(.+)\\n\\nAssistant:"
    prompt = "If you are an artificial intelligence assistant. It is designed to be helpful, honest, and harmless. please answer the user questions based on the user asks and descriptions. \n\nUser:基于以下角色信息完成一段对话\nJohn: 一名40岁的企业家，拥有一家成功的IT公司。他是个工作狂，一直在为自己的事业奋斗。\nLucy: 一名30岁的社会工作者，十分关注社会公益事业，正在为一个非营利性组织工作。\n\n\nAssistant:"
    match_list = re.findall(
        r"If you are an artificial intelligence assistant. It is designed to be helpful, honest, and harmless. please answer the user questions based on the user asks and descriptions. \n\nUser:([\s\S]+)\n\nAssistant:",
        prompt)
    print(len(match_list))
    print(match_list[0])

    # '樱TrickStudio Deen改编的电视动画\n中文名\n樱Trick\n原版名称\n桜Trick\n别 名\nSakura Trick\n动画制作\nSTUDIO DEEN\n原作者\nタチ\n地 区\n日本\n发行公司\n波丽佳音\n角色设计\n坂井久太\n导 演\n石仓贤一\n集 数\n全12集\n主要配音\n户松遥、井口裕香、相坂优歌、五十岚裕美\n首播电视台\nTBS\n播放期间\n2014年1月9日－3月27日\n代理发行\n木棉花国际(中国台湾)\n \n基本信息\n樱Trick剧情简介 \n高山春香与园田优两位好友，一起升学至3年后即将面临合并废校的美里西高中的故事。\n樱Trick动画制作 \n樱Trick制作人员\n原作：タチ企画：村上仁之、福场一义、孝寿尚志、野口和纪、中村达司监督・系列构成：石仓贤一人物设计：坂井久太道具设计：小坂知美术监督：田山修色彩设计：わたなべひろし摄影监督：浜尾繁光编集：松原理恵音响监督：饭田里树音响制作：DAX Production音乐：中西亮辅音乐制作：波丽佳音制作人：田中润一朗、高取昌史、小林宏之、浦崎宣光、青木絵理子动画制作：Studio DEEN制作协力：波丽佳音、芳文社、Studio DEEN、Memory-Tech制作：TBS、樱Trick制作委员会\n樱Trick角色配音\n高山春香：户松遥园田优：井口裕香野田琴音：相坂优歌南雫：五十岚裕美池野枫：渕上舞饭冢柚：户田惠园田美月：藤田咲坂井理奈：远藤祐里香乙川澄：麻仓桃\n樱Trick剧集信息 \n樱Trick各话制作', '', '请问樱Trick这部动画是什么类型，讲述的是什么故事？'
    prompt = "If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:樱TrickStudio Deen改编的电视动画\n中文名\n樱Trick\n原版名称\n桜Trick\n别 名\nSakura Trick\n动画制作\nSTUDIO DEEN\n原作者\nタチ\n地 区\n日本\n发行公司\n波丽佳音\n角色设计\n坂井久太\n导 演\n石仓贤一\n集 数\n全12集\n主要配音\n户松遥、井口裕香、相坂优歌、五十岚裕美\n首播电视台\nTBS\n播放期间\n2014年1月9日－3月27日\n代理发行\n木棉花国际(中国台湾)\n \n基本信息\n樱Trick剧情简介 \n高山春香与园田优两位好友，一起升学至3年后即将面临合并废校的美里西高中的故事。\n樱Trick动画制作 \n樱Trick制作人员\n原作：タチ企画：村上仁之、福场一义、孝寿尚志、野口和纪、中村达司监督・系列构成：石仓贤一人物设计：坂井久太道具设计：小坂知美术监督：田山修色彩设计：わたなべひろし摄影监督：浜尾繁光编集：松原理恵音响监督：饭田里树音响制作：DAX Production音乐：中西亮辅音乐制作：波丽佳音制作人：田中润一朗、高取昌史、小林宏之、浦崎宣光、青木絵理子动画制作：Studio DEEN制作协力：波丽佳音、芳文社、Studio DEEN、Memory-Tech制作：TBS、樱Trick制作委员会\n樱Trick角色配音\n高山春香：户松遥园田优：井口裕香野田琴音：相坂优歌南雫：五十岚裕美池野枫：渕上舞饭冢柚：户田惠园田美月：藤田咲坂井理奈：远藤祐里香乙川澄：麻仓桃\n樱Trick剧集信息 \n樱Trick各话制作\nHistory:\n\nUser:请问樱Trick这部动画是什么类型，讲述的是什么故事？\n\nAssistant:"
    match_list = re.findall(
        r"If you are a artificial intelligence assistant, please answer the user questions based on the user asks and descriptions.Context:([\s\S]*)\nHistory:([\s\S]*)\n\nUser:(.+)\n\nAssistant:",
        prompt)
    print(len(match_list))
    print(match_list)
    print(type(match_list[0]))
