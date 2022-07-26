% FFT 采样 幅度谱
close all;clear;clc;
k=16;   %采样频率
n1=[0:1:19];     %采样点20个
xa1=sin(2*pi*n1/k);

%绘制原始连续信号
figure(1);
subplot(1,2,1)
stem(n1,xa1)
xlabel('t/T');ylabel('x(n)');
title("20个采样点信号");

%{
xk1=fft(xa1);
xk1=abs(xk1);
subplot(1,2,2)
stem(n1,xk1)
xlabel('k');ylabel('X(k)');
title("20个采样点傅立叶幅值");
%}

n2=[0:1:15];
xa2=sin(2*pi*n2/k);
figure(2)
subplot(1,2,1)
stem(n2,xa2)
xlabel('t/T');ylabel('x(n)');
title("16个采样点信号");

%{
xk2=fft(xa1);
xk2=abs(xk2);
subplot(1,2,2)
stem(n1,xk2)
xlabel('k');ylabel('X(k)');
title("16个采样点傅立叶幅值");
%}



