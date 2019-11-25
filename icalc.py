import pegpy

peg = pegpy.grammar('''
Expression = Product (^{ '+' Product #Add})*
Product = Value (^{ '*' Value #Mul})*
Value = { [0-9]+ #Int }
''') #"math.tpeg"ファイルで定義された文法を呼び出す
parser = pegpy.generate(peg)  #上記で呼び出した文法に基づいてパーサを生成する

t = parser('1+2*3')
print(repr(t))

t = parser('@2') #Syntax Errorになってほしい
print(repr(t))

#以下、生成されたパーサが構文解析をした結果出力される解析構文木について、実際に計算して結果を表示する関数を作る

def calc(t):  #tは構文木
    if t == 'Int':
        return (int(str(t)))
    if t == 'Add':
        return calc(t[0]) + calc(t[1])
    if t == 'Mul':
        return calc(t[0]) * calc(t[1])  # 再帰的に定義
    print(f'TODO {t.tag}')
    return 0

t = parser('1+2*3+4*5')
print(repr(t))
print(calc(t))
