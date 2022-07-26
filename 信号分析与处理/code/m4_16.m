% 巴特沃斯滤波器设计

close all;clear;clc;
Wn=400;     %设置通带截止频率
[b,a]=butter(3,Wn,'low','s');

[H,F]=freqs(b,a);
plot(F,20*log10(abs(H)));    %转化为对数的形式
xlabel('频率');
ylabel('幅值');
title('低通滤波器');
axis([0 800 -30 5]);
grid on;
Hs=tf(b,a)