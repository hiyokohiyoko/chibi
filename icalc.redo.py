import pegpy.tpeg as pegpy
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)

class Expr(object): # 上位クラス
    def eval(self): pass # 下位クラスに共通のメソッド　定義の内容は下位クラスごとに違うのでここでは定義しない

def expr(e): #Expr(式)クラスであるかどうか判定する関数
    if not isinstance(e, Expr):
        e = Val(e)
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
        return self.left.eval() / self.right.eval()


def conv(t):
    print(repr(t))
    return Val(0)

def run(s: str):
    tree = parser(s)
    e = conv(tree)
    print(e)
    print(e.eval())

def main():
    s = input('>>>')
    run(s)

if __name__ == '__main__':
    main()