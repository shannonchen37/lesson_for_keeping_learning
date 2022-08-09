clear;clc;close all;
%任务1 a
% x=0:0.05:2*pi;
% y1=sin(x);
% y2=cos(x);
% subplot(1,2,1);
% plot(x,y1,'ro');
% title('sin(x)');
% hold on;
% plot(x,y1,'b-');
% subplot(1,2,2);
% plot(x,y2,'b*-');
% title('cos(x)');


%任务1 b
% t=0:0.05:2*pi;
% r=sin(2*t).*cos(2*t);
% polar(t,r,'r-');
% 

%任务1 c
% x=logspace(-1,2,50);
% y=exp(x);
% loglog(x,y,'b-');
% xlabel('X');
% ylabel('Y');
% grid;

%任务2
% [x,y]=meshgrid(-2:0.1:2,-2:0.1:2);
% z=x.^2+y.^2;
% subplot(2,2,1);
% mesh(x,y,z);
% title('mesh');
% subplot(2,2,2);
% surf(x,y,z);
% title('surf');
% subplot(2,2,3);
% meshc(x,y,z);
% title('meshc');
% subplot(2,2,4);
% meshz(x,y,z);
% title('surfz');
% 

