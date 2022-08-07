from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import xlrd

data=xlrd.open_workbook('python实验用名单.xls')
table=data.sheet_by_name('Sheet1')
name_list=table.col_values(0)[1:]
first_name = []
for name in name_list:
   if '·' in name:
      name1, name2 = name.split("·")
      first_name.append(name2)
   elif len(name) == 4:
      first_name.append(name[2:])
   else:
      first_name.append(name[1:])
#print(last_name)
first_name_list=str(first_name)
for ch in ",[]'《》，。：!‧「」『』〈〉；﹖.！ \n？":
   first_name_list = first_name_list.replace(ch, "")                  # 去掉文章的标点符号
letter_dict={}
for char in first_name_list:
    if char in letter_dict:
        letter_dict[char] = letter_dict[char]+1
    else:
        letter_dict[char] = 1
#print(letter_dict)
letter_sort = sorted(letter_dict.items(), key=lambda x:x[1], reverse=True)
#print(letter_sort)

total_c = len(letter_sort)   # 总长度
head_num = 10 
x = np.array(range(head_num))
y_c = []
xlabel_c = []
for tupe in letter_sort[0:head_num]:
    y_c.append(tupe[1])
    xlabel_c.append(tupe[0])

#print(y_c)
#print(x)
mpl.rcParams['font.sans-serif'] = ['SimHei'] #设置中文字体 
plt.figure(figsize=(40, 5), dpi=150)
plt.bar(x, y_c)
plt.xticks(x, xlabel_c)
for a, b in zip(x, y_c):
    plt.text(a-0.15, b+3, b)
plt.savefig("7_02.jpg")
plt.show()
