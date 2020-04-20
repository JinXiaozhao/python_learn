#使用列表实现循环队列
class Queue():
    def __init__(self,size):
        self.size = size
        self.length = 0
        self.head = 0
        self.end = 0
        self.items = [0]*self.size
    def push(self,num):
        if self.length == self.size:
            raise Exception("queue is full")
        self.length += 1
        self.items[self.end] = num
        self.end = 0 if self.end == self.size - 1 else self.end+1
    def pop(self):
        if  self.length == 0:
            raise Exception("queue is empty")
        self.length -= 1
        temp = self.head
        self.head = 0 if self.head == self.size-1 else self.head+1
        return self.items[temp]
    def is_full(self):
        return self.length == self.size
    def is_empty(self):
        return self.length == 0
    def show(self):
        if  self.length == 0:
            raise Exception("queue is empty")
        else:
            start = self.head
            l = self.length
            while l:
                print(self.items[start])
                start = 0 if start == self.size-1 else start+1
                l -= 1
if __name__=='__main__':
    x = Queue(10)
    x.push(1)
    x.push(2)
    x.show()
    print("-----")
    
    for i in range(3,9):
        x.push(i)
    x.show()
    print("-----")
    for i in range(7):
        print(x.pop())
    print("-----")
    x.show()
    print("-----")
    x.push(2)
    print("-----")
    print(x.pop())
    print(x.pop())
    for i in range(3,9):
        x.push(i)
    
    print("-----")
    x.show()
    print("-----")
            
