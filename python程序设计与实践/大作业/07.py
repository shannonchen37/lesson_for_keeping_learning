from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *

f=open('name.txt')
line = f.readline().strip() #读取第一行
txt=[]
txt.append(line)
while line:  # 直到读取完文件
   line = f.readline().strip()  # 读取一行文件，包括换行符
   txt.append(line)
f.close()  # 关闭文件
print(txt)
last_name = []
for name in txt:
   if '·' in name:
      name1, name2 = name.split("·")
      last_name.append(name1)
   elif len(name) == 4:
      last_name.append(name[:2])
   else:
      last_name.append(name[0:1])
#print(last_name)
last_num = defaultdict(int)
for i in range(len(last_name)):
   last_num[last_name[i]] += 1
last_sort = sorted(last_num.items(), key=lambda x:x[1], reverse=True)
#print(last_sort)
cnts=[]
total_cnt=0
for tupe in last_sort:
   cnts.append(tupe[1])
for i in cnts:
   total_cnt +=i
a=int((cnts[0]/total_cnt)*100)
b=int((cnts[1]/total_cnt)*100)
c=int((cnts[2]/total_cnt)*100)
d=int((cnts[3]/total_cnt)*100)
e=int((cnts[4]/total_cnt)*100)
others=100-a-b-c-d-e
labels = '王', '李', '张', '陈','刘','其他'
sizes = [a,b,c,d,e,others] #占比
colors = ['yellowgreen', 'gold', '#FF0000', 'lightcoral','#0000FF','#9F5887'] 
mpl.rcParams['font.sans-serif'] = ['SimHei'] #设置中文字体 
fig = plt.figure()
ax = fig.gca()
ax.pie(sizes, labels=labels, colors=colors,
   autopct='%1.1f%%', shadow=False, startangle=90,
   radius=0.4, center=(0.5, 0.5), frame=True) 
plt.show()
