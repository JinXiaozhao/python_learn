def yanghui(n):
    res = []
    for i in range(1,n+1):
        x = []
        if i == 1:
            x.append(1)
            res.append(x)
            continue
        x.append(1)
        for j in range(1,i-1):
            x.append(res[-1][j-1]+res[-1][j])
        x.append(1)
        res.append(x)
    return res
if __name__=='__main__':
    n = int(input('请输入N：\n'))
    y = yanghui(n)
    for i in y:
        print(*i)

