%系统零输入响应

close all;clear;clc;
%系数向量
a=[3,0.5,-0.1];
b=[1,1,0];
figure(1)
impz(b,a,-3:10);    %时间范围内做图
title('单位脉冲响应');

%零输入响应
k=0:15;     %时间范围
x=2.^k;     %输入序列表达式
%x=(0.5).^k;     %输入序列表达式
y=filter(b,a,x);    %filter()滤波器函数，使得波形平滑
figure(2)
subplot(2,1,1);
stem(k,x)
title('输入序列')
subplot(2,1,2);
stem(k,y)
title('输出序列')