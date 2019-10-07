
class Counter(object): #objectは最初のうちは決まり文句
    def  __init__(self): #コンストラクタ. 必ず必要
        self.cnt = 0 #引数は必ずself
    
    def count(self):
        self.cnt += 1
    
    def doublecount(self):
        self.cnt += 2
    
    def reset(self):
        self.cnt = 0
    
    def show(self):
        print(self.cnt)

    def __repr__(self): #__(  )__ で表記されるメソッドは元々意味が決まっている　reprはそのオブジェクトの中身を文字列として表示する
        return str(self.cnt)


c = Counter()
c.show()
c.count()
c.show()

print()

c.show()
c.doublecount()
c.show()

print(type(c)) #そのオブジェクトのクラスを出力
print(c) #オブジェクトの中身を表示　reprのおかげでオブジェクトの住所ではなく中身の数字が文字列として出力



