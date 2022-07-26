## 实验二:A*算法求解8数码问题实验

[TOC]

### 1.实验内容：

​	掌握启发式搜索的定义、估价函数和算法过程，利用A*算法求解8数码难题，理解求解流程和搜索顺序。

### 2.环境配置：

​	python3 + vscode + markdown

### 3.实验原理：

<img src="A*%E5%85%AB%E6%95%B0%E7%A0%81.assets/v2-62b7b2cf0b3331b0232852877f06f37c_1440w.jpg" alt="v2-62b7b2cf0b3331b0232852877f06f37c_1440w" style="zoom:75%;" />

<center>8数码问题表示<center>


问题分析：

（1）对于八数码问题的解决，首先要考虑是否有答案。每一个状态可认为是一个1×9的矩阵，问题即通过矩阵的变换，是否可以变换为目标状态对应的矩阵？由数学知识可知，可计算这两个有序数列的逆序值，如果两者都是偶数或奇数，则可通过变换到达，否则，这两个状态不可达。这样，就可以在具体解决问题之前判断出问题是否可解，从而可以避免不必要的搜索。

（2）如果八数码问题有解，我们要确定是深度搜索和广度搜索，缺点是他们都是在一个给定的状态空间中穷举。这在状态空间不大的情况下是很合适的算法，可是当状态空间十分大，且不预测的情况下就不可取了。他的效率实在太低，甚至不可完成。由于八数码问题状态空间共有9!个状态，对于八数码问题如果选定了初始状态和目标状态，有9!/2个状态要搜索，考虑到时间和空间的限制，不妨采用启发式搜索中A*算法作为搜索策略。

（3）估价函数：
$$
f^*(n) = g^*(n) +h^*(n)
$$
​			n表示搜索图中的某个当前被扩展的节点；f表示从起点出发，通过n到达目标的路径总代价的估计值；g表示从起点到n状态的最短路径代价；h表示n状态到达目的状态的最短路径代价。

### 4.实验算法：

#### 算法流程图：

<img src="A*%E5%85%AB%E6%95%B0%E7%A0%81.assets/v2-184d96e083330bc8f2827aace40eaeab_r.jpg" alt="v2-184d96e083330bc8f2827aace40eaeab_r" style="zoom:75%;" />

<center>算法流程图<center>
#### 实验方案：

​		（1）首先判断八数码问题是否可解，定义一个calInversionSum函数，计算序列逆序数之和, 返回逆序数之和的奇偶性；

​		（2）如果可解，我们将当前的状态存入open表，并且根据估价函数求出小的点，表示花费代价最小；

​		（3）如果在open表中发现了目标节点，则输出；若没有，则存入close表并移出open表；

​		（4）重复（2）和（3）



#### 源代码及注释：

