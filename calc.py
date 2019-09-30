def calc(s):
    ss = s.split("+")
    n = len(ss)
    ans = 0
    for i in range(n):
        t = ss[i]
        tt = t.split("*")
        m = len(tt)
        a = 1
        for j in range(m):
            a *= int(tt[j])
        ans += a
    print(ans)


calc("1*2+3")
calc("1+2*3")