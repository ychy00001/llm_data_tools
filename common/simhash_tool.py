from simhash import Simhash, SimhashIndex
from multiprocessing import Pool
import re
import time
import os
from common.utils import cut_sent, truncate_content, word_count
from common.log import logger


class SimhashTool:

    def __init__(self, hash_k=10, hash_f=128, width=4, max_hash_len=80, n_jobs=2):
        # 初始化hash索引  k=海明距离 越大表示相似内容判断的误差越大，就是将更大不太相似的判断为相似
        self.hash_k = hash_k
        self.hash_f = hash_f
        self.width = width
        self.max_hash_len = max_hash_len
        # 多协程控制
        self.n_jobs = n_jobs

    def __split_list(self, list, n):
        length = len(list)
        return [list[i * length // n: (i + 1) * length // n] for i in range(n)]

    def __get_features(self, s):
        '''
        根据宽度特征抽取
        print(get_features("我在家里写作业"))
        ['我在家里写作', '在家里写作业']
        '''
        s = s.lower()
        s = re.sub(r'[^\w]+', '', s)
        return [s[i:i + self.width] for i in range(max(len(s) - self.width + 1, 1))]

    def find_match(self, args):
        i, index = args
        value_dict = {}
        for item in i:
            flag = 1
            try:
                now_list = index.get_near_dups(item[1])
                for x in now_list:
                    if int(x) >= int(item[0]):
                        continue
                    flag = 0
                    break
                value_dict[item[0]] = flag
            except:
                value_dict[item[0]] = flag
        return value_dict

    def get_mem_hash(self, sent_list: list):
        # 获取内容hash值
        hashes = []
        members = []
        for idx, i in enumerate(sent_list):
            # 超过256个句子的数据不进行匹配
            if idx > 256:
                break
            try:
                # 截取最多前100提高效率 中英文区分
                member = truncate_content(i, self.max_hash_len)
                hashes.append((str(idx), Simhash(self.__get_features(member), f=self.hash_f)))
                members.append(member)
            except:
                continue
        # logger.debug(f" hashes:{hashes}")
        # logger.debug(f" members:{members}")
        # 初始化hash索引  k=海明距离 越大表示相似内容判断的误差越大，就是将更大不太相似的判断为相似
        index = SimhashIndex(hashes, f=self.hash_f, k=self.hash_k)
        # logger.debug("Finish building index!")
        # 数据分片
        n_hashes = self.__split_list(hashes, self.n_jobs)

        # 多线程执行
        # with Pool(self.n_jobs) as p:
        #     temp_dict = p.map(self.find_match, [(i, index) for i in n_hashes])
        # 单线程执行
        temp_dict = []
        for i in n_hashes:
            temp_dict.append(self.find_match((i, index)))

        value_dict = {}
        for dict in temp_dict:
            for i in dict:
                value_dict[i] = dict[i]
        # logger.debug("Finish finding matches!")
        # logger.debug(f"result: {value_dict}")
        mem_hashes = list(zip(members, hashes))
        return value_dict, mem_hashes

    def get_sim_sent(self, content):
        '''
        获取一大段内容中相似的句子或者段落
        '''
        sent_list = cut_sent(content)
        reformat_list = []
        # 避免频繁的小数据造成hash桶太大
        for i in sent_list:
            w_count = word_count(i)
            if w_count > 5:
                reformat_list.append(i)
        value_dict, mem_hashes = self.get_mem_hash(reformat_list)
        # 查看相似文本
        result = []
        for mem, a_hash in mem_hashes:
            if value_dict[a_hash[0]] != 1:
                result.append(mem)
        return result


if __name__ == '__main__':
    simtool = SimhashTool()
    # list = simtool.get_sim_sent("如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号")
    # text = "回环句是一种修辞方法。在修辞中，联珠句又叫顶针（顶真）句，它的结构形式是：上一句话收尾的词语是下一句话的开头，用符号表示就是“ABC,CDE,EFG……”。在具备上述条件的基础上，如果上一句的开头成为下一句话的收尾，则构成了回环句，用符号来表示就是“ABC,CDE,EFA”。为了训练方便，在作文文采训练中，我们笼统地把这两类句子都归入联珠句中。句子示例\n顶针句：\n关键时刻需要果断，果断抉择来自于智慧，智慧来自于学习和实践的积累。（关于“果断”的话题）\n盛年歌盛世，盛世逢盛会，盛会振奋人心。（关于“十六大”的话题）\n当今社会的竞争是国力的竞争；国力竞争的根本是科技的竞争；科技竞争背后是人才的竞争；人才竞争的后面则是教育的竞争，所以，教育是兴国的根本。（关于“教育”的话题）\n回环句：\n民族文化的进步需要文化的宽容，文化的宽容需要宽容的思想，宽容的思想能促进民族文化的发展。（关于“宽容”的话题）\n经济决定金融，金融服务于经济。（关于“经济与金融”的话题）\n"
    text = "中国大地构造学纲要，本书以地质构造演化历史为主要线索，以构造事件为单位，系统地、定量化地阐述了中国大地构造的主要宏观特征，把构造变形、变位的机制分析与历史分析紧密结合起来，把构造活动的稳定时期与活跃时期的演化结合起来进行研究；大力加强了中生代一新生代大地构造的探讨，尽量客观地反映近30年来国内外学者对中国大地构造学所做的贡献；系统介绍了具有特色的大地构造学研究方法，探讨了一些重要的大地构造学理论问题，如碰撞带和各类板内变形的特征与形成机制，中国大陆地壳与岩石圈厚度变化及其原因，地温梯度的变化与地幔羽的存在问题，构造作用对我国内、外生矿床形成的影响及找矿前景，最后对全球板块构造动力学机制假说提出了一些看法。内容简介\n本书后半部附有大量的构造变形、变位的原始数据和有关的参考文献，以备查考。本书是一本供研究生使用的教学参考书，也适合于从事构造地质、区域地质、矿产普查与勘探、地震地质、环境地质和灾害地质等方面的科研、教学与野外地质工作人员使用。本书目录\n序\n前言\n绪论\n第一章大地构造学的研究内容与方法\n一、构造事件研究\n二、构造变形、构造体系与构造应力方向的确定\n三、构造应力值的估算\n四、板块变形速度与变形量的估算——运动学研究之一\n五、古地磁学与古构造复原——运动学研究之二\n第二章太古宙和古元古代（1800 Ma以前）构造演化\n一、始太古代（4500～3600 Ma）的构造演化——星子聚集、吸积作用和形成古陆核\n二、古太古代一新太古代（3600～2500 Ma PA—NA）的构造演化——古陆块形成和陆壳克拉通化\n三、古元古代（吕梁期，2500～1800 Ma，PP）的构造演化——原始中朝板块裂陷和拼合，形成统一的结晶基底\n四、关于太古宙和古元古代陆壳厚度的讨论\n第三章中、新元古代（1800～513 Ma）构造演化\n一、中元古代（长城纪一蓟县纪，1800～1000 Ma）构造演化——原始中朝板块裂陷和形成沉积盖层，扬子板块完成拼合\n二、青白口纪（拉伸纪，looo～800 Ma）构造演化——各陆块普遍会聚或碰撞，扬子板块形成统一结晶基底\n三、南华纪（成冰纪，800～680 Ma）构造演化——各陆块普遍张裂，扬子一塔里木板块发育南沱组冰积层\n四、震旦纪一早寒武世（680～513 Ma）构造演化——中朝板块南缘发育罗圈组冰积层，泛非构造事件的广泛影响\n五、中国各地块在全球中、新元古代演化中的表现\n第四章中寒武世一早泥盆世（祁连期，513—386 Ma）构造演化——西域板块完成拼合、阿尔泰一额尔古纳碰撞带形成、华夏板块构成统一结晶基底、南扬子板内褶皱、多数地块呈离散状态\n一、沉积古地理与古生物分布\n二、古地磁研究与古构造复原\n三、构造活跃期的变形、变质作用与应力场特征\n四、岩浆活动与板块变位速度\n五、早古生代构造单元的划分\n第五章 中泥盆世一早二叠世（天山期，386—257 Ma）构造演化——天山一兴安碰撞带形成，发育峨眉山地幔羽\n一、沉积古地理与古生物分布\n二、古地磁研究与古构造复原\n三、构造活跃期的变形、变质作用与应力场特征\n四、岩浆活动与板块变位速度\n五、中元古代一古生代构造演化与板块的运移\n第六章晚二叠世一三叠纪（印支期，257—205 Ma）构造演化——澜沧江、金沙江、秦岭一大别和绍兴一十万大山等碰撞带形成，板内盖层广泛褶皱，印支构造体系形成\n一、沉积与生物古地理\n二、碰撞带构造\n三、板内构造变形\n第七章侏罗纪一早白垩世早期（燕山期，205—135 Ma）构造演化——新华夏构造体系形成，伊佐奈岐板块向西俯冲、挤压，中国大陆逆时针转动，壳内低速层滑脱，强烈的构造岩浆活动\n一、板内构造变形与应力场\n二、中国大陆板块与周边板块的运移和转动\n三、岩浆活动与壳内低速层及莫霍面的滑脱\n第八章早白垩世中期一古新世（四川期，135—52 Ma）构造演化——四川构造体系形成，东部盆岭构造发育，主应力方向的顺时针转变，班公错一怒江碰撞带形成，全球板块普遍北移\n一、板内构造变形与应力场\n二、岩浆活动及其相关的构造\n三、班公错一怒江碰撞带形成，全球板块普遍向北运移\n第九章始新世一渐新世（华北期，52—23．5 Ma）构造演化——华北构造体系形成，四大汇水盆地出现，太平洋板块首次向西俯冲、挤压，雅鲁藏布江碰撞带形成\n一、板内构造变形与应力场\n二、东部盆地的发育与油气资源的聚集\n三、西太平洋俯冲带和雅鲁藏布江碰撞带的形成\n第十章新近纪一早更新世（喜马拉雅期，23．5—0．78 Ma）构造演化\n一、喜马拉雅逆掩断层带、青藏薄皮构造和青藏高原形成\n二、东部板内变形、张裂与离散\n三、地形大台阶与大陆边缘伸展盆地的形成\n第十一章中更新世一全新世（新构造期，O．78 Ma以来）构造演化\n一、板内变形与现代构造应力场\n……\n第十二章中国大陆构造变形特征与问题的讨论\n第十三章中国大陆岩石圈构造与热状态\n第十四章中国大地构造与成矿作用\n第十五章关于全球板块构造动力学机制的讨论\n参考文献\n附录\n光盘中的图件目录\n"
    s_time = time.time() * 1000
    list = simtool.get_sim_sent(text)
    e_time = time.time() * 1000
    print('耗时：{}毫秒'.format(e_time - s_time))
    for i in list:
        print(i)

# if __name__ == '__main__':
#     # 获取内容hash值
#     hashes = []
#     members = []
#     with open("./simhash/test_data.txt", "r") as f:
#         lines = f.readlines()
#         for idx, i in enumerate(lines):
#             try:
#                 member = i
#                 if max_hash_len == 0:
#                     hashes.append((str(idx), Simhash(get_features(i))))
#                 else:
#                     hashes.append((str(idx), Simhash(get_features(i[:max_hash_len]))))
#                 members.append(member)
#             except:
#                 continue
#     print(f" hashes:{hashes}")
#     print(f" members:{members}")
#     # 初始化hash索引  k=海明距离 越大表示相似内容判断的误差越大，就是将更大不太相似的判断为相似
#     index = SimhashIndex(hashes, k=hash_k)
#     print("Finish building index!")
#
#     # 数据分片
#     n_hashes = split_list(hashes, n_jobs)
#
#     # 执行
#     with Pool(n_jobs) as p:
#         temp_dict = p.map(find_match, [(i, index) for i in n_hashes])
#     value_dict = {}
#     for dict in temp_dict:
#         for i in dict:
#             value_dict[i] = dict[i]
#     print("Finish finding matches!")
#     print(f"result: {value_dict}")
#
#     mem_hashes = list(zip(members, hashes))
#     # 查看相似文本
#     for mem, a_hash in mem_hashes:
#         if value_dict[a_hash[0]] != 1:
#             print(f"相似段落：{mem}")
