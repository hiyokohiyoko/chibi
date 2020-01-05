import pegpy
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)

class Expr(object):
    @classmethod
    def new(cls, v):
        if isinstance(v, Expr):
            return v
        return Val(v)

class Val(Expr):
    __slots__ = ['value']
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Val({self.value})'

    def eval(self, env: dict):
        return self.value

class Binary(Expr):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = Expr.new(left)
        self.right = Expr.new(right)
    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left}, {self.right})'

class Add(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) + self.right.eval(env)
class Sub(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) - self.right.eval(env)
class Mul(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) * self.right.eval(env)
class Div(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) // self.right.eval(env)
class Mod(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) % self.right.eval(env)
class Eq(Binary): # left == right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):   # cond ? x : y
        return 1 if self.left.eval(env) == self.right.eval(env) else 0
class Ne(Binary): # left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):   # cond ? x : y
        return 1 if self.left.eval(env) != self.right.eval(env) else 0
class Lt(Binary): # left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):   # cond ? x : y
        return 1 if self.left.eval(env) < self.right.eval(env) else 0
class Lte(Binary): # left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):   # cond ? x : y
        return 1 if self.left.eval(env) <= self.right.eval(env) else 0
class Gt(Binary): # left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):   # cond ? x : y
        return 1 if self.left.eval(env) > self.right.eval(env) else 0
class Gte(Binary): # left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):   # cond ? x : y
        return 1 if self.left.eval(env) >= self.right.eval(env) else 0

class Var(Expr):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def eval(self, env: dict):
        if self.name in env:
            return env[self.name]
        raise NameError(self.name)

class Assign(Expr):
    __slots__ = ['name', 'e']
    def __init__(self, name, e):
        self.name = name
        self.e = Expr.new(e)

    def eval(self, env):
        env[self.name] = self.e.eval(env)
        return env[self.name]

class Block(Expr):
    __slots__ = ['exprs']
    def __init__(self, *exprs): # 可変長個の引数
        self.exprs = exprs  # [e, e2, e3, e4, e5] リストになっている
    
    def eval(self, env):
        for e in self.exprs:
            e.eval(env)

class While(Expr):
    __slots__ = ['cond', 'body']
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def eval(self, env):
        while self.cond.eval(env) != 0:
            self.body.eval(env)

class If(Expr):
    __slots__ = ['cond', 'then', 'else_']
    def __init__(self, cond, then, else_ ):
        self.cond = cond
        self.then = then
        self.else_ = else_
    
    def eval(self, env):
        yesorno = self.cond.eval(env)
        if yesorno == 1:
            return self.then.eval(env)
        else:
            return self.else_.eval(env)
class Lambda(Expr):
    __slots__ = ['name', 'body']
    def __init__(self, name, body):
        self.name = name
        self.body = body
    def __repr__(self):
        return f'λ{self.name} . {str(self.body)}'
    def eval(self, env):
        return self

def copy(env): #環境をコピーすることでローカルスコープを作る
    newenv = {}
    for x in env.keys():
        newenv[x] = env[x]
    return newenv

class FuncApp(Expr):
    __slots__ = ['func', 'param']
    def __init__(self, func: Lambda, param):
        self.func = func
        self.param = Expr.new(param)
    def __repr__(self):
        return f'({repr(self.func)}) ({repr(self.param)})'
    def eval(self, env):
        f = self.func.eval(env)
        v = self.param.eval(env)  # パラメータを先に評価する
        name = f.name # Lambda の変数名をとる
        env = copy(env)  # 環境をコピーすることでローカルスコープを作る
        env[name] = v   # 環境から引数を渡す
        return f.body.eval(env)

def conv(tree):
    if tree == 'Block':
        return conv(tree[0])
    if tree == 'FuncDecl':   # この２行を追加します
        return Assign(str(tree[0]), Lambda(str(tree[1]), conv(tree[2])))
    if tree == 'FuncApp':   # この２行を追加します
        return FuncApp(conv(tree[0]), conv(tree[1]))
    if tree == 'If':
        return If(conv(tree[0]), conv(tree[1]), conv(tree[2]))
    if tree == 'While':
        return While(conv(tree[0]), conv(tree[1]))
    if tree == 'Val' or tree == 'Int':
        return Val(int(str(tree)))
    if tree == 'Add':
        return Add(conv(tree[0]), conv(tree[1]))
    if tree == 'Sub':
        return Sub(conv(tree[0]), conv(tree[1]))
    if tree == 'Mul':
        return Mul(conv(tree[0]), conv(tree[1]))
    if tree == 'Div':
        return Div(conv(tree[0]), conv(tree[1]))
    if tree == 'Mod':
        return Mod(conv(tree[0]), conv(tree[1]))
    if tree == 'Eq':
        return Eq(conv(tree[0]), conv(tree[1]))
    if tree == 'Ne':
        return Ne(conv(tree[0]), conv(tree[1]))
    if tree == 'Lt':
        return Lt(conv(tree[0]), conv(tree[1]))
    if tree == 'Lte':
        return Lte(conv(tree[0]), conv(tree[1]))
    if tree == 'Gt':
        return Gt(conv(tree[0]), conv(tree[1]))
    if tree == 'Gte':
        return Gte(conv(tree[0]), conv(tree[1]))
    if tree == 'Var':
        return Var(str(tree))
    if tree == 'LetDecl':
        return Assign(str(tree[0]), conv(tree[1]))
    print('@TODO', tree.tag, repr(tree))
    return Val(str(tree))

def run(src: str, env: dict):
    tree = parser(src)
    if tree.isError():
        print(repr(tree))
    else:
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

# Currying
env = {}
f = Lambda('x', Lambda('y', Add(Var('x'), Var('y'))))
e = FuncApp(FuncApp(f, Val(1)), Val(2))
# assert e.eval(env) == 3
