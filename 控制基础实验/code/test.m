x=[3,2,1,0; 5 6 8 7]
b=size(x,1)
c=size(x,2)
d=size(x,3)  %%如果维度小于3则返回1
s=sum(x)
s2=sum(x(:))
