from exp import Val, Add

def parse(s: str):
    num = int(s)
    return Val(num)


e = parse("1")
assert e.eval() == 1
print(e)

s = "123+456"
pos = s.find("+") # +文字の位置を見つける
print("pos", pos)

s1 = s[0:pos]
s2 = s[pos+1:]
print(s, s1, s2) #  +記号で分割

