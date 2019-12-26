from exp import Val, Add, Sub, Mul, Div

def parse(s: str):
    pos = s.rfind("+") # +文字の位置を見つける
    if pos > 0:
        s1 = s[0:pos]
        s2 = s[pos+1:]
        return Add(parse(s1), parse(s2))

    pos = s.rfind("-") # -文字の位置を見つける
    if pos > 0:
        s1 = s[0:pos]
        s2 = s[pos+1:]
        return Sub(parse(s1), parse(s2))

    pos = s.rfind("*") # *文字の位置を見つける
    if pos > 0:
        s1 = s[0:pos]
        s2 = s[pos+1:]
        return Mul(parse(s1), parse(s2))

    pos = s.rfind("/") # /文字の位置を見つける
    if pos > 0:
        s1 = s[0:pos]
        s2 = s[pos+1:]
        return Div(parse(s1), parse(s2))
    
    num = int(s)
    return Val(num)


# output Val 
e = parse("1")
assert e.eval() == 1
print(e)
print()

#output binary Add
e = parse("1+2")
assert e.eval() == 3
print(e)
print()

#output Add
print(parse("1"))
print(parse("1+2"))
print(parse("1+2+3"))

f = parse("1+2+3")
assert f.eval() == 6
print()

#output Add, Mul
print(parse("1*2+3"))
print(parse("1+2*3"))

g = parse("1*2+3")
assert g.eval() == 5
h = parse("1+2*3")
assert h.eval() == 7

print()

#output Expr
e = parse("1-2-3")
print(e.eval())
assert e.eval() == -4
print(parse("1-9/3+6*2+4").eval()) # 14(+, *もrfind()にしないと正しい答えが出ない)
print(parse("1*4/2+8*3*2/12-6").eval()) # 0(全部rfind()にしても正しい答えが出ない)→Divを//から/にしたら解決
print()





