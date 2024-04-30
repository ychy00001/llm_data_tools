import sys

sys.path.append("../..")
from common.utils import cut_sent
from common.filter import contain_err_num, contains_emoji, is_dirty_book, is_dirty_web
import re

if __name__ == '__main__':
    # test = "1910年秋季，考入湖南湘乡县立东山高等小学堂读书。此期间受康有为、梁启超改良主义思想的影响。 [21]1911-1920年1911年春季，到长沙，考入湘乡驻省中学读书。期间，读到同盟会办的《民立报》，受其影响，撰文表示拥护孙中山及同盟会的纲领。10月，响应辛亥革命，投笔从戎，在湖南新军当列兵。半年后退出。 [2]1913年春季，入湖南省立第四师范学校预科读书。1914年秋季，编入湖南省立第一师范学校本科第八班。在校期间，受杨昌济等进步教师的影响，成为《新青年》杂志的热心读者，崇拜陈独秀、胡适。1918年4月14日，同萧子升、何叔衡、蔡和森等发起成立新民学会。6月，在湖南省立第一师范学校毕业。8月，为组织湖南赴法勤工俭学运动第一次到北京。在北京期间，担任北京大学图书馆管理员，得到李大钊等人帮助，开始接受俄国十月革命的思想影响。1919年4月6日，从上海回到长沙。5月，响应五四运动，发起成立湖南学生联合会，领导湖南学生反帝爱国运动。7月14日，主编的湖南学生联合会会刊《湘江评论》在长沙创刊。7月至8月，连续撰写并发表《民众的大联合》长文。10月5日，母亲文氏病逝，闻讯从长沙赶回韶山。8日，在母亲灵前写成《祭母文》。12月，为领导驱逐湖南军阀张敬尧的运动，第二次到北京。在京期间，读到《共产党宣言》等马克思主义书籍。1920年5、6月间，在上海会见陈独秀，同他讨论读过的马克思主义书籍等问题。8月初，同易礼容等在长沙发起成立文化书社，传播马克思主义和新文化。8月至9月，参加筹备成立俄罗斯研究会。11月25日，致信罗章龙，提出新民学会，“要变为主义的结合才好。主义譬如一面旗子，旗子立起了，大家才有所指望，才知所趋赴”。11月，同何叔衡等组织长沙共产主义小组。12月1日，致信给蔡和森、萧子升和其他在法国勤工俭学的会友 [29] 。信中表明自己接受马克思主义，走俄国十月革命的道路。在长沙筹建社会主义青年团。同杨开慧结婚。 [21]1921-1930年1921年1月1日至3日，同何叔衡、彭璜、周世钊、熊瑾玎等十余人在长沙潮宗街文化书社召开新民学会会员新年大会。在会上提出新民学会应以“改造中国与世界”为共同目的，赞成用“俄式”方法改造中国。7月23日至8月初，同何叔衡作为长沙共产主义小组的代表出席在上海召开的中国共产党第一次全国代表大会。8月，回长沙，任中国劳动组合书记部湖南分部主任。与何叔衡创办湖南自修大学。10月10日，建立中共湖南支部，任书记。1922年5月，中共湘区执行委员会成立，任书记。9月至12月，组织领导粤汉铁路工人、安源路矿工人、长沙泥木工人等一系列罢工运动，推动湖南工人运动迅速走向高潮。1923年4月，离开长沙到达上海，在中共中央工作。6月，在广州出席中国共产党第三次全国代表大会，被选为中央执行委员、中央局委员、并担任中央局秘书。9月16日，遵照中共中央的决定并受国民党本部总务部副部长林伯渠的委托，回到长沙，筹建湖南国民党组织。1924年1月，在广州出席中国国民党第一次全国代表大会，被选为候补中央执行委员。2月，到上海，任国民党上海执行部委员、组织部秘书等职。12月，回湖南养病。1925年2月，回到韶山，一面养病，一面开展农民运动。9月，到广州，参加国民党第二次全国代表大会筹备工作。10月，任国民党中央宣传部代理部长。12月1日，发表《中国社会各阶级的分析》一文。12月5日，主编的国民党中央宣传部刊物《政治周报》创刊。 [21]1926年1月，出席中国国民党第二次全国代表大会，继续当选候补中央执行委员。3月18日，在广州国民党政治讲习班纪念巴黎公社五十五周年集会上发表讲演，题为《纪念巴黎公社的重要意义》。3月，蒋介石在广州制造中山舰事件，同周恩来等力主反击。5月至9月，主办国民党第六届农民运动讲习所，任所长。11月，到上海任中共中央农民运动委员会书记。不久到武汉，创办国民党中央农民运动讲习所。12月，在长沙出席湖南全省第一次工人代表大会和第一次农民代表大会。 [3]1927年1月4日至2月5日，在湖南考察湘潭、湘乡、衡山、醴陵、长沙五县农民运动。3月，发表《湖南农民运动考察报告》；在武汉出席国民党二届三中全会。4月12日，蒋介石在上海发动反革命政变。4月27日至5月10日，出席中国共产党第五次全国代表大会，被选为候补中央执行委员。会议批评了陈独秀的右倾错误。7月15日，汪精卫在武汉发动反革命政变，宁汉合流，大革命失败。8月1日，南昌起义爆发。同宋庆龄等二十二名国民党中央委员联名发表《中央委员宣言》，谴责蒋介石、汪精卫背叛国民革命。8月7日，出席中共中央在汉口召开的紧急会议，提出枪杆子里面出政权的思想，被选为临时中央政治局候补委员。会后到湖南领导湘赣边界秋收起义。9月9日，湘赣边界秋收起义爆发。在去江西铜鼓萧家祠第三团团部途经浏阳张家坊时，被团防局的清乡队抓住，押送途中机智脱险。9月，秋收起义受挫后，率起义部队向罗霄山脉中段进军。10月，到达江西宁冈县茅坪，开始创建井冈山革命根据地。11月，遭到中共临时中央政治局错误指责，被撤销政治局候补委员职务。1928年4月，率部在江西宁冈县砻市同朱德、陈毅率领的南昌起义军余部和湘南起义农军会师。5月，担任两支部队合编成的工农革命军（后改称中国红军）第四军党代表、军委书记。7月，在中国共产党第六次全国代表大会上被选为中央委员。10月，为中共湘赣边界第二次代表大会起草决议案，提出“工农武装割据”的思想。11月25日，代表中共红四军前委给中央写报告，总结井冈山工农武装割据的经验。12月，主持制定井冈山《土地法》。1929年1月，同朱德、陈毅率红四军主力向赣南、闽西进军，至1930年春赣南、闽西两块革命根据地初步形成。4月，主持制定兴国《土地法》。6月，出席在龙岩召开的中共红四军第七次代表大会，关于红军的任务、政治工作和军事工作等问题的正确意见未被接受，原由中共中央指定他担任的前委书记职务被改选他人担任。会后，离开红四军主要领导岗位，到闽西休养并指导地方工作。7月，指导召开中共闽西第一次代表大会。9月，中共中央给红四军前委发出指示信，肯定了毛泽东关于红军的行动策略和建设一支坚强的人民革命军队的正确主张。12月，在福建上杭县古田村主持召开中共红四军第九次代表大会，在会上作政治报告，并起草大会决议案（即古田会议决议）。大会重新选举毛泽东担任前委书记。 [30]1930年1月，写《星星之火，可以燎原》一文，阐述关于农村包围城市、武装夺取政权的中国革命道路的理论。5月，在江西寻乌作调查；同时撰写《反对本本主义》一文，提出“没有调查，没有发言权”。8月，任红一方面军总政治委员和中共总前敌委员会书记。9月，在中共六届三中全会上被选为政治局候补委员。12月30日至次年1月3日，同朱德等指挥红一方面军粉碎国民党军第一次“围剿”。1931-1940年1931年1月7日，中共扩大的六届四中全会在上海举行，被选为中共中央政治局候补委员（未出席会议）。王明在共产国际代表扶持下进入中央政治局。4月至5月，同朱德等指挥红一方面军粉碎国民党军第二次“围剿”。7月至9月，粉碎国民党军第三次“围剿”。11月1日至5日，在中央苏区党组织召开的第一次代表大会（赣南会议）上受到排挤，被指责为“狭隘的经验论”、“富农路线”和“极严重的一贯右倾机会主义”。11月，在中华苏维埃第一次全国代表大会上作报告；在中华苏维埃共和国中央执行委员会第一次会议上当选为主席和人民委员会主席。 [22]1932年1月，到江西瑞金城郊东华山古庙休养。3月，红军攻打赣州失利后，停止休养，赶赴前线指挥。4月15日，发表《对日战争宣言》。5月9日，同项英发布《中华苏维埃共和国临时中央政府反对国民党出卖淞沪协定通电》。6月，同朱德指挥红一、红五军团从闽西回师赣南。10月，在江西宁都召开的中共苏区中央局会议上，受到“左”倾错误领导的打击。会后，被撤销红一方面军总政治委员职务，前往福建长汀养病。 [4]1933年1月下旬，中共临时中央政治局迁到中央革命根据地。2月上旬，中共临时中央全面推行 “进攻路线”，清除毛泽东积极防御路线在中央根据地的影响，开展了所谓反“罗明路线”的斗争。5月30日，同项英等发布中华苏维埃共和国临时中央政府《为国民党出卖平津宣言》。6月1日，同项英等发布中华苏维埃共和国临时中央政府《关于查田运动的训令》。8月，在瑞金召开的中央苏区南部十七县经济建设大会上作《粉碎五次“围剿”与苏维埃经济建设任务》的报告。10月，写《怎样分析农村阶级》一文，成为划分农村阶级成分的标准。11月，先后在兴国县长冈乡和上杭县才溪乡调查，写出《长冈乡调查》和《才溪乡调查》。1934年1月，在中共六届五中全会上被选为政治局委员。在中华苏维埃第二次全国代表大会上作工作报告。继续当选为中华苏维埃共和国中央执行委员会主席。6月19日，同项英等发表《中华苏维埃共和国中央政府为国民党出卖华北宣言》。7月15日，同项英等发表《为中国工农红军北上抗日宣言》。10月18日，傍晚，带领警卫班离开于都城，踏上长征的路途。11月底，湘江之战中红军遭受惨重损失。30日，随军委第一野战纵队渡过湘江。12月12日，在湖南通道召开的中共中央负责人紧急会议上，力主红军放弃原定向湘西与红二、六军团会合的计划，改向敌人力量薄弱的贵州前进，被采纳。1935年1月15日至17日，出席在贵州遵义召开的中共中央政治局扩大会议，被增选为中央政治局常委。会议结束了王明“左”倾冒险主义在中共中央的统治，实际确立了以毛泽东为代表的新的中央领导。3月，同周恩来、王稼祥组成三人军事指挥小组。3月至5月，同周恩来等指挥红一方面军四渡赤水，巧渡金沙江，飞夺泸定桥，取得战略转移中具有决定意义的胜利。6月15日，同项英等发表《为反对日本并吞华北和蒋介石卖国宣言》。6月，率红一方面军同红四方面军在四川西部会合。不久，即同张国焘的逃跑主义、分裂主义进行斗争。10月19日，率领中国工农红军陕甘支队到达陕西延安吴起镇。红军胜利完成长征。12月，出席在陕北瓦窑堡召开的中共中央政治局会议。会议确定了建立抗日民族统一战线的策略。12月27日，在党的活动分子会议上作《论反对日本帝国主义的策略》报告，阐发抗日民族统一战线的策略方针。1936年1月25日，同周恩来、彭德怀等二十位红军将领联名发出《为红军愿意同东北军联合抗日致东北军全体将士书》，提出关于组织国防政府和抗日联军的具体办法，建议互派代表共同协商。2月至5月，同彭德怀率领红一方面军主力渡黄河东征。3月，向南京当局提出停止内战、一致抗日的五点意见。6月1日，同朱德发布关于救国救民的主张二十条。6月12日，同朱德发布宣言，对“两广事变”表示支持，提出抗日救国的八项纲领。7月至10月，在陕北延安多次会见美国记者斯诺，回答他提出的有关中国革命和工农红军等多方面的问题，并介绍了自己的经历。8月10日，出席中共中央政治局会议，作关于国共两党关系和统一战线问题的报告。8月25日，起草《中国共产党致中国国民党书》，呼吁一致抗日。12月7日，任中共中央革命军事委员会主席。12月12日 [31] ，张学良、杨虎城在西安实行“兵谏”，扣留蒋介石。毛泽东和中共中央分析当时错综复杂的政治形势，确定了和平解决西安事变的方针，并派周恩来等往西安参加谈判，促成事变和平解决。12月，撰写《中国革命战争的战略问题》。 [4]1937年1月13日，同中共中央和中央军委进驻延安。2月9日，出席中共中央政治局常委会议，会议讨论和通过《中共中央给中国国民党三中全会电》，提出五项国策、四项保证。这个文件实际成为国共合作谈判的纲领。3月，会见美国记者史沫特莱，回答她对中日战争与西安事变提出的一些问题。4月至7月，在抗日军政大学讲授辩证法唯物论，其中的两节后来整理成《实践论》和《矛盾论》。5月，在中国共产党全国代表会议上作《中国共产党在抗日时期的任务》的报告和《为争取千百万群众进入抗日民族统一战线而斗争》的结论。7月7日，卢沟桥事变爆发，全国抗日战争开始。7月23日，发表《反对日本进攻的方针、办法和前途》，提出坚决抗战，反对妥协退让的方针、政策。8月22日至25日，出席在陕北洛川召开的中共中央政治局扩大会议，强调统一战线中的独立自主原则，阐明独立自主山地游击战的战略方针，任新组成的中共中央军事委员会书记。8月25日，同朱德、周恩来联名发布关于红军改编为国民革命军第八路军的命令。随后，指导八路军开赴抗日前线。11月12日，在延安党的活动分子会议上作《上海太原失陷以后抗日战争的形势和任务》的报告，全面阐述了对统一战线和国共关系的意见。12月，出席中共中央政治局会议并发言，针对王明“一切经过统一战线”的右倾投降主义主张，重申和坚持了洛川会议确定的方针政策。 [5]1938年春季，作出八路军从华北山地进入到平原地区开展游击战争的决策。5月，发表《抗日游击战争的战略问题》一文。5月26日至6月3日，在延安抗日战争研究会作《论持久战》讲演。全面分析中日战争所处的时代和中日双方的基本特点，批驳速胜论和亡国论，阐述了中国抗日战争的持久战的总方针。9月14日至27日，出席中共中央政治局会议。王稼祥传达共产国际指示，说中共中央领导机关要以毛泽东为首解决统一领导问题。毛泽东在会上作长篇发言。9月29日至11月6日，出席中共扩大的六届六中全会，作《论新阶段》的政治报告和会议结论。会议批准以毛泽东为首的中央政治局的路线。1939年2月2日，在延安党政军生产动员大会上讲话，号召自己动手，克服经济困难。2月5日，在中共中央党校作《反对投降主义》的讲话。4月下旬，写《五四运动》一文。5月4日，在延安青年纪念五四运动二十周年大会上作《青年运动的方向》的讲演。7月至8月，多次作报告，谴责国民党顽固派制造反共磨擦，呼吁继续团结抗战。9月16日，同中央社、《扫荡报》、《新民报》三记者谈话，重申对国民党顽固派制造反共磨擦采取“人不犯我，我不犯人；人若犯我，我必犯人”的自卫原则。10月4日，发表《〈共产党人〉发刊词》，阐明统一战线、武装斗争、党的建设是中国革命克敌制胜的三大法宝。12月1日，为中共中央起草关于大量吸收知识分子的决定。12月21日，为八路军政治部、卫生部编印的《诺尔曼·白求恩纪念册》写《纪念白求恩》一文。同月，与人合作撰写《中国革命和中国共产党》。12月至次年3月，领导打退国民党顽固派第一次反共高潮。1940年1月，发表《新民主主义论》，系统论述新民主主义革命的理论和纲领。3月6日，为中共中央起草关于抗日根据地政权问题的指示，提出实行“三三制”。3月11日，作《目前抗日统一战线中的策略问题》的报告，总结打退第一次反共高潮的经验，提出“发展进步势力，争取中间势力，反对顽固势力”的策略思想和有理、有利、有节的原则。5月4日，起草中共中央致东南局和新四军的指示，强调必须放手扩大军队，抵抗反共顽固派的进攻，指出要采取斗争的方针，“应付可能的全国性的突然事变”。6月下旬，在中共中央政治局会议上作报告，分析国际形势及对中国抗战的影响，指出：既要警惕国民党顽固派发动突然事变，又要力争时局好转。11月，起草朱德、彭德怀、叶挺、项英复电何应钦、白崇禧《皓电》的电报（《佳电》），明确驳斥《皓电》对八路军、新四军的无理指责。12月，同从前线回来到中央党校学习的同志谈话，强调干部精通马克思列宁主义的重要性。 [5]1941-1950年1941年1月上旬，皖南事变发生。1月20日，为中共中央军委起草重建新四军军部的命令，并对新华社记者发表关于皖南事变的谈话，严正提出解决皖南事变的十二条办法。5月1日，审阅改写的经中共中央政治局批准的《陕甘宁边区施政纲领》发布，规定边区政权建设贯彻“三三制”原则。5月8日，起草《关于打退第二次反共高潮的总结》的党内指示，提出“以打对打，以拉对拉”和争取中间派的策略思想。5月19日，在延安干部会上作《改造我们的学习》的报告，提出反对主观主义，阐明实事求是的思想原则。8月1日，为中共中央起草《关于调查研究的决定》。9月10日至10月22日，出席中共中央政治局扩大会议，作反对主观主义和宗派主义的报告。9月26日，中共中央作出《关于高级学习组的决定》，成立以毛泽东为组长的中央学习组。秋冬，先后主持编辑《六大以来》、《六大以前》和《两条路线》等党的历史文献集。 [6]1942年2月1日，在中共中央党校开学典礼上作《整顿党的作风》的报告。2月8日，在中共中央宣传部召集的干部会议上作《反对党八股》的讲话。5月，在延安文艺工作者座谈会上发表讲话并作结论。9月7日，为延安《解放日报》撰写社论，论述精兵简政是一个极其重要的政策。12月，向中共中央西北局高干会议提交《经济问题与财政问题》长篇书面报告，论述“发展经济，保障供给”的财经工作总方针。1943年3月20日，在中共中央政治局会议上被推定为中央政治局主席和中央书记处主席。5月26日，在中共中央书记处召开的干部大会上作《关于共产国际解散问题的报告》。6月1日，为中共中央起草关于领导方法的决定。7月1日，致信康生，指出“防奸”工作应调查研究，分清是非，教育群众，反对“逼，供，信”。7月12日，为延安《解放日报》撰写《质问国民党》的社论，揭露国民党顽固派企图进攻陕甘宁边区的阴谋。9月上旬至10月上旬，主持中共中央政治局在这一期间召开的会议，批评王明在十年内战时期的“左”倾冒险主义错误和抗战初期的右倾机会主义错误，在会上多次发言并作小结。12月，为中央党校大礼堂落成题词“实事求是”。1944年4月12日和5月20日，先后在中共中央西北局高干会议和中央党校第一部作关于学习和时局的讲演。5月15日，通过在西安同国民党代表谈判的林伯渠，提出由他起草的作为谈判具体内容的意见书。意见书就关于全国政治和两党悬案问题，提出二十条意见。5月21日，在中共扩大的六届七中全会上被推举为中央委员会主席和七中全会主席团主席。6月5日，起草的《中共中央关于城市工作的指示》在中共六届七中全会讨论通过。6月至8月，多次会见中外记者西北参观团成员和驻延安美军观察组成员，阐述中国共产党的抗日政策和国共关系等问题。9月8日，在张思德追悼会上发表《为人民服务》的演讲。10月31日，主持中共六届七中全会主席团会议，决定派王震、王首道率部南下，“以衡山为中心建立根据地”。11月，和周恩来等同美国总统罗斯福的私人代表赫尔利多次会谈国共关系，并达成五条协定草案。这个协定草案被蒋介石拒绝。1945年4月20日，出席中共六届七中全会最后一次会议，会议基本通过经毛泽东多次作重要修改的《关于若干历史问题的决议》。4月23日至6月11日，主持召开中国共产党第七次全国代表大会，致开幕词（《两个中国之命运》）和闭幕词（《愚公移山》），向大会提交《论联合政府》书面政治报告。大会确定以毛泽东思想作为全党一切工作的指针。6月19日，在中共七届一中全会上当选为中央委员会主席。7月，同国民参政员褚辅成、黄炎培等六人就国共关系进行会谈。谈到通过民主“新路”，跳出政党、团体兴亡“周期律”问题。8月9日，发表《对日寇的最后一战》的声明。8月13日，发表《抗日战争胜利后的时局和我们的方针》的讲演，提出对国民党实行针锋相对、寸土必争的方针，争取国内的和平与民主。8月28日，赴重庆同蒋介石进行和平谈判。9月2日，日本政府正式签署投降书。中国抗日战争胜利结束。10月10日，《国民政府与中共代表会谈纪要》（简称《双十协定》）在重庆签署。11日，回到延安。10月17日，在延安干部会上作关于重庆谈判的报告，指出中国革命“前途是光明的，道路是曲折的”。12月28日，起草《建立巩固的东北根据地》的指示。 [6]1946年4月，撰写《关于目前国际形势的几点估计》。6月26日，国民党军大举进攻中原解放区，全面内战爆发。7月4日，作出南线野战军“先在内线打几个胜仗再转至外线”的战略决策。7月20日，起草《以自卫战争粉碎蒋介石的进攻》的党内指示。8月6日，会见美国记者斯特朗，提出“一切反动派都是纸老虎”的著名论断。9月16日，为中共中央军委起草《集中优势兵力，各个歼灭敌人》的指示。10月1日，为中共中央起草党内指示，总结三个月战争的经验。11月18日，在为中共中央起草的党内指示中，第一次使用“人民解放战争”的名称。 [7]1947年3月18日，率中共中央机关和人民解放军总部撤离延安，开始历时一年的陕北转战。3月至8月，领导西北野战军先后取得青化砭、羊马河、蟠龙、沙家店战役的胜利，粉碎了国民党对陕北解放区的重点进攻。7月21日至23日，在陕北靖边县小河村主持召开中共中央会议，提出对蒋介石的斗争用五年时间（从1946年7月算起）解决的设想。在此前后，部署刘邓、陈粟、陈谢三路大军渡过黄河，转入战略进攻。10月，起草《中国人民解放军宣言》，提出“打倒蒋介石，解放全中国”的口号。11月，将1933年起草的《怎样划分阶级》和《关于土地斗争中一些问题的决定》重新印发给全党，以指导解放区土改运动正确发展。12月25日至28日，在陕北米脂县杨家沟主持召开中共中央会议（即十二月会议），向会议提交《目前形势和我们的任务》的书面报告，提出了十大军事原则和新民主主义的三大经济纲领。1948年1月18日，为中共中央起草《关于目前党的政策中的几个重要问题》的决定草案。3月23日，结束陕北转战，东渡黄河，前往华北解放区。4月1日，在山西兴县蔡家崖晋绥干部会议上发表重要讲话，阐明党的新民主主义革命总路线和土地改革总路线。4月30日至5月7日，在河北阜平县城南庄主持召开中共中央书记处扩大会议，提出把战争引向国民党统治区、发展生产、加强纪律性等几点意见。5月1日，致信李济深、沈钧儒，提出成立民主联合政府，宜先行召开新的政治协商会议。5月27日，到达中共中央工委所在地河北平山县西柏坡村。9月8日至13日，在西柏坡主持召开中共中央政治局会议，作关于战争、建国、财经等问题的重要报告。9月至次年1月，组织指挥辽沈、淮海、平津三大战略决战，将国民党军主力聚歼在长江以北。12月30日，为新华社写一九四九年新年献词《将革命进行到底》。1949年3月，主持召开中共七届二中全会，提出实现党的工作重心转移、夺取全国胜利以及关于新中国建设的指导方针和基本政策。3月25日，率中共中央机关和人民解放军总部进驻北平。4月21日，在南京政府拒绝接受《国内和平协定》的情况下，和朱德联名发布《向全国进军的命令》。4月23日，人民解放军占领南京，作诗《七律·人民解放军占领南京》。6月15日至19日，出席新政协筹备会议第一次全体会议，并在开幕式上讲话。6月30日，发表《论人民民主专政》一文。7月4日，复电程潜，对程提出的反蒋反桂及和平解决湖南问题之方针，给予赞许，并对有关事宜作出安排。9月21日至30日，出席中国人民政治协商会议第一届全体会议，致开幕词，当选中央人民政府主席。会议通过了由周恩来主持起草、经他多次审阅修改的《共同纲领》。10月1日，中华人民共和国成立，主持开国大典。12月5日，颁发《关于一九五零年军队参加生产建设工作的指示》。12月16日，抵达莫斯科，首次访问苏联。1950年2月14日，中苏签署《中苏友好同盟互助条约》。12月至翌年初，对和平解放西藏作出具体部署。1950年6月6日至9日，主持召开中共七届三中全会，提交《为争取国家财政经济状况的基本好转而斗争》的书面报告，并作《不要四面出击》的讲话。6月28日，主持召开中央人民政府委员会第八次会议，通过《中华人民共和国土地改革法》。10月上旬，主持中共中央政治局会议，作出“抗美援朝，保家卫国”的决策。10月8日，发布组成中国人民志愿军的命令，命令志愿军迅即向朝鲜境内出动，援助朝鲜人民，并任命彭德怀为志愿军司令员兼政治委员。随后亲自指导了第一次至第三次战役。10月以后，发动和领导了镇压反革命运动。 [7-8]1951-1960年1951年2月，在中共中央政治局扩大会议上提出“三年准备、十年计划经济建设”的思想。5月20日，写作的《应当重视电影〈武训传〉的讨论》一文以《人民日报》社论形式发表。5月24日，设宴庆贺《关于和平解放西藏办法的协议》签订。至此，中国大陆全境解放。9月，主持制定《中共中央关于农业生产互助合作的决议（草）》。10月12日，《毛泽东选集》第一卷出版发行。第二卷和第三卷分别于1952年4月和1953年4月出版发行。12月，发动反贪污、反浪费、反官僚主义的“三反”运动。 [9]1952年1月，主持全国政协常委会，通过《关于开展各界人士思想改造的学习运动的决定》。1月26日，为中共中央起草关于开展“五反” 运动的指示（“五反”即反对行贿、反对偷税漏税、反对盗骗国家财产、反对偷工减料、反对盗骗国家经济情报）。4月6日，为中共中央起草《关于西藏工作方针的指示》。8月9日，发布《中华人民共和国民族区域自治实施纲要》。9月，开始酝酿提出过渡时期总路线。1953年1月13日，中华人民共和国宪法起草委员会成立，任主席。3月26日，为中共中央起草关于反对大汉族主义思想的指示。6月15日，在中共中央政治局会议上讲话，对党在过渡时期总路线作出比较完整的表述。7月27日，朝鲜停战协定在板门店正式签字。9月7日，同民主党派和工商界部分代表谈话，指出国家资本主义是改造资本主义工商业的必经之路。10月15日、11月4日，两次同中共中央农村工作部负责人谈话。指出，各级农村工作部要把互助合作看作极为重要的事。1954年1月，开始在杭州主持起草中华人民共和国宪法。3月23日，主持宪法起草委员会第一次会议，提出中华人民共和国宪法草案初稿。9月15日至28日，出席全国人大第一届第一次全体会议，致开幕词《为建设一个伟大的社会主义国家而奋斗》，当选中华人民共和国主席。9月28日，中共中央军事委员会组成，任主席。10月16日，给中共中央政治局及有关同志写《关于红楼梦研究问题的信》。10月19日，在同印度总理尼赫鲁的谈话中提出，和平共处五项原则应推广到所有国家关系中去。1955年1月15日，批示刘少奇、周恩来、邓小平：“应对胡风的资产阶级唯心论，反党反人民的文艺思想，进行彻底的批判。”3月，在中国共产党全国代表会议上致开幕词并作结论，号召干部要钻研社会主义工业化问题，成为这方面的内行。5月12日，在最高国务会议上提出肃反工作方针。6月9日，为天安门人民英雄纪念碑题词：人民英雄永垂不朽。7月31日，在中共中央召集的省委、市委、自治区党委书记会议上作《关于农业合作化问题》的报告。9月至12月，主持编辑《中国农村的社会主义高潮》一书，写了两篇序言和104篇按语。10月4日至11日，主持召开中共七届六中全会，通过《关于农业合作化问题的决议》。10月29日，邀集全国工商联执行委员座谈私营工商业的社会主义改造问题。12月16日，修改中央关于知识分子问题的指示草案，提出要大批地培养知识分子，注意吸收高级知识分子入党。1956年1月20日，在中共中央召开的关于知识分子问题的会议上讲话，号召全党努力学习科学知识，同党外知识分子团结一致，为迅速赶上世界科学先进水平而奋斗。1月25日，主持最高国务会议正式讨论通过《1956年到1967年全国农业发展纲要（草案）》（即四十条）。2月至3月，先后听取34个中央工作部门的汇报，对经济建设问题进行系统的调查研究。4月初，审改《关于无产阶级专政的历史经验》。4月25日，在中共中央政治局扩大会议上作《论十大关系》的报告。4月27日，签名死后实行火葬。4月28日，在中共中央政治局扩大会议上提出“百花齐放，百家争鸣”的方针。8月22日，主持召开中共七届七中全会，提出两个工作重点，一个是社会主义改造，一个是经济建设，两个重点中主要的还是在建设。9月15日至27日，主持召开中国共产党第八次全国代表大会，致开幕词。在八大期间，再次强调了加强经济建设的重要性。9月28日，在中共八届一中全会上当选为中央委员会主席。11月15日，在中共八届二中全会上讲话：我们的经济建设有退有进，主要的还是进。12月，审改《再论无产阶级专政的历史经验》。 [9]1957年2月27日，作《关于正确处理人民内部矛盾的问题》讲话，提出两类矛盾学说。3月12日，在中国共产党全国宣传工作会议上讲话，宣布开始在党内进行整风。4月30日，邀集各民主党派负责人座谈，请他们帮助共产党整风。5月15日，写《事情正在起变化》一文，随后发动反右派斗争，发生严重扩大化的错误。9月20日至10月9日，主持召开中共八届三中全会，在会上对八大决议中关于中国社会的主要矛盾的论述提出异议，认为应该回到党的七届二中全会的提法。11月，率中国党政代表团访问苏联，参加十月革命四十周年庆祝活动，出席共产党和工人党的代表会议。期间，提出15年内中国主要工业产品的产量要赶超英国。 [10]1958年1月，主持召开中共中央南宁会议，起草《工作方法六十条（草案）》。在会上批评“反冒进”。3月，主持召开中共中央成都会议。会议继续批评“反冒进”，制定的各项经济指标大幅度提高。5月5日至23日，主持召开中共八大二次会议。会议改变八大一次会议的有关结论，认为两个阶级、两条道路的斗争仍然是国内主要矛盾。会议通过“鼓足干劲，力争上游，多快好省地建设社会主义”的总路线。7月31日至8月3日，同来访的苏共中央第一书记赫鲁晓夫会谈，拒绝了苏方提出的侵犯中国主权的关于建立联合舰队和长波电台的建议。7月至8月，部署炮击金门。8月6日，视察河南新乡七里营人民公社。说到“人民公社这个名字好”。8月17日至30日，在北戴河主持召开中共中央政治局扩大会议，通过《关于在农村建立人民公社问题的决议》。11月2日至10日，主持召开第一次郑州会议，开始纠正“大跃进”和人民公社化运动中的“左”倾错误。会议期间，给县以上四级党委写信，要求学习《苏联社会主义经济问题》和《马恩列斯论共产主义社会》。11月28日至12月10日，在武昌主持召开中共八届六中全会，通过《关于人民公社若干问题的决议》。1959年2月27日至3月5日主持召开第二次郑州会议，3月25日至4月5日在上海召开中共中央政治局扩大会议和八届七中全会，继续纠正“左”倾错误。4月，根据毛泽东的意见，第二届全国人大第一次会议通过他不再担任国家主席，由刘少奇担任的决议。6月25日至28日，回故乡韶山。7月2日至8月16日，在庐山主持召开中共中央政治局扩大会议和八届八中全会。政治局扩大会议原拟进一步纠正“左”的错误，但在后期和接着召开的八届八中全会上错误地发起了对彭德怀等的批判。 [11]8月24日，建议分期分批为右派分子摘帽和赦免一批确实改恶从善的战犯等。9月17日，中共中央下发了《关于摘掉确实悔改的右派分子的帽子的指示》；全国人大常委会第九次会议通过了《关于特赦确实改恶从善的罪犯的决定》。12月10日至翌年2月9日，组织有陈伯达、胡绳、邓力群、田家英参加的读书小组，先后在杭州、上海和广州，学习讨论苏联《政治经济学（教科书）》，并发表了许多谈话。1960年3月，在广州审定《毛泽东选集》第四卷。九月出版发行。3月30日，为中共中央起草《关于反对官僚主义的指示》。6月14日至18日，在上海主持召开中共中央政治局扩大会议，写《十年总结》一文，重新强调实事求是原则，提出要认真研究社会主义革命和建设的规律。7月5日至8月10日，主持在北戴河召开的中共中央工作会议，研究国际问题和国内经济调整问题。11月15日，为中共中央起草《关于彻底纠正“五风”问题的指示》。（“五风”，即共产风、浮夸风、命令风、干部特殊风和瞎指挥风。）1961-1970年1961年1月14日至18日，主持召开中共八届九中全会，号召大兴调查研究之风。这次会议正式批准了调整国民经济的八字方针。会后组织和领导三个调查组，深入浙江、湖南、广东农村调查研究。5月21日至6月12日，主持召开中共中央工作会议，讨论修改《农村人民公社工作条例（草案）》（即农业六十条）。其中规定，取消供给制；办不办食堂，完全由社员讨论决定。8月23日至9月16日，在庐山主持召开中共中央工作会议，讨论工业、粮食、财贸、教育等问题。会议强调切实地执行调整经济的八字方针。9月29日，提出“三级所有，队为基础”，将农村人民公社的基本核算单位下放到生产队。 [10]1962年1月11日至2月7日，主持召开中共扩大的中央工作会议（又称“七千人大会”），作关于民主集中制问题的重要讲话。7月至9月，在北戴河、北京先后召开中共中央工作会议和八届十中全会，批判所谓“黑暗风”、“单干风”、“翻案风”，作关于阶级、形势、矛盾和党内团结问题的讲话，进一步发展了关于阶级斗争是社会主义社会的主要矛盾的错误论点。1963年2月11日至28日，召开中共中央工作会议，会议确定在农村普遍进行“四清”运动和城市开展“五反”运动。3月5日，在《人民日报》发表题词“向雷锋同志学习”。5月，在杭州主持制定《中共中央关于目前农村工作若干问题的决定（草案）》（简称“前十条”），作为指导农村“四清”的纲领性文件。12月16日，听取聂荣臻关于科学技术十年规划的汇报，指出：不搞科学技术，生产力无法提高。12月，作出关于文艺工作的第一个批示。1964年2月13日，召集教育工作座谈会，提出改革教育体制的设想。5月，在听取关于第三个五年计划的汇报时，提出两个拳头（农业、国防）一个屁股（基础工业）的思想；还提出把全国划分为一、二、三线的战略布局。6月15日和16日，观看北京、济南部队军事训练汇报表演。6月16日，在北京十三陵召开的小型会议上，作关于培养无产阶级革命事业接班人的讲话。6月，再次对文艺工作作批示，文艺界进而扩大到意识形态其他领域，错误地开展了过火的政治批判。10月16日，中国第一颗原子弹爆炸成功。12月15日至28日，主持召开中央工作会议，讨论制定《农村社会主义教育运动中目前提出的一些问题》（简称“二十三条”），部分地纠正“四清”运动中“左”的做法，但错误地提出“运动的重点是整党内那些走资本主义道路的当权派”。 [12]1965年5月22日至29日，重上井冈山。7月27日，会见从海外归来的原国民党政府代总统李宗仁和夫人。11月初，批准发表《评新编历史剧〈海瑞罢官〉》一文，揭开“文化大革命”的序幕。1966年3月12日，致信刘少奇，提出“备战备荒为人民”。3月底，错误地指责由彭真主持制定的文化革命五人小组《关于当前学术讨论的汇报提纲》。 [12]5月7日，作出“五·七指示”，提出人民解放军“应该是一个大学校”，各行各业要以本业为主，“兼学别样”，“教育要革命”等。5月16日，中共中央政治局扩大会议通过毛泽东主持制定的《中国共产党中央委员会通知》，对当时党和国家政治形势作了严重错误的估计。8月1日至12日，主持召开中共八届十一中全会，通过《关于无产阶级文化大革命的决定》。会议期间，印发了毛泽东5日写的《炮打司令部——我的一张大字报》，不点名地批评了刘少奇、邓小平。5月的中央政治局扩大会议和这次会议的召开，是“文化大革命”全面发动的标志。8月18日至11月26日，在北京先后八次接见来自全国各地的院校师生和红卫兵。1967年1月，对上海“一月革命”表示支持。此后夺权之风遍及全国。1月23日，批示发出《中国人民解放军坚决支持革命左派群众的决定》。2月11日和16日，谭震林、陈毅、叶剑英、李富春、李先念、徐向前、聂荣臻等不满林彪、江青一伙的倒行逆施，对“文化大革命”的错误做法提出了强烈的批评，是为“大闹怀仁堂”。毛泽东在听取了中央文革小组的汇报后，表示很不满意。 [12]6月17日，中国第一颗氢弹爆炸成功。7月至9月，视察华北、中南和华东地区，号召“实现革命的大联合”，指出“正确地对待干部”。8月底，批准对中央文革小组成员王力、关锋实行隔离审查。1968年1月，又对戚本禹实行隔离审查。1968年1月16日，对江青等人送来的所谓“伍豪等脱离共产党启事”等材料作出重要批示：“此事早已弄清，是国民党造谣污蔑”，使他们诬陷周恩来的图谋未能得逞。10月13日至31日，主持召开中共八届十二中全会，在极不正常的情况下，通过诬陷刘少奇并开除他的党籍的错误决定。 [12]12月22日，“知识青年到农村去，接受贫下中农的再教育，很有必要”的指示，在《人民日报》发表，知识青年上山下乡的热潮由此开始。1969年4月1日至24日，主持召开中国共产党第九次全国代表大会，批准“文化大革命”的错误理论和实践，并把林彪定为接班人写入党章。 [13]4月28日，在中共九届一中全会上再次当选为中央委员会主席。1970年4月24日，中国第一颗人造地球卫星发射成功。5月20日，发表《全世界人民团结起来，打败美国侵略者及其一切走狗！》的声明。8月23日至9月6日，在庐山主持召开中共九届二中全会，写《我的一点意见》，揭露挫败林彪、陈伯达企图抢班夺权的阴谋。12月18日，会见美国友人斯诺，表示欢迎美国总统尼克松来华访问。1971-1976年1971年8月至9月，在南方巡视期间，同当地党政军负责人多次谈话，揭露林彪的阴谋。途中机警地几次变更行动计划，于9月12日回到北京，粉碎林彪集团的反革命武装政变阴谋。9月13日，同周恩来等果断地处理林彪叛逃事件。在周恩来请示要不要拦截林彪座机时，毛泽东表示：“由他去吧”。10月25日，第二十六届联合国大会以压倒多数通过决议，恢复中华人民共和国在联合国的一切合法权利，把蒋介石集团的代表驱逐出去。11月14日，接见参加成都地区座谈会的同志，为所谓“二月逆流”平反。1972年1月10日，参加陈毅的追悼会。2月21日，会见来华访问的美国总统尼克松；28日，中美双方在上海发表联合公报，决定实现中美两国关系正常化。9月27日，会见日本内阁总理大臣田中角荣；29日，中日两国政府发表联合声明，宣布实现中日邦交正常化，正式建立外交关系。1973年3月，提议恢复邓小平的国务院副总理职务。8月24日至28日，主持召开中国共产党第十次全国代表大会，使一批老一辈无产阶级革命家重新进入中央委员会，但同时江青集团的势力也得到加强。8月30日，在中共十届一中全会上当选中央委员会主席。12月，提出邓小平担任中共中央政治局委员、人民解放军总参谋长。还提出要给贺龙、罗瑞卿、杨成武、余立金、傅崇碧平反。1974年1月18日，批准转发《林彪与孔孟之道》材料。“批林批孔”运动由此开始。2月22日，会见赞比亚总统卡翁达，谈话中提出“三个世界”划分的思想。7月17日，在中共中央政治局会议上批评王洪文、张春桥、江青、姚文元搞帮派活动，第一次提出“四人帮”问题。9月29日，经毛泽东批准，中共中央为贺龙平反。10月4日，提议由邓小平担任国务院第一副总理职务。11月12日，对江青来信作批示，批评她的“组阁”野心，明确指出“不要由你组阁（当后台老板）”。1975年1月13日至17日，第四届全国人民代表大会第一次会议在北京举行，会议重申在本世纪内实现四个现代化，选出以朱德为委员长的全国人大常务委员会组成人员，任命周恩来为总理、邓小平等为副总理的国务院组成人员。会后，周恩来病重，国务院工作实际由邓小平主持。2月，在毛泽东支持下，邓小平开始领导对铁路、教育等方面的调整整顿工作。5月3日，召集在北京的中共中央政治局委员谈话，强调要搞马列主义，要团结，要光明正大，再次批评“四人帮”。7月14日，对文艺问题发表谈话，指出党的文艺政策应该调整。11月下旬，审阅批准《打招呼的讲话要点》，错误地发动所谓“批邓、反击右倾翻案风”运动。 [13]1976年1月8日，周恩来在北京逝世。1月21日、28日，先后提议华国锋任国务院代总理和主持中央日常工作。3月下旬至4月5日，北京市上百万群众连续几天自发到天安门广场，献花圈、诗词，悼念周恩来，声讨“四人帮”。毛泽东错误地批准了否定“天安门事件”的报告 [13] 。4月7日，根据毛泽东提议，中共中央政治局通过《中共中央关于华国锋同志任中共中央第一副主席、国务院总理的决议》和《关于撤销邓小平党内外一切职务的决议》。9月9日，在北京逝世。 [13]主要作品 播报《毛泽东选集》：毛泽东的主要著作集。《毛泽东文集》：中共中央文献研究室编，人民出版社1993年起陆续出版，编入了《毛泽东选集》以外的毛泽东重要文稿。《毛泽东诗词》：毛泽东创作的旧体诗词作品。 [14]"
    # print(len(test))
    # sent = cut_sent("如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号")
    # print(sent)
    # content = "乙基叠氮乙酸酯是一种化学物质，化学式是C4H7N3O2。InChI编码\n1S/C4H7N3O2/c1-2-9-4(8)3-6-7-5/h2-3H2,1H3\n其他名称\nACETICACID,AZIDO-,ETHYLESTER(7CI,8CI,9CI);\n(ETHOXYCARBONYL)METHYLAZIDE;\n2-AZIDOACETATEETHYLESTER;\nAZIDOACETICACIDETHYLESTER;\nETHYL2-AZIDOACETATE;\nETHYLAZIDOACETATE;\nETHYLA-AZIDOACETATE;\nNSC84132;\n"
    # content = "化学式是C4H7N3O2。InChI编码\n1S/C4H7N3O2/c1-2-9-4(8)3-6-7-5/h2-3H2,1H3\n其他名称\nACETICACID,AZIDO-,ETHYLESTER(7CI,8CI,9CI);\n(ETHOXYCARBONYL)METHYLAZIDE;\n2-AZIDOACETATEETHYLESTER;\nAZIDOACETICACIDETHYLESTER;\nETHYL2-AZIDOACETATE;\nETHYLAZIDOACETATE;\nETHYLA-AZIDOACETATE;\nNSC84132;\n"
    # sub_content = content[:100]
    # if "是一种化学物质" in sub_content:
    #     print("存在")
    # else:
    #     print("不存在")
    #
    # content = "第283啊"
    # if re.search('第.*?章', content):
    #     print("已章节开头")
    # else:
    #     print("不已章节开头")

    print(contain_err_num("", "孙淑2方3案"))

