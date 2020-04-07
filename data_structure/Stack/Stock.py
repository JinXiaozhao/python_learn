class Stock():
    #数组栈
    def __init__(self,size=1000):
        self.max_size = size
        self.item = []
        self.top = -1
    def is_empty(self):
        return self.item == []
    def is_full(self):
        return self.top == self.max_size + 1
    def push(self,x):
        if self.top == self.max_size + 1:
            raise Exception('stack is full!')
        else:
            self.item.append(x)
            self.top = self.top + 1
    def pop(self):
        if self.top == -1:
            raise Exception('stack is empty!')
        else:
            self.top = self.top -1
            return self.item.pop()
    def show(self):
        if self.top == -1:
            raise Exception('stock is empty!')
        else:
            return self.item
    def size(self):
        return len(self.item)
    def peek(self):
        return self.item[-1]

if __name__=='__main__':
    a = Stock(20)
    for i in range(10):
        a.push(i)
    print(a.show())
    a.pop()
    print(a.peek())
    print(a.show())
    print(a.size())
