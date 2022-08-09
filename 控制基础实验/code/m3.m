clc;close all;clear;
A = rand([5 10])
B = A>0.48&A<0.52;
I = find(A>0.48 & A<0.52)
n = length(I)
A(B)
Sum = sum(A(B))