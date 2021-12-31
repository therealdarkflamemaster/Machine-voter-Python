def premier(self,p,q):
    flag=1
    n=min(p,q)
    m=max(p,q)
    for i in range (2,n-1):
        if (n%i==0 && m%i==0):
            flag=0
            break
    return flag