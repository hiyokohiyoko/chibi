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

    def eval(self, env: dict):
        return self.value

    def __repr__(self):
        return f'Val({self.value})'

class Add(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right) #この2つは式として渡される
    
    def eval(self, env: dict):
        return self.left.eval(env) + self.right.eval(env) # 元々式の値として渡し、ここで評価するようにする

    # reprは上位クラスBinaryで定義済

class Mul(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return self.left.eval(env) * self.right.eval(env)

class Sub(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
        
    def eval(self, env: dict):
        return self.left.eval(env) - self.right.eval(env)

class Div(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
            
    def eval(self, env: dict):
        return self.left.eval(env) / self.right.eval(env)

class Mod(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
            
    def eval(self, env: dict):
        return self.left.eval(env) % self.right.eval(env)

class Eq(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return 1 if self.left.eval(env) == self.right.eval(env) else 0

class Ne(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return 1 if self.left.eval(env) != self.right.eval(env) else 0

class Lt(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return 1 if self.left.eval(env) < self.right.eval(env) else 0

class Lte(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return 1 if self.left.eval(env) <= self.right.eval(env) else 0

class Gt(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return 1 if self.left.eval(env) > self.right.eval(env) else 0

class Gte(Binary):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = expr(left)
        self.right = expr(right)
    
    def eval(self, env: dict):
        return 1 if self.left.eval(env) >= self.right.eval(env) else 0


def conv(t):
    #print(repr(t)) # 評価される前の構造木を表示
    if t.tag == 'Block':
        return conv(t[0])
    if t.tag == 'Int':
        return Val(int(str(t)))
    if t.tag == 'Add':
        return Add(conv(t[0]), conv(t[1]))
    if t.tag == 'Sub':
        return Sub(conv(t[0]), conv(t[1]))
    if t.tag == 'Mul':
        return Mul(conv(t[0]), conv(t[1]))
    if t.tag == 'Div':
        return Div(conv(t[0]), conv(t[1]))
    if t.tag == 'Mod':
        return Mod(conv(t[0]), conv(t[1]))
    return Val(str(t))

def run(s: str, env: dict):
    tree = parser(s)
    if tree.isError:
        print(repr(tree))
    else:  # 解析が可能な場合
        e = conv(tree)
        print(repr(e))
        print('env', env)
        print(e.eval(env))

def main():
    while True:
        env = {}
        s = input('>>>')
        if s == '':
            break
        run(s, env)
    return

if __name__ == '__main__':
    main()


# modified eval()
e = Mul(Val(1), Val(2))
assert e.eval({}) == 2

# added comere
e = Lt(Val(0), Val(1))
assert e.eval({}) == 1
e = Gt(Val(0), Val(1))
assert e.eval({}) == 0
