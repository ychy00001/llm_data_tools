import sys
sys.path.append("../..")
from common.utils import cut_sent
import re

if __name__ == '__main__':
    sent = cut_sent("如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号")
    print(sent)
    content = "乙基叠氮乙酸酯是一种化学物质，化学式是C4H7N3O2。InChI编码\n1S/C4H7N3O2/c1-2-9-4(8)3-6-7-5/h2-3H2,1H3\n其他名称\nACETICACID,AZIDO-,ETHYLESTER(7CI,8CI,9CI);\n(ETHOXYCARBONYL)METHYLAZIDE;\n2-AZIDOACETATEETHYLESTER;\nAZIDOACETICACIDETHYLESTER;\nETHYL2-AZIDOACETATE;\nETHYLAZIDOACETATE;\nETHYLA-AZIDOACETATE;\nNSC84132;\n"
    content = "化学式是C4H7N3O2。InChI编码\n1S/C4H7N3O2/c1-2-9-4(8)3-6-7-5/h2-3H2,1H3\n其他名称\nACETICACID,AZIDO-,ETHYLESTER(7CI,8CI,9CI);\n(ETHOXYCARBONYL)METHYLAZIDE;\n2-AZIDOACETATEETHYLESTER;\nAZIDOACETICACIDETHYLESTER;\nETHYL2-AZIDOACETATE;\nETHYLAZIDOACETATE;\nETHYLA-AZIDOACETATE;\nNSC84132;\n"
    sub_content = content[:100]
    if "是一种化学物质" in sub_content:
        print("存在")
    else:
        print("不存在")

    content = "第283啊"
    if re.search('第.*?章', content):
        print("已章节开头")
    else:
        print("不已章节开头")
