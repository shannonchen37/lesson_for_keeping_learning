%设计切比雪夫滤波器
close all;clear;clc;
%[z,p,k]=cheb1ap(8,4);   %设置切比雪夫参数
[z,p,k]=cheb1ap(6,5);
[num,den]=zp2tf(z,p,k);
[H,W]=freqs(num,den);
%绘制整个滤波器幅频特性曲线
subplot(2,1,1);
plot(W,20*log10(abs(H)));
xlabel('模拟频率/(rad/s)');
ylabel('幅值/dB');
title('低通滤波器');
axis([0 10 -250 10]);
grid on;
%绘制放大的滤波器幅频特性曲线
subplot(2,1,2);
plot(W,20*log10(abs(H)));
xlabel('模拟频率/(rad/s)');
ylabel('幅值/dB');
title('低通滤波器通带放大');
axis([0 3 -10 10]);
grid on;
%输出系统函数
Hs=tf(num,den)
