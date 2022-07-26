class rule:
    def __init__(self, p, q):
        self.__p = p
        self.__q = q

    def get_p(self):
        return self.__p

    def get_q(self):
        return self.__q

    def matching(self, feture):
        cnt = 0
        for i in self.__p:
            if i in feture:
                cnt += 1
        if cnt == len(self.__p):
            return self.__q
        else:
            return -1


class insect_recognition_system:
    def __init__(self, name, feature, rule):
        self.__name = name
        self.__feature = feature
        self.__rule = rule

    def forward_reasoning(self, synthesis_database):
        for r in self.__rule:
            result = r.matching(synthesis_database)
            if result != -1:
                t = r.get_p()
                for f in t:
                    if f != t[-1]:
                        print(self.__feature[f], end=" & ")
                    else:
                        print(self.__feature[f], end="")
                print(" -> {}".format(self.__feature[result]))
                if self.__feature[result] in self.__name:
                    return self.__feature[result]
                synthesis_database.append(result)
        print("特征不足,推理失败.")


feature = [
    "0:飞行快",
    "1:尾部亮黑",
    "2:有斑点",
    "3:下唇黄褐色",
    "4:体黄褐色",
    "5:背棕黑",
    "6:胸深蓝色",
    "7:暗色斑纹",
    "8:雌额宽",
    "9:体青绿色",
    # 0         1           2           3           4           5       6           7          8          9
    "10:只有一对翅膀",
    "11:前翅狭长",
    "12:翅膀膜质透明",
    "13:翅膀多",
    "14:粗壮",
    "15:头部半球形",
    "16:复眼",
    "17:刺吸式口器",
    # 10            11          12              13      14      15          16          17
    "18:双翅目",
    "19:直翅目",
    "20:蜻蜓目",
    "21:虻类",
    "22:蚊类",
    "23:蝇类",
    # 18        19      20          21      22      23
    "24:中华盗虻",
    "25:麻蝇",
    "26:中华按蚊",
    "27:巨圆臀大蜓",
    "28:牛虻",
    "29:绿蝇",
    "30:乐仙蜻蜓",
    "31:东亚飞蝗"
    # 24        25      26          27          28      29      30          31
]
name = ["中华盗虻", "麻蝇", "中华按蚊", "巨圆臀大蜓", "牛虻", "绿蝇", "乐仙蜻蜓", "东亚飞蝗"]

R = [
    rule([10], 18),
    rule([11], 19),
    rule([12, 13], 20),
    rule([18, 14], 21),
    rule([18, 15], 22),
    rule([18, 16], 22),
    rule([18, 17], 23),
    rule([18, 21, 0], 24),
    rule([18, 1, 5, 8], 25),
    rule([18, 2, 0], 26),
    rule([20, 1, 3], 27),
    rule([18, 21, 4, 5, 8], 28),
    rule([20, 1, 5, 6], 30),
    rule([19, 4, 7, 8], 31),
]


def run():
    print("可以判断的昆虫名称：")
    print(name)
    print("规则的编号：")
    print(feature[0:24])
    model = insect_recognition_system(name, feature, R)
    while 1:
        print("\n请输入综合数据库（特征之间以空格隔开,输入-1结束程序):")
        synthesis_database = list(map(lambda x: int(x), list(input().split(" "))))
        if -1 in synthesis_database:
            print("程序已结束")
            break
        else:
            model.forward_reasoning(synthesis_database)


if __name__ == "__main__":
    run()
