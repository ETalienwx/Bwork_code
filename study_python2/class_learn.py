import types
from types import MethodType
from enum import Enum, unique


class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s %s' % (self.name, self.score))

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score


s1 = Student('wangxuan', 90)
s1.print_score()
print(type(s1))
print(s1)  # 是一个类的实例
s2 = Student('bart', 59)
s2.print_score()


class Animal(object):
    def run(self):
        print('animal is running...')


class Dog(Animal):
    def run(self):
        print('dog is running...')


class Tortoise(Animal):
    def run(self):
        print('Tortoise is running slowly...')


class Timer(object):
    def run(self):
        print('Start...')


def run2(animal):
    animal.run()


dog = Dog()
dog.run()
animal = Animal()
animal.run()
print(isinstance(dog, Dog))
print(isinstance(dog, Animal))  # 子类数据类型可以看做是父类
print(isinstance(animal, Dog))  # 父类数据类型不可以看做是子类
a1 = Animal()
d1 = Dog()
t1 = Tortoise()
print(run2(a1))
print(run2(d1))
print(run2(t1))
t2 = Timer()  # python中不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以了
print(run2(t2))


def fn():
    pass


# print(type(fn) == types.FunctionType)
# print(type(lambda x: x) == types.LambdaType)

print(isinstance(fn, types.FunctionType))
print(dir('abc'))
print(len('abc'))
print('abc'.__len__())


# 自己写的类如果想用len方法，那就自己写一个__len__
class Dog(Animal):
    def run(self):
        print('dog is running...')

    def __len__(self):
        print(100)


dog = Dog()
# len(dog)


class MyObject(object):

    def __init__(self):
        self.x = 100

    def power(self):
        return self.x * self.x


obj = MyObject()
print(hasattr(obj, 'x'))  # True
print(getattr(obj, 'x'))  # 100
print(setattr(obj, 'y', 1000000))
print(hasattr(obj, 'y'))
print(getattr(obj, 'y'))
# 获取属性'z'，如果不存在，返回默认值404
print(getattr(obj, 'z', 404))

fn = getattr(obj, 'power')
print(fn)  # fn是power函数
print(fn())  # 调用power函数


class Student(object):
    count = 0  # 类属性

    def __init__(self, name):
        self.name = name
        Student.count += 1


w = Student('wang')
z = Student('zhang')
l1 = Student('li')
print(w.name)
print(Student.count)


class Student(object):
    pass


s = Student()
# 动态给实例绑定一个属性
s.name = 'zhangsan'
print(s.name)


# 动态给实例绑定一个方法
def set_age(self, age):  # 定义一个函数作为实例方法
    self.age = age


# from types import MethodType
s.set_age = MethodType(set_age, s)  # 给实例绑定方法
s.set_age(20)  # 调用实例方法
print(s.age)  # 打印

Student.set_age = MethodType(set_age, Student)  # 给类添加方法后所有的实例都可以使用了
s2 = Student()
s2.set_age(25)
print(s2.age)

s3 = Student()
s3.set_age(30)
print(s3.age)


# 限制实例属性
class Student(object):
    __slots__ = ('name', 'age')  # 限制只能添加name和age


s1 = Student()
s1.name = 'zhangsan'
s1.age = 30
# s1.score = 90  # 添加不进去
try:
    s1.score = 99
except AttributeError as e:
    print('AttributeError:', e)


class Student(object):

    def set_score(self, score):
        if not isinstance(score, int):
            raise TypeError('score must be an integer')
        if score > 100 or score < 0:
            raise ValueError('score must be between 0 and 100')
        self.score = score

    def get_score(self):
        return self.score


s1 = Student()
s2 = Student()
# s1.set_score('123')
# s2.set_score(9999)
s1.set_score(90)
print(s1.get_score())


class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise TypeError('score must be an integer')
        if value > 100 or value < 0:
            raise ValueError('score must be between 0 and 100')
        self._score = value


s1 = Student()
s1.score = 100
print(s1.score)


class Student(object):

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday = value

    def age(self):
        return 2020 - self._birthday


s1 = Student()
s1.birthday = 1998
print(s1.birthday)
print(s1.age())


