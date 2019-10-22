class Stock():
    #数组栈
    def __init__(self,size):
        self.size = size
        self.stock = []
        self.top = -1
    def is_empty(self):
        return self.top == -1
    def is_full(self):
        return self.top == self.size + 1
    def push(self,x):
        if self.top == self.size + 1:
            raise Exception('stack is full!')
        else:
            self.stock.append(x)
            self.top = self.top + 1
    def pop(self):
        if self.top == -1:
            raise Exception('stack is empty!')
        else:
            self.top = self.top -1
            return self.stock.pop()
    def show(self):
        if self.top == -1:
            raise Exception('stock is empty!')
        else:
            return self.stock

if __name__=='__main__':
    a = Stock(20)
    for i in range(10):
        a.push(i)
    print(a.show())
    a.pop()
    print(a.pop())
    print(a.show())
