function sum = fun(x)
    sum = 0;
    for i=x
        if i<0
            continue;
        end
        sum=sum+i;
    end
end