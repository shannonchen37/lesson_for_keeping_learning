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
