import pegpy.tpeg as pegpy

#peg = pegpy.grammar('''
#Expression = Product (^{ '+' Product #Add})*
#Product = Value (^{ '*' Value #Mul})*
#Value = { [0-9]+ #Int }
#''') #"math.tpeg"ファイルで定義された文法を呼び出す
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)  #上記で呼び出した文法に基づいてパーサを生成する

'''
t = parser('1+2*3')
print(repr(t))

t = parser('@2') #Syntax Errorになってほしい
print(repr(t))
'''

#以下、run()を使う場合に必要になるExpr(式)クラスの定義をする

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

    def eval(self, env:dict):
        return self.value

# e = Val(0)
# assert e.eval({}) == 0

class Binary(Expr):
    __slot__ = ['left', 'right']

    def __init__(self, left, right):
        self.left = Expr.new(left)
        self.right = Expr.new(right)

    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left}, {self.right})'

class Add(Binary):
    __slot__ = ['left', 'right']

#以下、生成されたパーサが構文解析をした結果出力される解析構文木について、実際に計算して結果を表示する関数を作る

def calc(t):  #tは構文木
    if t == 'Int':
        return (int(str(t)))
    if t == 'Add':
        return calc(t[0]) + calc(t[1])
    if t == 'Mul':
        return calc(t[0]) * calc(t[1])  # 再帰的に定義
    print(f'TODO {t.tag}')  #まだできていないところは"TODO"と出る
    return 0

t = parser('1+2*3+4*5')
print(repr(t))
print(calc(t))


#以下、ターミナル画面で対話型のプログラムとして計算が実行できるようにする

def main():  #Main関数を作りたい
    while(True):
        s = input('$ ') # 入力プロンプト　''内の文字列は何でもよい
        if s == '':
            break
        #t = parser(s) #tは構文木
        #print(calc(t))  #以上2行は単純にcalc()を使う場合

        run(s) #式(Expr)に変換して評価する場合(@レポート)

def run(s: str):
    tree = parser(s) #構文木を生成
    ee = conv(tree) #構文木を式にする
    print(ee)
    print(ee.eval())

def conv(tree):
    pass

if __name__ == '__main__':  # >>>python icalc.py と打ち込んだら対話型のプログラムが開始されるようにする
    main()