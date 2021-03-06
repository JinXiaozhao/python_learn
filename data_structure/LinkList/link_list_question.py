'''
题目3如下(LeetCode)：
将链表循环右移K个位置
题目解析：
找倒数第k个结点类似，先获取长度最关键，
要注意对k>=长度的处理。关键点在于利用三个结点：
head（链表头），p（链表尾），q（倒数第k结点的前一个），将三者按顺序连起来即可。

题目2如下（剑指Offer）：
输入两个单调递增的链表，输出两个链表合成后的链表，
当然我们需要合成后的链表满足单调不减规则。
题目2解析：

题目1如下（剑指Offer）：
输入一个链表，输出该链表中倒数第k个结点。
题目1解析：
链表无法回溯，不能从后向前，遍历一遍得到长度，再从头向后找即可。

'''
class ListNode(object):
    def __init__(self,now_data,next_data=None):
        self.head = now_data
        self.next = next_data

class Solution:

    

    #3.rotate right K
    def rotate_rightK(self,head,k):
        if head == None:
            return head
        p = head
        l = 1
        while p.next:
            p = p.next
            l += 1
        if l == k:
            return head
        if k == 0:
            return head
        if l < k:
            k = k % l
        q = head
        for i in range(1,l-k):
            q = q.next
        p.next = head
        res = q.next
        q.next = None
        return res
        
        
    
    #2.merge two ordered link_list
    def merge2link_list(self,head1,head2):
        if head1 == None:
            return head2
        if head2 == None:
            return head1
        if head1.head <= head2.head:
            head1.next = Solution.merge2link_list(self,head1.next,head2)
            return head1
        else:
            head2.next = Solution.merge2link_list(self,head2.next,head1)
            return head2
        
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
    
def show(head):
    q = head
    while q:
        print(q.head,end=',')
        q = q.next
    print('over!')
    
if __name__=='__main__':


    #测试题目3
    print('----------------------------------')
    #生成一个链表x
    x = ListNode(0)
    p = x
    for i in range(5):
        p.next = ListNode(i)
        p = p.next
    print('链表为：')
    show(x)
    y = Solution()
    res3 = y.rotate_rightK(x,2)
    print('链表右移2位后，链表为：')
    show(res3)
    
    #测试题目2
    print('----------------------------------')
    #生成一个链表x
    x = ListNode(0)
    p = x
    for i in [1,5,8,40,45,55]:
        p.next = ListNode(i)
        p = p.next
    #生成一个链表z
    z = ListNode(5)
    p = z
    for i in range(6,11):
        p.next = ListNode(i)
        p = p.next
    
    #遍历输出链表
    print('第一个链表为：')
    show(x)
    print('第二个链表为：')
    show(z)
    y = Solution()
    res2 = y.merge2link_list(x,z)
    print('合并后链表为：')
    show(res2)
    
    #测试题目1函数
    print('----------------------------------')
    #生成一个链表x
    x = ListNode(0)
    p = x
    for i in range(5):
        p.next = ListNode(i)
        p = p.next
    print('链表为：')
    show(x)
    y = Solution()
    res1 = y.find_K(x,2)
    print('倒数第2个元素为：{}'.format(res1.head))

    
    
