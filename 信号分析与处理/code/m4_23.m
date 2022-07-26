%设计低通滤波器（切比雪夫）
close all;clear;clc;
%频率归一化
Wp=100/500;
Ws=200/500;
Rp=3;   %通带波纹
Rs=30;  %阻带衰减
[n,Wp]=cheb1ord(Wp,Ws,Rp,Rs);
[b,a]=cheby1(n,Rp,Wp);
[H,F]=freqz(b,a,512,1000);
plot(F,20*log10(abs(H)));
xlabel('频率/(rad/s)');
ylabel('幅值/dB');
title('数字低通滤波器');
axis([0 500 -200 20]);
grid on;
Hz=tf(b,1,1/1000,'Variable','z^-1')
