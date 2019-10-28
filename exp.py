class Expr(object): # 上位クラス
    def eval(self): pass

def expr(e):
    if not isinstance(e, Expr):
        e = Val(e)
    return e

class Binary(Expr):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def eval(self): # ここに何書けばよい???????
        pass

    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left}, {self.right})'

class Val(Expr): #Exprから継承されたクラス
    __slots__ = ['value']
    def __init__(self, v = 0):
        self.value = v

    def eval(self):
        return self.value

    def __repr__(self):
        return f'Val({self.value})'

class Add(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right) #この2つは式として渡される
    
    def eval(self):
        return self.left.eval() + self.right.eval() # 元々式の値として渡し、ここで評価するようにする

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



    
#Val
e = Val(1)
assert e.eval() == 1
print(e.eval())
assert isinstance(e, Expr) # 値の種類を判定 True
assert isinstance(e, Val) # True
# assert isinstance(e, int) # false

#Add
v = Add(Val(1), Val(2))
assert v.eval() == 3
print(v.eval())
# e = Add(1, Add(2, 3)) # これだとうまくいかない　self.rightに式が入ってしまうため
e = Add(Val(1), Add(Val(2), Val(3)))
print(e.eval())

#Mul
e = Mul(Val(1), Val(2))
assert e.eval() == 2
print(e.eval())

#Sub
e = Sub(Val(1), Val(2))
assert e.eval() == -1
print(e.eval())

#Div
e = Div(Val(7), Val(2))
assert e.eval() == 3
print(e.eval())

#class継承
assert isinstance(Val(1), Expr)
assert isinstance(Div(Val(7), Val(2)), Expr)

#シンプルに
e = Mul(Add(1, 2), 3)
assert e.eval() == 9
print(e.eval())

