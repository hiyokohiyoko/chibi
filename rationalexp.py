# 有理数版の計算機を作る
import math

class Expr(object): # 上位クラス
    def eval(self): pass # 下位クラスに共通のメソッド　定義の内容は下位クラスごとに違うのでここでは定義しない

def expr(e): #Expr(式)クラスであるかどうか判定する関数
    if not isinstance(e, Expr):
        e = Qval(e)
    return e

class Binary(Expr):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def eval(self): pass # 定義の内容は下位クラスごとに違うのでここでは定義しない

    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left}, {self.right})'

class Qval(Expr): #Exprから継承されたクラス
    __slots__ = ['a', 'b']
    def __init__(self, a, b = 1):
        gcd = math.gcd(a, b)
        self.a = a//gcd
        self.b = b//gcd

    def __repr__(self):
        if self.b == 1:
            return str(self.a)
        else:
            return f'{self.a}/{self.b}'

    def eval(self):
        return self.a/self.b


class Add(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right) #この2つは式として渡される
    
    def eval(self):
        return self.left.eval() + self.right.eval() # 元々式の値として渡し、ここで評価するようにする eQval()は中身の該当クラスのメソッド

    # reprは上位クラスBinaryで定義済

class Mul(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self):
        return self.left.eval() * self.right.eval()

class Sub(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
        
    def eval(self):
        return self.left.eval() - self.right.eval()

class Div(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
            
    def eval(self):
        return self.left.eval() // self.right.eval()



    
#val
e = Qval(1)
assert e.eval() == 1
print(e.eval())
assert isinstance(e, Expr) # 値の種類を判定 True
assert isinstance(e, Qval) # True
# assert isinstance(e, int) # false

e = Qval(1, 2)
assert e.eval() == 0.5
print(e.eval())

#Add
v = Add(Qval(1), Qval(2))
assert v.eval() == 3
print(v.eval())
# e = Add(1, Add(2, 3)) # これだとうまくいかない　self.rightに式が入ってしまうため
e = Add(Qval(1), Add(Qval(2), Qval(3)))
print(e.eval())

#Mul
e = Mul(Qval(1), Qval(2))
assert e.eval() == 2
print(e.eval())

#Sub
e = Sub(Qval(1), Qval(2))
assert e.eval() == -1
print(e.eval())

#Div
e = Div(Qval(7), Qval(2))
assert e.eval() == 3
print(e.eval())

#class継承
assert isinstance(Qval(1), Expr)
assert isinstance(Div(Qval(7), Qval(2)), Expr)

#シンプルに
e = Mul(Add(1, 2), 3)
assert e.eval() == 9
print(e.eval())

#分数表示
e = Mul(Add(Qval(1, 2), Qval(2, 3)), Qval(6, 7))
print(e.eval())

# 1/2 + 2/3
e = Add(Q(1, 2), Q(2, 3))

