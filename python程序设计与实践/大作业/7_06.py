import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import xlrd
from collections import defaultdict

data=xlrd.open_workbook('python实验用名单.xls')
table=data.sheet_by_name('Sheet1')
location=table.col_values(4)[1:]
year_list=table.col_values(3)[1:]
#print(location)
Llist=[]
for place in location:
	if "省" in place:
		Llist.append(place[:-1])
	elif '市' in place:
		Llist.append(place[:-1])
	else:
		Llist.append(place)
while '' in Llist:
    Llist.remove('')
#print(Llist)

Llist_2012,Llist_2013,Llist_2014,Llist_2015,Llist_2016,Llist_2017,Llist_2018=[],[],[],[],[],[],[]
for i in range(len(Llist)):
	if year_list[i]==2012:
		Llist_2012.append(Llist[i])
	elif year_list[i]==2013:
		Llist_2013.append(Llist[i])
	elif year_list[i]==2014:
		Llist_2014.append(Llist[i])
	elif year_list[i]==2015:
		Llist_2015.append(Llist[i])
	elif year_list[i]==2016:
		Llist_2016.append(Llist[i])
	elif year_list[i]==2017:
		Llist_2017.append(Llist[i])
	else:
		Llist_2018.append(Llist[i])

Llist_num_2012 = defaultdict(int)
for i in range(len(Llist_2012)):
	Llist_num_2012[Llist_2012[i]] += 1
Llist_sort_2012 = sorted(Llist_num_2012.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2012)


Llist_num_2013 = defaultdict(int)
for i in range(len(Llist_2013)):
	Llist_num_2013[Llist_2013[i]] += 1
Llist_sort_2013 = sorted(Llist_num_2013.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2013)

Llist_num_2014 = defaultdict(int)
for i in range(len(Llist_2014)):
	Llist_num_2014[Llist_2014[i]] += 1
Llist_sort_2014 = sorted(Llist_num_2014.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2014)

Llist_num_2015 = defaultdict(int)
for i in range(len(Llist_2015)):
	Llist_num_2015[Llist_2015[i]] += 1
Llist_sort_2015 = sorted(Llist_num_2015.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2015)

Llist_num_2016 = defaultdict(int)
for i in range(len(Llist_2016)):
	Llist_num_2016[Llist_2016[i]] += 1
Llist_sort_2016 = sorted(Llist_num_2016.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2016)

Llist_num_2017 = defaultdict(int)
for i in range(len(Llist_2017)):
	Llist_num_2017[Llist_2017[i]] += 1
Llist_sort_2017 = sorted(Llist_num_2017.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2017)

Llist_num_2018 = defaultdict(int)
for i in range(len(Llist_2018)):
	Llist_num_2018[Llist_2018[i]] += 1
Llist_sort_2018 = sorted(Llist_num_2018.items(), key=lambda x:x[1], reverse=True)
print(Llist_sort_2018)


zhejiang=[0,0,0,0,0,0,0]
guizhou=[0,0,0,0,0,0,0]
henan=[0,0,0,0,0,0,0]
sichuan=[0,0,0,0,0,0,0]
hebei=[0,0,0,0,0,0,0]
for i in range(len(Llist_sort_2012)):
	if Llist_sort_2012[i][0]=='浙江':
		zhejiang[0]=Llist_sort_2012[i][1]
	elif Llist_sort_2012[i][0]=='贵州':
		guizhou[0]=Llist_sort_2012[i][1]
	elif Llist_sort_2012[i][0]=='河南':
		henan[0]=Llist_sort_2012[i][1]
	elif Llist_sort_2012[i][0]=='四川':
		sichuan[0]=Llist_sort_2012[i][1]
	elif Llist_sort_2012[i][0]=='河北':
		hebei[0]=Llist_sort_2012[i][1]

for i in range(len(Llist_sort_2013)):
	if Llist_sort_2013[i][0]=='浙江':
		zhejiang[1]=Llist_sort_2013[i][1]
	elif Llist_sort_2013[i][0]=='贵州':
		guizhou[1]=Llist_sort_2013[i][1]
	elif Llist_sort_2013[i][0]=='河南':
		henan[1]=Llist_sort_2013[i][1]
	elif Llist_sort_2013[i][0]=='四川':
		sichuan[1]=Llist_sort_2013[i][1]
	elif Llist_sort_2013[i][0]=='河北':
		hebei[1]=Llist_sort_2013[i][1]