if __name__ == '__main__':
    content = "残疾人如何办理福利彩票店2020年02月23日 04:18\n目前联合光电已是高新技术企业和广东省工程技术研究中心。依托强大的研发设计能力、优异的产品性能和齐全的产品线结构，已在行业内树立了良好的市场口碑，客户认知度高，市场地位突出。 该公告称，公司正组织有关各方积极有序地推进本次重大资产重组的各项工作，而本次资产重组交易涉及海外收购，且对价支付方式为发行股份购买资产，所涉及的工作程序复杂，相关工作尚未最终完成，且具有不确定性。 对于这一镜头厂商cheng功上市消息的爆出，ye内摄像头ren士geng是发出这样的感叹：龚zong的坚持和努力，令人钦佩。 近】【年】【，】【重】【庆】【抓】【住】【市】【场】【趋】【势】【，】【积】【极】【打】【造】【智】【能】【终】【端】【手】【机】【产】【业】【生】【态】【圈】【，】【规】【划】【目】【标】【实】【现】【全】【球】【手】【机】【1】【/】【4】【在】【重】【庆】【研】【发】【生】【产】【的】【产】【业】【集】【群】【。】【手】【机】【报】【在】【线】【举】【办】【的】【本】【次】【“】【2】【0】【1】【7】【国】【际】【手】【机】【产】【业】【暨】【智】【能】【制】【造】【博】【览】【会】【”】【希】【望】【能】【够】【促】【进】【商】【品】【流】【通】【的】【同】【时】【带】【动】【手】【机】【产】【业】【加】【速】【发】【展】【升】【级】【。 刘军一呼百应，事业部负责人陈文晖、产品研发负责人常程、销售负责人冯幸、曾国章等人都陆续加盟。 诸多前联想手机人士认为，刘军的另外一个问题在于不懂产品，包括产品上市的节奏、产品的成本、产品的卖点，他都拿捏不准，并没有对运营商市场和开放市场的深刻理解。 刘军是个豪气的人。2013年4月初，为犒劳团队将士和重要合作伙伴，他包了一条大游轮，邀请了以销售为主的联想移动员工共计三四百人上船吃喝玩乐，从三亚开到越南然后再返回。这也是刘军承诺给冯幸和曾国章的庆祝活动。\n现如今，智能手机市场进入了存量时代，性能、审美和差异化三个维度成为手机厂商的角力场，手机摄像头层出不穷的应用创新更有力证明了这点。其中，尤以双摄像头的分配最为亮眼，也成为了下一波智能手机规格升级浪潮中不可忽视的力量，而这无疑都提高了手机镜头的使用率。 韦尔股份自8月4号发布公告称，因并购北京豪威科技有限公司（以下简称“北京豪威”）资产重组而持续停牌以来，并购进展深受业界人士关注。8月18号晚间，韦尔股份发布了该资产重组的最新进展公告。 对于乐shi电视业务，孙宏斌高度认可。zai融创业绩发布会上，孙宏斌biao示，“wo们投资乐视的逻辑没变，乐视是了不起的公司，前瞻性特别好。我看的是3——5年后的事，现在股票跌了和我们关系不大。乐视电视比苹果APP做得还好，是全球都认的，肯定是非常值钱，我特别有信心。” 下】【沉】【的】【庆】【功】【游】【轮 双镜头相机可呈现浅景深等高画质拍摄效果，相较于华为、苹果(Apple)等手机业者早已在产品上搭载双镜头相机模组，先前三星在双镜头的采用倾向保守姿态。 “将主要责任推到下属头上，万一遇到问题，按照联想的惯例，进退都有保障”一位前联想的管理人士艾奋希（化名）如此告诉腾讯科技。 2013年，杨元庆发内部邮件宣布，联想在当年4月1日拆分成Lenovo业务集团和Think业务集团。其中Lenovo业务集团包含联想电脑和原移动业务，由刘军负责。\n此外，公告还显示，为了解决公司控股股东贾跃亭及其配偶甘薇女士涉及的同业竞争事宜，经协商，公司拟收购甘薇女士持有的北京乐漾影视传媒有限公司47.8261%股权。待前述方案实施完成后，甘薇女士不再持有乐漾影视的股权。 双镜头相机模组对零组件业界上游业者的影响力不容忽视。因为双镜头模组的单价约是单镜头模组的1.5倍，且三星从GalaxyNote8开始扩大采用后，将快速带动相关产业发展。 在车载镜头领域，联合光电已通guo相关认证，并zheng逐步通过下游模组厂商向广qi本田、长城汽车、上海通用、海nan马自达、奇瑞汽车等整车厂商推广，以不断提高在专业前装市场、行车记lu仪市场的市场份额和zhan有率。 其】【生】【产】【的】【像】【素】【为】【5】【M】【、】【8】【M】【、】【1】【3】【M】【、】【2】【1】【M】【等】【中】【高】【端】【产】【品】【已】【经】【被】【华】【为】、】【L】【G】【、】【T】【C】【L】【、】【D】【X】【O】【等】【客】【户】【采】【用】【，】【获】【得】【了】【一】【定】【的】【市】【场】【份】【额】【。 这种管理风格，很容易造成不同业务领域之间的高管互相对立，谁都想把责任推到对方的板块。 尽管当下乐视获得融创投资暂时缓解了乐视缺钱的问题，但是想要在乐视生态的诸多领域进行发力甚至扭转局面，并非易事。 刘军曾试图改变这个局面，2012年下半年他在吉林长白山与联想移动管理层制定的2013年目标中，就包括让运营商与开放市场销量占比从6：4扭转为4：6，但2013年最后运营商与开放市场销量占比反而上升至8：2。"
    print(is_dirty_web("", content))
