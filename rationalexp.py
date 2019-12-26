# 有理数としての演算を可能にする

class Expr(object): # 上位クラス
    def eval(self): pass # 下位クラスに共通のメソッド　定義の内容は下位クラスごとに違うのでここでは定義しない

def expr(e): #Expr(式)クラスであるかどうか判定する関数
    if not isinstance(e, Expr):
        e = Val(e)
    return e

class Binary(Expr):
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def eval(self): pass # 定義の内容は下位クラスごとに違うのでここでは定義しない

    def __repr__(self):pass
        #classname = self.__class__.__name__
        #return f'{classname}({self.a}, {self.b})'

class Val(Expr): #Exprから継承されたクラス
    __slots__ = ['value']
    def __init__(self, v = 0):
        self.value = v

    def eval(self):
        return self.value

    def __repr__(self):
        return self.value

class Add(Binary):
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = expr(a)
        self.b = expr(b) #この2つは式として渡される

    def __repr__(self):
        aa = self.a.eval().a.eval() * self.b.eval().b.eval() + self.a.eval().b.eval() * self.b.eval().a.eval()
        bb = self.a.eval().b.eval() * self.b.eval().b.eval()
        return Div(aa, bb)
    
    def eval(self):
        aa = self.a.eval().a.eval() * self.b.eval().b.eval() + self.a.eval().b.eval() * self.b.eval().a.eval()
        bb = self.a.eval().b.eval() * self.b.eval().b.eval()
        return Div(aa, bb) # 元々式の値として渡し、ここで評価するようにする

    # reprは上位クラスBinaryで定義済

class Mul(Binary):
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = expr(a)
        self.b = expr(b)

    def __repr__(self):
        aa = self.a.eval().a.eval() * self.b.eval().a.eval()
        bb = self.a.eval().b.eval() * self.b.eval().b.eval()
        return Div(aa, bb)
    
    def eval(self):
        aa = self.a.eval().a.eval() * self.b.eval().a.eval()
        bb = self.a.eval().b.eval() * self.b.eval().b.eval()
        return Div(aa, bb)

class Sub(Binary):
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = expr(a)
        self.b = expr(b)

    def __repr__(self):
        aa = self.a.eval().a.eval() * self.b.eval().b.eval() - self.a.eval().b.eval() * self.b.eval().a.eval()
        bb = self.a.eval().b.eval() * self.b.eval().b.eval()
        return Div(aa, bb)
        
    def eval(self):
        aa = self.a.eval().a.eval() * self.b.eval().b.eval() - self.a.eval().b.eval() * self.b.eval().a.eval()
        bb = self.a.eval().b.eval() * self.b.eval().b.eval()
        return Div(aa, bb)

class Div(Binary):
    __slots__ = ['a', 'b']
    def __init__(self, a, b = 1):
        self.a = expr(a)
        self.b = expr(b)

    def __repr__(self):
        if self.a.eval().b.eval() == 1 and self.b.eval().b.eval() == 1:
           return Div(self.a.eval().a.eval(), self.b.eval().a.eval())
        else:
            aa = self.a.eval().a.eval() * self.b.eval().b.eval()
            bb = self.a.eval().b.eval() * self.b.eval().a.eval()
            return Div(aa, bb)
            
    def eval(self):
        if self.a.eval().b.eval() == 1 and self.b.eval().b.eval() == 1:
           return Div(self.a.eval().a.eval(), self.b.eval().a.eval())
        else:
            aa = self.a.eval().a.eval() * self.b.eval().b.eval()
            bb = self.a.eval().b.eval() * self.b.eval().a.eval()
            return Div(aa, bb)


#有理数表示 1/2 + 2/3
e = Add(Div(1, 2), Div(2, 3))
#assert e == Div(6, 7)
print(e)


