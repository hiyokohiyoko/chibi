# 有理数としての演算を可能にする

import math

class Expr(object):
    pass

class Q(Expr):
    def  __init__(self, a, b = 1): #引数を渡す インスタンス化の時に呼ばれる bの初期値を書いておくと省略可能
        gcd = math.gcd(a, b)
        self.a = a//gcd  #引数は必ずself (Java, C等はthisを使う)
        self.b = b//gcd

    def __repr__(self): #__(  )__ で表記されるメソッドは元々意味が決まっている　reprはそのオブジェクトの中身を文字列として表示する print(object)で呼び出せる
        if self.b == 1:
            return str(self.a)
        else:
            return f"{self.a}/{self.b}" #要復習!
    
    def __add__(self, q): # __add__で「＋」を用いた糖衣記法に対応可能
        if isinstance(q, Q):
            a = self.a * q.b + self.b * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a + self.b * q
            b = self.b
            return Q(a, b)

    def __sub__(self, q):
        if isinstance(q, Q):
            a = self.a * q.b - self.b * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a - self.b * q
            b = self.b
            return Q(a, b)

    def __mul__(self, q):
        if isinstance(q, Q):
            a = self.a * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a * q
            b = self.b
            return Q(a, b)

    def __truediv__(self, q):
        if isinstance(q, Q):
            a = self.a * q.b
            b = self.b * q.a
            return Q(a, b)
        else:
            a = self.a
            b = self.b * q
            return Q(a, b)

    def __eq__(self, q):
        if self.a == q.a and self.b == q.b:
            return True
        else:
            return False

    def eval(self):
        return self

class Binary(Q):
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def eval(self): pass # 定義の内容は下位クラスごとに違うのでここでは定義しない

    def __repr__(self):pass
        #classname = self.__class__.__name__
        #return f'{classname}({self.a}, {self.b})'

class Add(Binary):
    __slots__ = ['a', 'b']
    def eval(self):
        return self.a.eval() + self.b.eval()
    # reprは上位クラスBinaryで定義済
class Mul(Binary):
    __slots__ = ['a', 'b']
    def eval(self):
        return self.a.eval() * self.b.eval()
class Sub(Binary):
    __slots__ = ['a', 'b']
    def eval(self):
        return self.a.eval() - self.b.eval()
class Div(Binary):
    __slots__ = ['a', 'b']
    def eval(self):
        return self.a.eval() / self.b.eval()

#有理数表示 1/2 + 2/3
e = Add(Q(1, 2), Q(2, 3))
assert e == Q(7, 6)
#print(repr(e))


