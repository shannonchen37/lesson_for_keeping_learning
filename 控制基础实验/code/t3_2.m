num=[1,1];  
den=[0.1  1  0  0];
sys=tf(num,den);
[gm,pm,wcg,wcp]=margin(sys)
nyquist(sys)