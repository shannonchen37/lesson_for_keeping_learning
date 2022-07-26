%离散信号翻转，注意有序列长度
%离散信号的反转可用fliplr()函数实现
close all;clear;clc;
n=0:8;  %定义序列长度
nn=n-4; %生成对称x轴坐标
%x=[zeros(1,4),1,2,0,0,3,];   %书中例子的信号
x=[zeros(1,4),1,3,0,0,2,];   %题目的信号
y=fliplr(x);

figure(1);  %打开画图1
subplot(2,1,1); 
stem(nn,x); %画出原信号的火柴梗图
axis([-5 5 0 4]);   %坐标轴范围
grid on;    

subplot(2,1,2); 
stem(nn,y); %画出反转信号的火柴梗图
axis([-5 5 0 4]);   %坐标轴范围
grid on;    



