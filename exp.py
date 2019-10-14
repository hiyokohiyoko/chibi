class Val(object):
    __slots__ = ['value']
    def __init__(self, v = 0):
        self.value = v

    def eval(self):
        return self.value

    def __repr__(self):
        return f'Val({self.value})'

class Add(object):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right #この2つは式として渡される
    
    def eval(self):
        return self.left.eval() + self.right.eval() # 元々式の値として渡し、ここで評価するようにする

class Mul(object):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def eval(self):
        return self.left.eval() * self.right.eval()

class Sub(object):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def eval(self):
        return self.left.eval() - self.right.eval()



    
#Val
e = Val(1)
assert e.eval() == 1
print(e.eval())

#Add
v = Add(Val(1), Val(2))
assert v.eval() == 3
print(v.eval())
# e = Add(1, Add(2, 3)) # これだとうまくいかない　self.rightに式が入ってしまうため
e = Add(Val(1), Add(Val(2), Val(3)))
print(e.eval())

#Mul
e = Mul(Val(1), Val(2))
assert e.eval() == 2
print(e.eval())

#Sub
e = Sub(Val(1), Val(2))
assert e.eval() == -1
print(e.eval())