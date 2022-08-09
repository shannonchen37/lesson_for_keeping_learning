num=[10];
den=conv([5,-1,0,0],[1,5])
[z,p,k]=tf2zp(num,den);   % tf2zp将传递函数转换为零极点形式的一个转换函数，可求出零点、极点和增益 
p
nyquist(num,den)

figure(2)
w=logspace(-2,3,100);   %即在10-2和103之间，产生100个等距离的点p。
bode(num,den,w)
grid;

sys=tf(num,den)
sys_c=feedback(sys,1)
figure(3)
step(sys_c)            %绘制闭环系统的阶跃响应曲线
