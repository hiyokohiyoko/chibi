class Val(object):
    __slots__ = ['value']
    def __init__(self, v = 0):
        self.value = v

    def eval(self):
        return self.value

    def __repr__(self):
        return f'Val({self.value})'

e = Val(1)
assert e.eval() == 1
print(e.eval())