# 请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution
class Screen(object):
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def resolution(self):
        return self._width * self._height


s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')


class Animal(object):
    pass


# 大类:
class Mammal(Animal):
    pass


class Bird(Animal):
    pass


class Runnable(object):
    def run(self):
        print('Running...')


class Flyable(object):
    def fly(self):
        print('Flying...')


# 各种动物:
class Dog(Mammal, Runnable):  # MixIn(MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系)
    pass


class Bat(Mammal, Flyable):
    pass


class Parrot(Bird, Flyable):
    pass


class Ostrich(Bird, Runnable):
    pass


# 定制类
# __str__：创建实例打印的时候，若打印该实例可以打印一个好看的字符串
class Student(object):
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return 'Student Object (name: %s)' % self._name

    __repr__ = __str__  # __str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的


print(Student('Michael'))
s = Student('Michael')
print(s)


# __iter__:可以让class类用于for...in...循环，不断迭代__next__方法
class Fib(object):

    def __init__(self):
        self.a, self.b = 0, 1  # 初始化两个计数器a，b

    def __iter__(self):
        return self  # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b  # 计算下一个值
        if self.a > 1000000:  # 退出循环的条件
            raise StopIteration()
        return self.a  # 返回下一个值


for i in Fib():
    print(i)


# __getitem__:可以让class像list一样根据下标取到元素
class Fib(object):

    def __getitem__(self, n):
        if isinstance(n, int):  # n是索引
            a, b = 1, 1
            for i in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):  # n是切片
            start, stop = n.start, n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for i in range(stop):
                if i >= start:
                    L.append(a)
                a, b = b, a + b
            return L


print(Fib()[100])  # 获取第100个元素
print(Fib()[0:10])  # 获取前十个元素


# # __getattr__:当调用的是不存在的属性的时候，会试图调用getattr里的属性
# class Student(object):

#     def __init__(self, name):
#         self.name = name

#     def __getattr__(self, attr):
#         if attr == 'age':
#             return 10
#         if attr == 'gender':
#             return 'Female'
#         raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)


# s = Student('zhangsan')
# print(s.name)
# # 只有在没有找到属性的情况下，才调用__getattr__，已有的属性，比如name，不会在__getattr__中查找
# print(s.age)
# print(s.gender)
# # 任意调用如s.abc都会返回None，这是因为我们定义的__getattr__默认返回就是None
# print(s.abc)  # None
# # 要让class只响应特定的几个属性，我们就要按照约定，抛出AttributeError的错误


# __call__:直接对实例进行调用
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('my name is %s.' % self.name)


s = Student('Michael')
print(s())  # 不需要传入self参数，直接调用的时候调用的是__call__

print(callable(Student('Michael')))
print(callable(max))
print(callable([1, 2, 3]))


# 枚举类
# from enum import Enum

Months = Enum('Months', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Months.__members__.items():
    print(name, '=>', member, ',', member.value)

# from enum import Enum, unique


@unique
class Weekday(Enum):
    Sun = 0  # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6


print(Weekday.Mon)  # Weekday.Mon
print(Weekday.Mon.value)  # 1
print(Weekday['Mon'])  # Weekday.Mon
print(Weekday['Mon'].value)  # 1
print(Weekday(1))  # Weekday.Mon
print(Weekday(6))  # Weekday.Sat
for name, member in Weekday.__members__.items():
    print(name, '==>', member)
# Sun ==> Weekday.Sun
# Mon ==> Weekday.Mon
# Tue ==> Weekday.Tue
# Wed ==> Weekday.Wed
# Thu ==> Weekday.Thu
# Fri ==> Weekday.Fri
# Sat ==> Weekday.Sat


# 使用元类：type()
class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)


h = Hello()
h.hello()  # Hello, world.
print(type(Hello))  # <class 'type'>
print(type(h))  # <class '__main__.Hello'>


def fn(self, name='world'):  # 先定义函数
    print('Hello, %s.' % name)


Hello = type('Hello', (object,), dict(hello=fn))  # 创建Hello class
h = Hello()
h.hello()

# metaclass:控制类的创建行为
