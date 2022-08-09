
clear;clc;close all;
T=readtable('体测成绩');
T1=T(:,{'class','height'});
Tongji=grpstats(T1,'class',{'mean','std','max','min'})
T2=T(:,{'height','weight','VC','score1','score2','score3'});
C=corrcoef(table2array(T2))
%相关系数矩阵第i行第j列是原矩阵中，第i列与第j列的相关系数

