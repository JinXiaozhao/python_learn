'''
题目2如下：
输入两个单调递增的链表，输出两个链表合成后的链表，
当然我们需要合成后的链表满足单调不减规则。（剑指Offer）
题目2解析：

题目1如下：
输入一个链表，输出该链表中倒数第k个结点。（剑指Offer）
题目1解析：
链表无法回溯，不能从后向前，遍历一遍得到长度，再从头向后找即可。

'''
class ListNode(object):
    def __init__(self,now_data,next_data=None):
        self.head = now_data
        self.next = next_data

class Solution:
    
    #2.merge two ordered link_list
    
    #1.find k th to tail
    def find_K(self,head,k):
        p = head
        n = 0
        while p:
            p = p.next
            n += 1
        
        if n<k:
            return None
        q = head
        for i in range(n-k):
            q = q.next
        return q
    
if __name__=='__main__':
    
    #生成一个链表x
    x = ListNode(5)
    p = x
    for i in range(5):
        p.next = ListNode(i)
        p = p.next
    
    #遍历输出链表x
    q = x
    while q:
        print(q.head,end=',')
        q = q.next
    print('over!')
    
    y = Solution()
    
    #测试题目1函数
    res = y.find_K(x,2)
    print('倒数第2个元素为：{}'.format(res.head))

    
    
