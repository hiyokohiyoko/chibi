from exp import Val, Add

def parse(s: str):
    pos = s.find("+") # +文字の位置を見つける
    if pos == -1:
        num = int(s)
        return Val(num)
    else:
        s1 = s[0:pos]
        s2 = s[pos+1:]
        return Add(parse(s1), parse(s2))


# output Val 
e = parse("1")
assert e.eval() == 1
print(e)

#output binary Add
e = parse("1+2")
assert e.eval() == 3
print(e)

#output Add
print(parse("1"))
print(parse("1+2"))
print(parse("1+2+3"))

f = parse("1+2+3")
assert f.eval() == 6


