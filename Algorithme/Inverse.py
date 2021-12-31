def inverse(a,p):
    x=a
    y=p
    n=int(x/y)
    m=a%p
    c1=0
    c2=1
    c=0
    while m>1:
        x=y
        y=m
        n=int(x/y)
        m=x%y
        c=c1-n*c2
        c1=c2
        c2=c
    if c<0:
        c=c+p
    return c