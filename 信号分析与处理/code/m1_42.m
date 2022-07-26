%求信号的频谱傅立叶反变化,给出表达式
close all;clear;clc;
syms t w a;     %定义变量
Fw = sym(2*a/(w^2+a^2));    %题目表达式
ft=ifourier(Fw,w,t)    %傅立叶反变化