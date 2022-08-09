%% 任务一 a) sincos
clc;close all;clear;
t=0:0.1:2*pi;
subplot(1,2,1);
plot(t,sin(t),'ro');
hold on
plot(t,sin(t),'b');
grid on
title('sin(x)');

subplot(1,2,2);
plot(t,cos(t),'b*');
hold on
plot(t,cos(t),'b');
grid on
title('cos(x)');
%% 任务一 b) r=sin(2t)cos(2t)
clc;close all;clear;
theta=linspace(0,2*pi,1000);
r=sin(2*theta).*cos(2*theta);   %点乘，每个元素进行相乘
polar(theta,r,'r');
title('sin(2t)cos(2t)');
%% 任务一 c) y=exp(x)
clc;close all;clear;
t=logspace(-1,2,100);
loglog(t,exp(t),'b');
grid on;
xlabel('x');
ylabel('y');
title('exp(x)');
%% 任务二 三维绘图qiumian
[x,y]=meshgrid(-2:0.1:2,-2:0.1:2);%使用meshgrid得到带范围的二维网格
z=x.^2+y.^2;%按元素求幂
subplot(1,2,1);
mesh(x,y,z);
title('mesh  z=x^2+y^2');
subplot(1,2,2)
surf(x,y,z);
title('surf z=x^2+y^2');