num=1;
den=conv([1 2 2 0],[1 6 13]);
sys=tf(num,den);              
rlocus(sys);          %绘制系统的根轨迹
grid
hold on;
[k,r]=rlocfind(sys)       %确定临界稳定时的增益值k和对应的极点r 
sys_c=feedback(sys,1);    %形成单位负反馈闭环系统
xlabel('Real Axis');
ylabel('Imaginary Axis') ;  %给坐标轴加上说明
title('Root Locus');         %给图形加上标
figure(2)
step(sys_c)            %绘制闭环系统的阶跃响应曲线