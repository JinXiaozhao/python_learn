class ListNode(object):
    def __init__(self,now_data,next_data=None):
        self.data = now_data
        self.next = next_data

class LinkList(object):
    
    def __init__(self):
        self.head = None

    def set(self):
        print('以空格键结束输入！')
        print('input:')
        data = input()
        if data != ' ':
            self.head = ListNode(int(data))
            p = self.head
        else:
            print('over!')
            return
        while 1:
            data = input()
            if data != ' ':
                p.next = ListNode(int(data))
                p = p.next
            else:
                print('over!')
                break

    @property
    def show(self):
        print('链表的元素如下所示：')
        p = self.head
        if p == None:
            print('Empty!')
            return
        while p:
            print(p.data,end = ',')
            p = p.next
        print('over!')
        return
    
    @property
    def isempty(self):
        p = self.head
        if p == None:
            return True
        else:
            return False
        
    @property
    def length(self):
        l = 0
        p = self.head
        while p :
            l += 1
            p = p.next
        return l

    @property
    def reverse(self):
        new_head = self.head
        self.head = None
        while new_head:
            p = new_head
            new_head = new_head.next
            p.next = self.head
            self.head = p
        return
            
            
    def insert(self,data,pos):
        if pos <= 0:
            raise Exception('wrong position!')
        if self.isempty and pos != 1:
            raise Exception('wrong position!')
        
        p = self.head
        if pos == 1:
            self.head = ListNode(int(data))
            self.head.next = p
            return
        n = 2
        while n < pos and p.next != None:
            p = p.next
            n += 1
        
        if n == pos:
            tmp = p.next
            p.next = ListNode(int(data))
            p = p.next
            p.next = tmp
        elif n < pos:
            raise Exception('wrong position!')
        return
    

    def delete(self,pos):
        if pos <= 0:
            raise Exception('wrong position!')
        if pos > self.length :
            raise Exception('wrong position!')
        
        if pos == 1:
            self.head = self.head.next
        else:
            p = self.head
            for i in range(pos-2):
                p = p.next
            p.next = p.next.next
        return

    def swap(self,m,n):
        if m <= 0 or n <= 0 or m==n or m>self.length\
           or n>self.length:
            raise Exception('wrong position!')
        if m>n:
            x=m
            m=n
            n=x
        new_head = ListNode(-1)
        new_head.next = self.head
        p = new_head
        for i in range(m-1):
            p = p.next
        tmp = p
        for i in range(m-1,n-1):
            p = p.next
        
        tmp.next,p.next = p.next,tmp.next
        tmp.next.next,p.next.next = p.next.next,tmp.next.next
        self.head = new_head.next
        return
        
                

if __name__=='__main__':
    x = LinkList()
    x.show
    x.set()
    x.show
    print('链表长度为：%d'%x.length)
    print('删除第一个元素')
    x.delete(1)
    x.show
    print('删除第5个元素')
    x.delete(5)
    x.show
    print('在第4处插入元素4')
    x.insert(4,4)
    x.show
    print('链表翻转')
    x.reverse
    x.show
    print('将第2个元素与第6个元素交换位置')
    x.swap(3,2)
    x.show
    
        

        
        
            
        






            
            
