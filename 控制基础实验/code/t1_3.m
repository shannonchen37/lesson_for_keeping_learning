%直接求根判稳
roots([2,1,3,5,10])

%劳斯稳定判据
syms EPS    %定义符号
den=[2,1,3,5,10]; 
ra=routh(den,EPS)