for i in range(len(Llist_sort_2014)):
	if Llist_sort_2014[i][0]=='浙江':
		zhejiang[2]=Llist_sort_2014[i][1]
	elif Llist_sort_2014[i][0]=='贵州':
		guizhou[2]=Llist_sort_2014[i][1]
	elif Llist_sort_2014[i][0]=='河南':
		henan[2]=Llist_sort_2014[i][1]
	elif Llist_sort_2014[i][0]=='四川':
		sichuan[2]=Llist_sort_2014[i][1]
	elif Llist_sort_2014[i][0]=='河北':
		hebei[2]=Llist_sort_2014[i][1]

for i in range(len(Llist_sort_2015)):
	if Llist_sort_2015[i][0]=='浙江':
		zhejiang[3]=Llist_sort_2015[i][1]
	elif Llist_sort_2015[i][0]=='贵州':
		guizhou[3]=Llist_sort_2015[i][1]
	elif Llist_sort_2015[i][0]=='河南':
		henan[3]=Llist_sort_2015[i][1]
	elif Llist_sort_2015[i][0]=='四川':
		sichuan[3]=Llist_sort_2015[i][1]
	elif Llist_sort_2015[i][0]=='河北':
		hebei[3]=Llist_sort_2015[i][1]

for i in range(len(Llist_sort_2016)):
	if Llist_sort_2016[i][0]=='浙江':
		zhejiang[4]=Llist_sort_2016[i][1]
	elif Llist_sort_2016[i][0]=='贵州':
		guizhou[4]=Llist_sort_2016[i][1]
	elif Llist_sort_2016[i][0]=='河南':
		henan[4]=Llist_sort_2016[i][1]
	elif Llist_sort_2016[i][0]=='四川':
		sichuan[4]=Llist_sort_2016[i][1]
	elif Llist_sort_2016[i][0]=='河北':
		hebei[4]=Llist_sort_2016[i][1]

for i in range(len(Llist_sort_2017)):
	if Llist_sort_2017[i][0]=='浙江':
		zhejiang[5]=Llist_sort_2017[i][1]
	elif Llist_sort_2017[i][0]=='贵州':
		guizhou[5]=Llist_sort_2017[i][1]
	elif Llist_sort_2017[i][0]=='河南':
		henan[5]=Llist_sort_2017[i][1]
	elif Llist_sort_2017[i][0]=='四川':
		sichuan[5]=Llist_sort_2017[i][1]
	elif Llist_sort_2017[i][0]=='河北':
		hebei[5]=Llist_sort_2017[i][1]

for i in range(len(Llist_sort_2018)):
	if Llist_sort_2018[i][0]=='浙江':
		zhejiang[6]=Llist_sort_2018[i][1]
	elif Llist_sort_2018[i][0]=='贵州':
		guizhou[6]=Llist_sort_2018[i][1]
	elif Llist_sort_2018[i][0]=='河南':
		henan[6]=Llist_sort_2018[i][1]
	elif Llist_sort_2018[i][0]=='四川':
		sichuan[6]=Llist_sort_2018[i][1]
	elif Llist_sort_2018[i][0]=='河北':
		hebei[6]=Llist_sort_2018[i][1]

print(zhejiang)
print(guizhou)
print(henan)
print(sichuan)
print(hebei)

x=['2012级','2013级','2014级','2015级','2016级','2017级','2018级']
mpl.rcParams['font.sans-serif'] = ['SimHei'] 
plt.plot(x,zhejiang, color='green', label='浙江')
plt.plot(x,guizhou, color='red',label='贵州')
plt.plot(x,henan, color='blue',label='河南')
plt.plot(x,sichuan, color='#FFFF00',label='四川')
plt.plot(x,hebei, color='#FF00FF',label='河北')
plt.legend() 
plt.xlabel('年级') 
plt.ylabel('录取人数') 
plt.show()






