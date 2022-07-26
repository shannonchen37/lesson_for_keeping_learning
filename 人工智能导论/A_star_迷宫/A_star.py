import numpy as np
import time


def findSmallestCost(openList, closeList):
    """寻找此时open表中估价最小的节点"""
    maxCost = 1e8
    smallestCostLabel = None
    for i in range(len(openList)):
        if i not in closeList and openList[f"{i}"]["cost"] <= maxCost:
            maxCost = openList[f"{i}"]["cost"]
            smallestCostLabel = i
    return smallestCostLabel


def calNodeCost(puzzle, point):
    """计算当前节点估价值, 计算公式表示为f(x) = g(x) + h(x),其中g(x)表示从起点到
    当前节点的实际距离, 表示为g(x) = sqrt((dx - x)^2 + (dy - y)^2), 实际意
    义为欧式距离,h(x)表示从当前节点到目标节点的估算距离, 这里选择的启发式函数为
    h(x) = |dx - x| + |dy - y|, 实际意义为曼哈顿距离"""
    initIdx = np.array([0, 0])
    endIdx = np.array([puzzle.shape[0] - 1, puzzle.shape[1] - 1])
    cost = np.sqrt(
        np.power(initIdx[0] - point[0], 2) + np.power(initIdx[1] - point[1], 2)
    ) + (np.abs(endIdx[0] - point[0]) + np.abs(endIdx[1] - point[1]))
    # cost = np.abs(initIdx[0] - point[0]) + np.abs(initIdx[1] - point[1]) + \
    #        np.sqrt(np.power(endIdx[0] - point[0], 2) + np.power(endIdx[1] - point[1], 2))
    return cost


def recordNextNode(puzzle, visitPuzzle, openList, currentLabel, label):
    """迭代计算下一步, 包括寻找下一步可以走的坐标, 还有估价计算, 并添加入open表中"""
    m, n = puzzle.shape
    startIdx = openList[f"{currentLabel}"]["currentIdx"]
    fatherIdx = None
    if openList[f"{currentLabel}"]["fatherNode"]:
        fatherLabel = openList[f"{currentLabel}"]["fatherNode"]
        fatherIdx = openList[f"{fatherLabel}"]["currentIdx"]
    aroundPoint = list()  # 记录可以前进的点坐标
    aroundX = [
        startIdx[0] - 1 if startIdx[0] > 0 else None,
        startIdx[0] + 1 if startIdx[0] < (m - 1) else None,
    ]
    aroundY = [
        startIdx[1] - 1 if startIdx[1] > 0 else None,
        startIdx[1] + 1 if startIdx[1] < (n - 1) else None,
    ]
    for idx in range(len(aroundX)):
        x, y = aroundX[idx], aroundY[idx]
        if x != None:
            if (
                puzzle[x][startIdx[1]] == 0
                and (np.array([x, startIdx[1]]) != fatherIdx).any()
            ):
                aroundPoint.append([x, startIdx[1]])
        if y != None:
            if (
                puzzle[startIdx[0]][y] == 0
                and (np.array([startIdx[0], y]) != fatherIdx).any()
            ):
                aroundPoint.append([startIdx[0], y])
    for point in aroundPoint:
        cost = calNodeCost(puzzle, point)
        openList[f"{label}"] = {
            "currentIdx": np.array(point),
            "fatherNode": currentLabel,
            "cost": cost,
        }
        visitPuzzle[point[0]][point[1]] += 1
        label += 1
    return openList, visitPuzzle, label


def aStarSolvingPuzzle(puzzle):
    """主函数, 用于求解输入的迷宫"""
    t=time.time()
    initIdx = np.array([0, 0])
    endIdx = np.array([puzzle.shape[0] - 1, puzzle.shape[1] - 1])
    label = 1  # 标记方便用于表示父子节点
    openList = dict()  # open表初始化
    closeList = list()  # close表初始化
    visitPuzzle = np.zeros((puzzle.shape[0], puzzle.shape[1]))
    openList["0"] = {"currentIdx": initIdx, "fatherNode": None, "cost": 1e5}
    while True:
        smallestCostLabel = findSmallestCost(openList, closeList)
        closeList.append(smallestCostLabel)
        openList, visitPuzzle, label = recordNextNode(
            puzzle, visitPuzzle, openList, smallestCostLabel, label
        )
        if visitPuzzle[endIdx[0]][endIdx[1]] > 0:
            break
        if time.time()-t>10:
            global sign
            sign = 0 
            break
    return openList, closeList


def mapPuzzle(puzzle, openList, closeList):
    """通过求解迷宫得到的open表和close表, 绘制路线"""
    flag = 100
    for label in closeList:
        idx = openList[f"{label}"]["currentIdx"]
        puzzle[idx[0]][idx[1]] = flag
        flag += 1
    puzzle[-1][-1] = flag
    return puzzle

#================main==========================

''' mat = np.array(
    [
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
    ]
)  '''

mat = np.array(
    [
        [0, 0, 0, 0, 0, 0,0],
        [1, 0, 1, 0, 1, 0,0],
        [0, 0, 1, 1, 1, 0,0],
        [0, 1, 0, 0, 0, 0,0],
        [0, 0, 0, 1, 0, 1,1],
    ]
) 


print("迷宫问题：")
print(mat)
start_time=time.time()
openMap, closeMap = aStarSolvingPuzzle(mat)
map = mapPuzzle(mat, openMap, closeMap)
if sign==1:
    print("求解路径展示：")
    print(map)
    print("A*解决迷宫寻路问题的运行时间:{}(s)".format(time.time()-start_time))
elif sign==0:
    print("无法求解！")


