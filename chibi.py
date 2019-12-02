
import pegpy

#from pegpy.tpeg import ParseTree
peg = pegpy.grammar('''
Expression = Product (^{ '+' Product #Add})*
Product = Value (^{ '*' Value #Mul})*
Value = { [0-9]+ #Int }
''')
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

class Var(Expr):  #変数を環境を用いて保持するクラス
    __slots__ = ['name']  #複数形です。
    def __init__(self, name: str):
        self.name = name
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        # return 0 #キーが辞書になかったら初期値0を返すようにする
        raise NameError(self.name) #エラー発見をしやすくするためにはエラー報告をさせるほうが望ましい

class Assign(Expr): #変数への値の代入を行うクラス
    __slots__ = ['name', 'expr']
    def __init__(self, name: str, e):
        self.name = name
        self.e = Expr.new(e) # classmethodを使用　Expr型でない場合はExpr型に変換
    def eval(self, env):
        env[self.name] = self.e.eval(env) #ここ循環定義にならないのなぜだろう?
        return env[self.name]
    

# Varクラスのテスト
try:
    e = Var('x')
    print(e.eval({'x': 123})) #ここで辞書を作っている
    print(e.eval({})) #辞書が定義されていないので(エラー対策をしていないと)キーエラーになる
except NameError:
    print("未定義の変数です")

# 変数への値の代入
env = {}
e = Assign('x', Val(1)) # x = 1
print(e.eval(env)) # 1
e = Assign('x', Add(Var('x'), Val(2))) # x = x + 2
print(e.eval(env)) # 3


def conv(tree):
    if tree == 'Block':
        return conv(tree[0])
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

    print('@TODO', tree.tag)
    return Val(str(tree))


def run(src: str):
    tree = parser(src)
    if tree.isError():
        print(repr(tree))
    else:
        e = conv(tree)
        print(repr(e))
        print(e.eval({}))
def main():
    try:
        while True:
            s = input('>>> ')
            if s == '':
                break
            run(s)
    except EOFError:
        return
if __name__ == '__main__':
    main()