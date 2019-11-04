class Num_systems():
    def __init__(self,a,b,data):
        self.__a = int(a)
        self.__b = int(b)
        self.__num = int(data)
    def a2ten(self):
        s = 0
        y = []
        for i in str(self.__num):
            y.append(i)
        i = 0
        while y:
            num = y.pop()
            s += int(num)*self.__a**i
            i += 1
        self.__num = s
      
    def a2b(self):
        if self.__a != 10:
            self.a2ten()
        x = []
        while self.__num:
            x.append(int(self.__num % self.__b))
            self.__num = int(self.__num / self.__b)
        return x
if __name__ == '__main__':
    y = Num_systems(10,8,2007)
    x = y.a2b()
    while x:
        print(x.pop())
