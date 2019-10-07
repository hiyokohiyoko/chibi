
class Q(object):
    def  __init__(self, a, b): #引数を渡す
        self.a = a #引数は必ずself
        self.b = b
    
    def __repr__(self): #__(  )__ で表記されるメソッドは元々意味が決まっている　reprはそのオブジェクトの中身を文字列として表示する
        return f"{self.a}/{self.b}"
    
    
q = Q(1, 2)
print(q)