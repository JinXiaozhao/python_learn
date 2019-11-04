# 循环队列
from collections import deque

class Queue():
    def __init__(self, size):
        self.__size = size
        self.__head = -1 
        self.__tail = -1
        self.__quene = deque([])
    def pop(self):
        if self.is_empty():
            raise Exception('queue is empty!')
        else:
            self.__head += 1
            if self.__head == self.__size:
                self.__head = 0
            return self.__quene.popleft()
    def push(self, data):
        if self.is_full():
            raise Exception('out of range!')
        else:
            self.__quene.append(data)
            self.__tail += 1
            if self.__tail == self.__size:
                self.__tail = 0   
    def is_empty(self):
        return self.__head == self.__tail
    def is_full(self):
        if self.__head != self.__tail:
            return self.__tail == (self.__head) % self.__size
        else:
            return False
    def show(self):
        if self.is_empty():
            raise Exception('queue is empty!')
        else:
            print(self.__quene)
            
if __name__=='__main__':
    x = Queue(10)
    x.push(1)
    x.push(2)
    x.show()
    for i in range(3,9):
        x.push(i)
    for i in range(7):
        print(x.pop())
    x.push(2)
    print(x.pop())
    print(x.pop())
    for i in range(3,9):
        x.push(i)
    print(x._Queue__head)
    print(x._Queue__tail)
    
