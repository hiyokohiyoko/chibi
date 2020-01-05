import pegpy
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)

class Expr(object): # 上位クラス
    def eval(self): pass # 下位クラスに共通のメソッド　定義の内容は下位クラスごとに違うのでここでは定義しない
    
def expr(e): #Expr(式)クラスであるかどうか判定する関数
    if not isinstance(e, Expr):
        e = Val(e)
    return e

class Var(Expr):
    __slots__ = ['name']
    def __init__(self, s: str):
        self.name = s
    def __repr__(self):
        return self.name
    def eval(self, env: dict):
        if self.name in env:
            return env[self.name]
        else:
            raise NameError(self.name)

class Assign(Expr):
    __slots__ = ['name', 'expr']
    def __init__(self, s: str, ex: Expr):
        self.name = s
        self.expr = expr(ex)

    def eval(self, env: dict):
        env[self.name] = self.expr.eval(env)
        return env[self.name]

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

class Block(Expr):
    __slots__ = ['exprs']
    def __init__ (self, *exprs):
        self.exprs = exprs

    def eval(self, env):
        for e in self.exprs:  # 逐次処理の本質的な部分はここ
            e.eval(env)

class If(Expr):
    __slots__ = ['cond', 'then', 'else_']
    def __init__ (self, cond, then, else_):
        self.cond = cond
        self.then = then
        self.else_ = else_
    
    def eval(self, env):
        if self.cond.eval(env) != 0:
            return self.then.eval(env)
        else:
            return self.else_.eval(env)

class While(Expr):
    __slots__ = ['cond', 'body_']
    def __init__ (self, cond, body_):
        self.cond = cond
        self.body_ = body_

    def eval(self, env):
        while self.cond.eval(env) != 0:
            try:
                self.body_.eval(env)
            except ValueError:
                break

class Break(Expr):
    def eval(self, env):
        raise ValueError

class Lambda(Expr):
    __slots__ = ['name', 'body']
    def __init__ (self, name: str, body: Expr):
        self.name = name
        self.body = body
    def __repr__ (self):
        return f'λ{self.name} . {str(self.body)}'
    def eval(self, env):
        return self.body

class FunkApp(Expr):
    __slots__ = ['func', 'param'] # funcはλ式
    def __init__ (self, func: Expr, param: Expr):
        self.func = func
        self.param = param
    def eval (self, env):
        f = self.func.eval(env)
        p = self.param.eval(env)
        env[self.name] = p # 正格評価
        return f.body.eval(env)

def copy(env):
    localenv = {}
    for x in env.keys():
        localenv[x] = env[x]
    return localenv

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
    if t.tag == 'Eq':
        return Eq(conv(t[0]), conv(t[1]))
    if t.tag == 'Ne':
        return Ne(conv(t[0]), conv(t[1]))
    if t.tag == 'Lt':
        return Lt(conv(t[0]), conv(t[1]))
    if t.tag == 'Lte':
        return Lte(conv(t[0]), conv(t[1]))
    if t.tag == 'Gt':
        return Gt(conv(t[0]), conv(t[1]))
    if t.tag == 'Gte':
        return Gte(conv(t[0]), conv(t[1]))
    if t.tag == 'Var':
        return Var(str(t))
    if t.tag == 'LetDecl':
        return Assign(str(t[0]), conv(t[1]))
    if t.tag == 'If':
        return If(conv(t[0]), conv(t[1]), conv(t[2]))
    if t.tag == 'While':
        return While(conv(t[0]), conv(t[1]))
    return Val(str(t))


def run(s: str, env: dict):
    tree = parser(s)
    if tree.isError():
        print('Error')
    else:  # 解析が可能な場合
        e = conv(tree)
        print(repr(e))
        print('env', env)
        print(e.eval(env))

def main():
    try:
        env = {}
        while True:
            s = input('>>> ')
            if s == '':
                break
            run(s, env)
    except EOFError:
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

# added Var
e = Var('x')
assert e.eval({'x':1}) == 1

# added Assign
env = {}
e = Assign('x', Val(1))
assert e.eval(env) == 1

# Block
e = Block(
    Assign('x', Val(1)),
    Assign('x', Add(Var('x'), Val(1))),
    #Var('x')
)
# assert e.eval({}) == 2

# If
e = Block(
    Assign('x', 2),
    Assign('y', 1),
    If(Gt(Var('x'), Var('y')), Var('x'), Var('y'))
)
# assert e.eval({}) == 2

# While
e = Block(
    Assign('x', Val(0)),
    While(Lt(Var('x'), Val(10)),
        Assign('x', Add(Var('x'), Val(1))) ),
    Var('x')
)
# assert e.eval({}) == 10

# Break
e = Block(
    Assign('x', Val(0)),
    While(Lt(Var('x'), Val(10)),
        If(Eq(Var('x'), Val(5)),
            Break(),
            Assign('x', Add(Var('x'), Val(1))))
    ),
    Var('x')
)
# assert e.eval({}) == 5
print(e.eval({}))