clear;clc;close all;
x=[0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1];
y=[-0.232  0.647  1.877  3.565  5.134  7.443  9.221 10.011  11.678  12.566   13.788];
scatter(x,y);
% legend('原始数据');
hold on;
y2=polyfit(x,y,2);
f2=polyval(y2,x);
plot(x,f2);
% legend('2次拟合曲线');
hold on;
y3=polyfit(x,y,3)
f3=polyval(y3,x);
plot(x,f3);
legend('原始数据','2次拟合曲线','3次拟合曲线');
grid on;