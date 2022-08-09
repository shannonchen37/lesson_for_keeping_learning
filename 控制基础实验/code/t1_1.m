num=[0   0   4]; 
den1=[1   0   4];
t=0:0.1:10;
step(num,den1,t);
text(1,1.7,'¦Æ=0')
hold on
den2=[1   2  4];
den3=[1  4  4];
step(num,den2,t);
text (1,0.8,'¦Æ=0.5')
step(num,den3,t);
text (1,0.5,'¦Æ=1')
grid
title('Impulse-Response Curves for G(s)=wn^2/[s^2+2(zeta)s+wn^2]')