```python
import numpy as np
import time


def calInversionSum(arrayList):
    """计算序列逆序数之和, 返回逆序数之和的奇偶性."""
    totalSum = 0
    arrayList = np.delete(arrayList, np.where(arrayList == 0)[0][0])
    for i in range(1, len(arrayList)):
        for j in range(i):
            if arrayList[j] > arrayList[i]:
                totalSum += 1
    print("Inversion:", totalSum)
    return totalSum % 2


def calCost(depth, statusMat, targetMat):
    """计算当前状态估价值"""
    totalCost = depth
    for y in range(statusMat.shape[0]):
        for x in range(statusMat.shape[1]):
            element = statusMat[y][x]
            if element == 0:
                continue
            targetY, targetX = np.argwhere(targetMat == element)[0]
            totalCost += np.abs(targetY - y) + np.abs(targetX - x)
    return totalCost


def createNewLabel(openList, depth):
    currentLabel = ["@"]
    for key, value in openList.items():
        if int("".join(filter(str.isdigit, key))) == depth:
            currentLabel.append(key[6])
    return chr(ord(max(currentLabel)) + 1) + "".join(str(depth))


def createPossibleStatus(openList, closeList, stopFlag, targetMat):
    """计算将当前状态可能存在的移动方法的估价值并添加进open表"""
    minCostScore = 1e10
    bestKey, bestValue = None, None
    for key, value in openList.items():
        if value["costScore"] <= minCostScore and value["label"] not in closeList:
            minCostScore = value["costScore"]
            bestKey, bestValue = key, value
    matDepth = int("".join(filter(str.isdigit, bestKey)))
    mat = bestValue["currentMat"]
    label = bestValue["label"]
    closeList.append(label)

    yIdx, xIdx = np.argwhere(mat == 0)[0]
    yAroundIdx = [(0, xIdx), (2, xIdx)] if yIdx == 1 else [(1, xIdx)]
    xAroundIdx = [(yIdx, 0), (yIdx, 2)] if xIdx == 1 else [(yIdx, 1)]
    availableIdx = yAroundIdx + xAroundIdx
    for idx in availableIdx:
        newMat = mat.copy()
        newMat[yIdx][xIdx], newMat[idx[0]][idx[1]] = (
            newMat[idx[0]][idx[1]],
            newMat[yIdx][xIdx],
        )
        totalCost = calCost(matDepth + 1, newMat, targetMat)
        newLabel = createNewLabel(openList, matDepth + 1)
        openList["Depth {}".format(newLabel)] = {
            "currentMat": newMat,
            "costScore": totalCost,
            "label": newLabel,
            "fatherStatus": label,
        }
        if np.all(newMat == targetMat):
            stopFlag = True
            closeList.append(newLabel)
    return openList, closeList, stopFlag


def aStarSearchAlgorithm(originalMat, targetMat):
    """估价函数定义为:f(n) = d(n) + w(n), 其中d(n)表示为状态的深
    度以步为代价; w(n)表示为两节点的曼哈顿距离|dx - nx|+|dy - ny|."""
    openList = dict()
    closeList = list()
    stopFlag = False
    openList["Depth A0"] = {
        "currentMat": originalMat,
        "costScore": 1e3,
        "label": "A0",
        "fatherStatus": None,
    }
    while not stopFlag:
        openList, closeList, stopFlag = createPossibleStatus(
            openList, closeList, stopFlag, targetMat
        )
    print("Moving Start!\n--------------")
    for element in closeList:
        print(openList["Depth {}".format(element)]["currentMat"])
    print("--------------\nMoving end!")


# ==================main===============================

timeStart = time.time()

arr1 = np.array([[8, 5, 2], [3, 6, 1], [4, 7, 0]])
arr2 = np.array([[4, 3, 5], [8, 1, 6], [7, 2, 0]])
print(f"初始状态:\n{arr1}\n目标状态:\n{arr2}")
print("=====================开始求解============================")

aStarSearchAlgorithm(arr1, arr2)
print("A*求解8数码问题计算时间 = {} (s)".format(time.time() - timeStart))

```



### 5.实验分析与结果：

#### 实验结果：

<img src="A*%E5%85%AB%E6%95%B0%E7%A0%81.assets/%E6%88%AA%E5%B1%8F2022-06-07%2023.16.08.png" alt="截屏2022-06-07 23.16.08" style="zoom:27%;" />

<center>8数码初始状态和目标状态<center>

<img src="A*%E5%85%AB%E6%95%B0%E7%A0%81.assets/%E6%88%AA%E5%B1%8F2022-06-07%2023.16.19-4661016.png" alt="截屏2022-06-07 23.16.19" style="zoom:30%;" />

<center>8数码问题求解的中间过程和运行时间<center>

#### 结果分析：

​		通过矩阵的形式给出了八数码的状态，并且输出了求解过程中的每一步中间过程，能够可视化的看到每一步是怎么移动求解八数码问题。给出了8数码问题的求解时间，还是比较快速能收敛的。

### 6.实验心得：

​		首先就是在编程过程中发现有时候陷入了死循环，debug了很久后发现不是语法错误，而是我们的算法存在问题，即对于8数码问题，有时候是无解的，这就导致了死循环的发生。了解到了这个，我重新审视了8数码问题，其实不难发现，如果我们交换两个数码，那么如果原问题有解，那么新问题是无解的，反之亦然。那么我根据数学推导，我们可以得到如下的结论：计算这两个有序数列的逆序值，如果两者都是偶数或奇数，则可通过变换到达，否则，这两个状态不可达。通过首先判断8数码问题可不可解来避免程序死循环。

> 注：871526340这个排列的，Y=0+0+0+1+1+3+2+3+0=10，10是偶数，所以他偶排列。
>
> ​		871625340，Y=0+0+0+1+1+2+2+3+0=9，9是奇数，所以他奇排列。

​		再就是对曼哈顿距离的理解，因为8数码问题智能上下左右移动，所以我们用w(n)表示为两节点的曼哈顿距离|dx - nx|+|dy - ny｜，我们可以这么编写python代码计算两点之间的曼哈顿距离：

```python
import numpy as np

x1=[1,2]
x2=[5,6]
x1_np = np.array(x1)
x2_np = np.array(x2)

dist3 = np.sum(np.abs(x1_np-x2_np))
print(f"d3={dist3}\n")
```

​		在本次实验中需要注意的是如何利用好启发式的信息，以估价函数作为评定指标，体会启发式搜索相比于盲目搜索的优点。

### 7.改进点：

​		1.可以设置一个选项让用户自行选择是使用深度优先搜索还是宽度优先搜索，因为两种搜索模式的应用场景不同。

​		2.可以再写一个随机生成8数码问题的函数，实现端到端的测试过程。



















