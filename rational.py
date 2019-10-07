
class Q(object):
    def  __init__(self, a, b = 1): #引数を渡す bの初期値を書いておくと省略可能
        g = gcd(a, b)
        self.a = a #引数は必ずself
        self.b = b

    
    def __repr__(self): #__(  )__ で表記されるメソッドは元々意味が決まっている　reprはそのオブジェクトの中身を文字列として表示する print(object)で呼び出せる
        if self.b == 1:
            return str(self.a)
        else:
            return f"{self.a}/{self.b}" #要復習!
    
    def __add__(self, q): # __add__で「＋」を用いた糖衣記法に対応可能
        a = self.a * q.b + self.b * q.a
        b = self.b * q.b
        return Q(a, b)


def gcd(a, b):
    if b == 0:
        return a
    r = a % b
    gcd(b, r)

    
    
    
q = Q(1, 2)
print(q)

q = Q(2, 4)
print(q)

q = Q(3)
print(q)

q1 = Q(1, 2)
q2 = Q(1, 3)
# print(q1.add(q2)) # = 5/6
print(q1 + q2) #糖衣構文
