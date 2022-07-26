%利用频率变化，对已知冲激响应的系统输入，求输出

close all;clear;clc;
syms w t;   %定义w和t
h=10*t*exp(-2*t)*heaviside(t);   %heaviside()=u(t)
H=fourier(h);
[Hn,Hd]=numden(H);   %得到H的分子和分母
Hnum=abs(sym2poly(Hn));     %求得系数向量
Hden=abs(sym2poly(Hd));

%计算频率特性
[Hh,Hw]=freqs(Hnum,Hden,500);   
Hh1=abs(Hh);    %幅频特性
Hw1=angle(Hh);  %相频特性

%绘制系统的幅频特性和相频特性
subplot(2,1,1);
plot(Hw,Hh1);
grid on;
xlabel('角频率');
ylabel('幅度');
title('H(j)的幅频特性');
axis([0 10 0 3]);

subplot(2,1,2);
plot(Hw,Hw1*180/pi);
grid on;
xlabel('角频率');
ylabel('相位');
title('H(j)的相频特性');

%绘制输入响应
x=exp(-2*t)*heaviside(t);
X=fourier(x);
Y=X*H;      %频域相乘
y=ifourier(Y);   %傅立叶反变化
figure(2)
ezplot(y,[-4,20]);
axis([-2 10 0 1]);
grid on;
title('通过频域Y计算y');
xlabel('t');
ylabel('y(t)');
