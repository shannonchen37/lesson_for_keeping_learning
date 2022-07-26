%两个矩形脉冲的卷积
%t1 t2 t3 分别表示f1 f2 f1和f2卷积的时间
close all;clear;clc;
tspan=0.01;  %采样间隔
t1=0:tspan:3.5; %时间向量
t1_len=length(t1);
t2=0:tspan:3.5;
t2_len=length(t2);
t3=0:tspan:(t1_len+t1_len-2)*tspan; %卷积

%生成题目所要求的两个信号(这里直接写成矩形信号的形式）
f1=[zeros(1,length([0:tspan:(1-0.01)])),3*ones(1,length([1:tspan:2])),zeros(1,length([2.01:tspan:3.5]))];
f2=[zeros(1,length([0:tspan:(1-0.01)])),1*ones(1,length([1:tspan:3])),zeros(1,length([3.01:tspan:3.5]))];

%两矩形信号进行卷积
w=conv(f1,f2);
w=w*tspan;

%绘制f1信号波形
subplot(3,1,1);
plot(t1,f1);
title('f1信号波形')
grid on;
xlabel('时间t/s');
axis([0 7 0 4]) %设置坐标范围

%绘制f2信号波形
subplot(3,1,2);
plot(t2,f2);
title('f2信号波形')
grid on;
xlabel('时间t/s');
axis([0 7 0 2]) %设置坐标范围

%绘制f1和f2卷积信号波形
subplot(3,1,3);
plot(t3,w);
title('f1和f2卷积信号波形')
grid on;
xlabel('时间t/s');
















