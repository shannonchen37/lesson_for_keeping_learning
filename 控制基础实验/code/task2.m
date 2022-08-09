%% 1)fenzutj
clc;close all;clear;
A=readtable('体测成绩.xls');
T=A(:,{'class','height'});
whichstats={'mean','std','min','max'};  %统计量
Tongji=grpstats(T,'class',whichstats)

T1=A(:,{'height','weight','VC','score1','score2','score3'});
T1=table2array(T1); %将excel表格转化为数组
corrcoef(T1)    %相关系数矩阵，统计两个随机变量之间线性相关程度
%% 2)NORMCANSHU
clc;close all;clear;
x=[15.14,14.81,15.11,15.26,15.08,15.17,15.12,14.95,15.05,14.87];
[mu,sigma,muci,sigmaci]=normfit(x,0.1)
%% 3)polyroots
clc;close all;clear;
a=[2 -6 3 0 7];
poly2sym(a)
r=roots(a)
p=polyval(a,1)
%% 4)dxsnihe
clc;close all;clear;
x=[0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1];
y=[-0.232  0.647  1.877  3.565  5.134  7.443 9.221 10.011  11.678  12.566   13.788];

p2=polyfit(x,y,2)
expression1=poly2sym(p2)
a2=polyval(p2,x)

p3=polyfit(x,y,3)
expression2=poly2sym(p3)
a3=polyval(p3,x)

plot(x,y,'o')
hold on;
plot(x,a2,'k','linewidth',2)
hold on;
plot(x,a3,'r','linewidth',2)
legend('原始数据', '二次拟合曲线', '三次拟合曲线')