#小根堆
class Bin_heap():
    def __init__(self):
        self.item = []
        self.len = 0
    def size(self):
        return len(self.item)
    def num_up(self,i):
        while (i-1)//2 >= 0:
            j = (i-1)//2
            if self.item[i]<self.item[j]:
                self.item[i],self.item[j] = self.item[j],self.item[i]
            else:
                break
            i = j  
    def insert(self,num):
        self.item.append(num)
        self.num_up(self.len)
        self.len = self.len + 1
    def num_down(self,i,j):
        while i*2+1 <= j:
            if i*2+2>j:
                s = i*2+1
            else:
                if self.item[i*2+1]<self.item[i*2+2]:
                    s = i*2+1
                else:
                    s = i*2+2
            if self.item[s]<self.item[i]:
                self.item[s],self.item[i] = self.item[i],self.item[s]
            else:
                break
            i = s
    def del_first(self):
        self.item[0],self.item[self.len-1] = self.item[self.len-1],self.item[0]
        x = self.item.pop()
        self.len = self.len-1
        self.num_down(0,self.len-1)
        return x
    def build_heap(self,nums):
        i = len(nums)
        while i >0:
            self.insert(nums.pop())
            i -= 1
        return self.item
    def show(self):
        print(self.item)
    def is_empty(self):
        return self.len == 0
#大根堆
class Big_heap(Bin_heap):
    def num_down(self,i,j):
        while i*2+1<=j:
            if i*2+2>j:
                s = i*2+1
            else:
                if self.item[i*2+1]<self.item[i*2+2]:
                    s = i*2+2
                else:
                    s = i*2+1
            if self.item[s]>self.item[i]:
                self.item[s],self.item[i] = self.item[i],self.item[s]
            else:
                break
            i = s
    
    def num_up(self,i):
        while (i-1)//2 >= 0:
            j = (i-1)//2
            if self.item[i]>self.item[j]:
                self.item[i],self.item[j] = self.item[j],self.item[i]
            else:
                break
            i = j   

def test():
    import random
    b = Big_heap()
    x = []
    res = []
    for i in range(random.randint(10,11)):
        x.append(random.randint(0,100))
    print(x)
    y = b.build_heap(x)
    print(y)
    while len(y)> 0:
        res.append(b.del_first())
        #print(y)
    print(res)
    

if __name__ == "__main__":
    test()

        
        
