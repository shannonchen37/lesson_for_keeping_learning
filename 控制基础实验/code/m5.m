x=linspace(0,4*pi,100);
y=sin(x);
z=cos(x);
plot(x,y,'r',x,z,'bo')
title('ÕıÏÒÓàÏÒº¯ÊıÍ¼Ïñ')
xlabel('0 < x < 2\pi') 
ylabel('Sine and Cosine Values')
legend({'y = sin(x)','y = cos(x)'},'Location','southwest')
text(pi,0,' \leftarrow ÕıÏÒ');
text(pi/2,0,' \leftarrow ÓàÏÒ');
grid on