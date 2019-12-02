
import pegpy
#from pegpy.tpeg import ParseTree
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)
tree = parser('1+2*3')
print(repr(tree))
tree = parser('1@2*3')
print(repr(tree))
class Expr(object):
    @classmethod
    def new(cls, v):
        if isinstance(v, Expr):
            return v
        return Val(v)
class Val(Expr):
    __slot__ = ['value']
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Val({self.value})'
    def eval(self, env: dict):
        return self.value
e = Val(0)
assert e.eval({}) == 0
class Binary(Expr):
    __slot__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = Expr.new(left)
        self.right = Expr.new(right)
    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left},{self.right})'
class Add(Binary):
    __slot__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) + self.right.eval(env)
class Sub(Binary):
    __slot__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) - self.right.eval(env)
class Mul(Binary):
    __slot__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) * self.right.eval(env)
class Div(Binary):
    __slot__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) // self.right.eval(env)
class Mod(Binary):
    __slot__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) % self.right.eval(env)
def conv(tree):
    if tree == 'Block':
        return conv(tree[0])
    if tree == 'Val' or tree == 'Int':
        return Val(int(str(tree)))
    if tree == 'Add':
        return Add(conv(tree[0]), conv(tree[1]))
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