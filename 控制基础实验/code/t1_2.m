num1=[0   0   1]; 
den1=[1   0.5   1];
t=0:0.01:10;
step(num1,den1,t);
text(1,1.4,'wn=3')
hold on
num2=[0   0   9]; 
den2=[1   1.5  9];
num3=[0   0   36]; 
den3=[1  3  36];
step(num2,den2,t);
text (1,0.8,'wn=6')
step(num3,den3,t);
text (1,0.5,'wn=1')
grid
title('Impulse-Response Curves for G(s)=wn^2/[s^2+2(zeta)s+wn^2]')
