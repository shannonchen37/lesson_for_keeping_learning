## 实验三:A*算法求解迷宫寻路问题

[TOC]

### 1.实验内容：

​	熟悉和掌握A*算法实现迷宫寻路功能，掌握启发式函数的编写以及各类启发式函数效果的比较。

### 2.环境配置：

​	python3 + vscode + markdown

### 3.实验原理：

<img src="A*%E8%BF%B7%E5%AE%AB.assets/%E6%88%AA%E5%B1%8F2022-06-09%2023.16.43.png" alt="截屏2022-06-09 23.16.43" style="zoom:40%;" />

<center>A*解决迷宫问题<center>

求解思路：

（1）在明确地算出了顶点到起始顶点的距离（G）和顶点到目标顶点的距离（H）

（2）我们只要在选择走哪个格子的时候，选择G+H的值最小的格子**，**这个值暂且命名为F，F = G + H，该值代表了在当前路线下选择走该方块的代价。

### 4.实验算法：

#### 算法流程：

- 首先将根节点放入队列中。
- 将根节点放入封闭列表
- 开始循环
- 从队列中找f值【总代价】最小的节点current
- 如果找到目标，则结束搜寻并回传结果。
- 否则将它所有尚未检验过的所有相邻节点加入队列中。
- 假如某邻近点既没有在开放列表或封闭列表里面，则计算出该邻近点的g值和h值，并设父节点为P，然后将其放入开放列表
- gCost = current.gCost + GetDistance(current, neighbor)
- hCost = GetDistance(end, neighbor)
- 直至没有节点可以访问

#### 源代码及注释：

```python
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
    """计算当前节点估价值, 计算公式表示为f(x) = g(x) + h(x)"""
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
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 1],
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
```

### 5.实验分析与结果：

#### 实验结果：

<img src="A*%E8%BF%B7%E5%AE%AB.assets/%E6%88%AA%E5%B1%8F2022-06-09%2023.26.30.png" alt="截屏2022-06-09 23.26.30" style="zoom:40%;" />

<center>迷宫问题和求解路径展示<center>

> 注：设定左上角为入口，右下角为出口

<img src="A*%E8%BF%B7%E5%AE%AB.assets/%E6%88%AA%E5%B1%8F2022-06-10%2016.17.27.png" alt="截屏2022-06-10 16.17.27" style="zoom:50%;" />

<center>自动退出无法求解的迷宫问题<center>

> 注：当出现无法解决的迷宫问题时，能自动退出求解过程，避免出现死循环

#### 结果分析：

​		在迷宫问题中，我们用0表示可以走的路径，用1表示障碍，在求解路径中，我们用100作为我们求解的起点，每走一步我们都在原先的数字上+1，最终，我们得到了一个以100为起点，112为终点，共计13步的求解路径。而当出现了无解的迷宫问题或是太过复杂的迷宫问题时，程序容易陷入死循环，我设置了10秒的处理时长，超过时长后程序自动退出，输出无法求解。

### 6.实验心得：

​		A*通过维护2个列表，开放和封闭列表，每次寻路的时候，从开放列表找出一个总代价最小的节点，如果不是终点，就算出起点到当前位置的移动代价G和当前位置到终点的移动代价H，计算出总代价F，然后加入封闭列表，并把这个节点所有的邻居都遍历一遍，计算总代价，加入开放列表，然后循环遍历，直到找到终点。

​		在实验中，对比盲目搜索的广度优先算法和深度优先算法，可以发现启发式的A*相比宽度优先搜索，效率更高，所耗时间更少，相比深度优先搜索，可以解决其不能找到最优解的不足。

### 7.改进点：

​		1.用户修改迷宫时需要在代码中一个个的修改0和1，比较麻烦，可以写一个读取数字的函数，一行中1的位置即可，其他的位置默认置0；

​		2.A*的计算两较大，有时会出现求解时间过长的情况，而且遇到了无法求解的迷宫问题还会造成死循环，为了解决这个问题，我仅仅规定了运行时间，这就会导致可能较复杂但是存在解的迷宫问题被判定为无解，后续可以做具体的理论推算和实验，按照矩阵的大小规定运行时间。

​		



















