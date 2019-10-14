import math

class Q(object):
    def  __init__(self, a, b = 1): #引数を渡す インスタンス化の時に呼ばれる bの初期値を書いておくと省略可能
        gcd = math.gcd(a, b)
        self.a = a//gcd  #引数は必ずself (Java, C等はthisを使う)
        self.b = b//gcd

    def __repr__(self): #__(  )__ で表記されるメソッドは元々意味が決まっている　reprはそのオブジェクトの中身を文字列として表示する print(object)で呼び出せる
        if self.b == 1:
            return str(self.a)
        else:
            return f"{self.a}/{self.b}" #要復習!
    
    def __add__(self, q): # __add__で「＋」を用いた糖衣記法に対応可能
        if isinstance(q, Q):
            a = self.a * q.b + self.b * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a + self.b * q
            b = self.b
            return Q(a, b)

    def __sub__(self, q):
        if isinstance(q, Q):
            a = self.a * q.b + self.b * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a - self.b * q
            b = self.b
            return Q(a, b)

    def __mul__(self, q):
        if isinstance(q, Q):
            a = self.a * q.b + self.b * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a * q
            b = self.b
            return Q(a, b)

    def __truediv__(self, q):
        if isinstance(q, Q):
            a = self.a * q.b + self.b * q.a
            b = self.b * q.b
            return Q(a, b)
        else:
            a = self.a
            b = self.b * q
            return Q(a, b)
    

q = Q(1, 2)
print(q)

q = Q(2, 4)
print(q)

q = Q(3)
print(q)

q1 = Q(1, 2)
q2 = Q(1, 3)
# print(q1.add(q2)) # = 5/6
print(q1 + q2) #糖衣構文 5/6
print(q1 - q2) # 1/6
print(q1 * q2) # 1/6
print(q1 / q2) # 3/2

print(q1 / 2)


