%绘制信号幅度频谱
close all;clear;clc;
syms t v w x;       %定义变量

%表示题目所给的表达式
% heaviside(x)函数表示阶跃函数 returns the value 0 for x < 0, 1 for x > 0, and 1/2 for x = 0.
% x=1/2*exp(-1*t)*sym('heaviside(t)');    %例题中的表达式
x=sym(1/2*exp(-1*t)*heaviside(t-1));    %题目修改后的表达式,matlab版本太高，去掉单引号

%傅立叶变化
F = fourier(x);

%绘制原信号波形
subplot(2,1,1);
ezplot(x);     %用ezplot绘制函数，可用fplot代替，matlab版本太高，去掉单引号
%fplot(x);

%绘制傅立叶变化之后的波形
subplot(2,1,2);
ezplot(abs(F));     %用ezplot绘制函数，可用fplot代替，matlab版本太高，去掉单引号
%fplot('abs(F)');