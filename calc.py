def calc(s):
    ss = s.split("+")
    n = len(ss)
    ans = 0
    for i in range(n):
        ans += int(ss[i])
    print(ans)

calc("1")
calc("1+2")
calc("1+2+3")