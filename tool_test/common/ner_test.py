import fool
import sys

sys.path.append("../..")
from common.ner_tool import NerTool

# text = "张三和李四在2019年3月23日在北京的腾讯技术有限公司一起开会。"
text = "陶华兰"
text1 = ""
text2 = "Varela M"
if __name__ == '__main__':
    # res = fool.analysis(text)
    # if res[1][0][0][2] == "person":
    #     print("是中文人名")
    # else:
    #     print("不是中文人名")
    res1 = fool.analysis("甘良均")
    print("\n")
    print(res1)
    if res1[1] and res1[1][0] and res1[1][0][0] and res1[1][0][0][2] and res1[1][0][0][2] == "person":
        print("是中文人名")
    else:
        print("不是中文人名")
    # res2 = fool.analysis(text2)
    # print("\n")
    # print(res2[0])
    # print(res2[1][0])

    res3 = fool.analysis("广州橙悦健身有限公司")
    print(res3)
    if res3[1] and res3[1][0] and res3[1][0][0] and res3[1][0][0][2] and res3[1][0][0][2] == "company":
        print("是中文公司")
    else:
        print("不是中文公司")
    # tool = NerTool()
    #
    # res = tool.get_ner(text)
    # print("\n")
    # print(res)
    # if res and res[0] and res[0][1] and res[0][1] == "PERSON":
    #     print(f"{text} 是英文人名")
    # else:
    #     print(f"{text} 不是英文人名")
    # res1 = tool.get_ner(text1)
    # print("\n")
    # print(res1)
    # if len(res1) > 0 and res1[0] and res1[0][1] and res1[0][1] == "PERSON":
    #     print(f"{text1} 是英文人名")
    # else:
    #     print(f"{text1} 不是英文人名")
    # res2 = tool.get_ner(text2)
    # print("\n")
    # print(res2)
    # if res2 and res2[0] and res2[0][1] and res2[0][1] == "PERSON":
    #     print(f"{text2} 是英文人名")
    # else:
    #     print(f"{text2} 不是英文人名")
    #


