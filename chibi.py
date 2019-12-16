
import pegpy

#from pegpy.tpeg import ParseTree
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)

'''
tree = parser('1+2*3')
print(repr(tree))
tree = parser('1@2*3')
print(repr(tree))
'''


class Expr(object):
    @classmethod  # クラスのメソッド
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
    def eval(self, env: dict):    #引数に変数の集合とそれに対応する値の集合(=環境)をとる。　環境envは変数が値をローカルに、可変量として保持している状態の辞書である
        return self.value

#e = Val(0)
#assert e.eval({}) == 0

class Binary(Expr):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = Expr.new(left)
        self.right = Expr.new(right)
    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left},{self.right})'

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

class Var(Expr):  #変数を環境を用いて保持するクラス
    __slots__ = ['name']  #slotsは複数形です。
    def __init__(self, name: str):
        self.name = name
    def __repr(self):
        return self.name
    def eval(self, env: dict):
        if self.name in env:
            return env[self.name]
        # return 0 #キーが辞書になかったら初期値0を返すようにする
        else:
            raise NameError(self.name) #エラー発見をしやすくするためにはエラー報告をさせるほうが望ましい

class Assign(Expr): #変数への値の代入を行うクラス
    __slots__ = ['name', 'e']
    def __init__(self, name: str, e):
        self.name = name
        self.e = Expr.new(e) # classmethodを使用　Expr型でない場合はExpr型に変換
    def eval(self, env):
        env[self.name] = self.e.eval(env) #ここ循環定義にならないのなぜだろう?
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
    
'''
# Varクラスのテスト
try:
    e = Var('x')
    print(e.eval({'x': 123})) #ここで辞書を作っている
    print(e.eval({})) #辞書が定義されていないので(エラー対策をしていないと)キーエラーになる
except NameError:
    print("未定義の変数です")

# Assignクラスのテスト
env = {}
e = Assign('x', Val(1)) # x = 1
print(e.eval(env)) # 1
e = Assign('x', Add(Var('x'), Val(2))) # x = x + 2
print(e.eval(env)) # 3
'''

# lambda式
class Lambda(Expr):
    __slots__ = ['name', 'body']
    def __init__(self, name, body):
        self.name = name
        self.body = body
    def __repr__(self):
        return f'λ{self.name} . {str(self.body)}'
    def eval(self, env):
        return self

def copy(env): #環境をコピーする関数
    newenv = {}
    for x in env.keys():
        newenv[x] = env[x]
    return newenv


# 確認
f = Lambda('x', Add(Var('x'), 1)) # λx.x+1
print(repr(f))

class FuncApp(Expr):
    __slots__ = ['func', 'param']
    def __init__(self, func: Lambda, param):
        self.func = func
        self.param = Expr.new(param)
    def __repr__(self):
        return f'({repr(self.func)}) ({repr(self.param)})' # ここ循環定義にならないのか?

    def eval(self, env): #環境を書き換えて評価する
        f = self.func.eval(env)
        v = self.param.eval(env) # パラメータを先に評価する
        name = f.name # Lambda classの変数名をもらう
        env = copy(env) # 環境をコピーすることでローカルスコープを作る
        env[name] = v # コピーして作られたローカルな環境において、変数名にパラメータの値を代入する
        return f.body.eval(env) # パラメータの値を式に代入して値を返す


def conv(tree):
    if tree == 'Block':
        return conv(tree[0])
    if tree == 'FuncDecl': # Lambda式の時に追加
        return Assign(str(tree[0]), Lambda(str(tree[1]), conv(tree[2])))
    if tree == 'FuncApp':
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
        return Assign(str(tree[0]), conv(tree[1])) # 変数への代入を行う場合

    print('@TODO', tree.tag, repr(tree))
    return Val(str(tree))


def run(src: str, env: dict): #構文木からVar, Assign式に変換できるようにする
    tree = parser(src)
    if tree.isError():
        print(repr(tree))
    else:
        e = conv(tree)
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