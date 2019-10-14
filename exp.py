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
        self.right = right
    
    def eval(self):
        return self.left + self.right

    

e = Val(1)
assert e.eval() == 1
print(e.eval())

v = Add(1, 2)
assert v.eval() == 3
print(v.eval())