from exp import Val, Add

def parse(s: str):
    pos = s.find("+") # +文字の位置を見つける
    if pos == -1:
        num = int(s)
        return Val(num)
    else:
        s1 = s[0:pos]
        s2 = s[pos+1:]
        return Add(Val(int(s1)), Val(int(s2)))


# output Val 
e = parse("1")
assert e.eval() == 1
print(e)

#output binary Add
e = parse("1+2")
assert e.eval() == 3
print(e)


