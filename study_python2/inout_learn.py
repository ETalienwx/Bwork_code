from collections.abc import Iterable, Iterator
# print()会依次打印每个字符串，遇到逗号“,”会输出一个空格
print("hello", "world", "apple")

# 输入字符串
# name = input()
# print(name)
# print(type(name))  # string

# name = input("请输入名字：")
# print("hello", name)

# if
# a = input ("please enter a number:")
# a = int(a)
# if a > 0:
#     print(a)
# else:
#     print(-a)

print(20/3)
print(6.66/3)

print("I'm okay!")
print("I'm \"OK\"!")
print("\\")
print('''line1
line2
line3
line4''')

print(2 > 3)  # False
print(2 > 1 and 3 > 5)
print(2 > 1 or 5 > 7)
print(not 2 > 3)

a = 'ABC'
b = a  # b也指向a的字符串
print(a)  # ABC
print(b)  # ABC

a = 'ABC'
b = a  # b也指向a的字符串
a = 'XYZ'
print(a)  # XYZ
print(b)  # ABC

# 普通除法
print(10/3)  # 3.33333333335
print(9/3)  # 3.0
# 整除
print(10//3)  # 3
print(9//3)  # 3
# 取余
print(10 % 3)  # 1

# 字符编码
print(ord("你"))
print(chr(21566))

# Unicode表示的str通过encode()方法可以编码为指定的bytes
print("中文".encode("utf-8"))
print("abc".encode("ascii"))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode("utf-8"))

# 格式化
print("hello %s" % "world")
print("hi, %s you have %d$" % ("jack", 100))
print("%s你好，你当月话费为%0.2f，当月余额为%0.2f。" % ("jack", 23.6, 0.01))

s1 = 72
s2 = 85
percent = ((s2-s1)/s2)*100
print("%0.1f%%" % percent)

l1 = [1, 2, 3, 3, 3]
print(l1[-1])
print(l1[2])
l1.append(4)
print(l1)
l1.insert(1, 50)
print(l1)
l1.pop()
print(l1)
l2 = l1.copy()
print(l2)
print(l1.count(3))
print(l1.index(50))
l1.reverse()
print(l1)
l1.remove(3)
print(l1)
l1.sort()
print(l1)
l1.pop(2)
print(l1)
l1[1] = 20
print(l1)

p = ['asp', 'php']
s = ['python', 'java', p, 'scheme']
print(s)

t1 = (1, 2, 3, 4, 5)
t2 = (1,)
print(t2)
t3 = (1)
print(t3)

t4 = (1, 2, 3, [4, 5])
t4[3][0] = 40
print(t4)

# 条件判断
age = 16
if age >= 18:
    print('your age is ', age)
    print('adult')
elif age >= 12:
    print('your age is ', age)
    print('child')
else:
    print('your age is ', age)
    print('teenager')

# 从上往下执行
age = 16
if age >= 12:
    print('your age is ', age)
    print('adult')
elif age >= 18:
    print('your age is ', age)
    print('child')
else:
    print('your age is ', age)
    print('teenager')

x = 0
if x:
    print('True')

# s = input('Enter your birth month:')
# s = int(s)
# if s > 2000:
#     print('00后')
# else:
#     print('00前')

weight = 46
height = 1.59
bmi = weight/(height*height)
if bmi < 18.5:
    print("guoqing")
elif 18.5 < bmi < 25:
    print("zhengchang")
elif 25 < bmi < 28:
    print("guozhong")
elif 28 < bmi < 32:
    print("feipang")
else:
    print('yanzhongfeibang')

# l3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# sum = 0
# for i in l3:
#     # print(i)
#     sum = sum + i
#     print(sum)

sum = 0
for i in range(101):
    sum = sum + i
print(sum)

sum = 0
i = 100
while i > 0:
    if i % 2 != 0:
        sum = sum + i
    i = i - 1
print(sum)

# dict
d = {'jack': 10, 'jecka': 25, 'jason': 30}
print(d)
print(d['jack'])
d['jundy'] = 40
print(d)
d['jack'] = 90
print(d)
for i in d:
    print(i, ':', d[i])
for i in d:
    if d[i] % 2 == 0:
        print(i, ':', d[i])
    else:
        pass

print(d.get("kop"))

print('kop' in d)

d.pop('jundy')
print(d)

# set(自动排序，去重)
s = set([5, 3, 2, 1, 1, 1, 1, 4])
s.add(6)
s.remove(4)
s.clear()
print(s)

s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 | s2)
print(s1 & s2)

# 函数


def my_abs(x):
    if x < 0:
        return(-x)
    else:
        return(x)


print(my_abs(-10))


# def test(x):
#     if not isinstance(x, (int, float)):
#         raise TypeError("bad operand type")
#     if x < 0:
#         return(-x)
#     else:
#         return(x)


# print(test('A'))


def test2(x, y):
    return x, y


print(test2(1, 2))
print(type(test2(1, 2)))


def test3(x, y):
    ret = 1
    while y > 0:
        ret = ret * x
        y -= 1
    return ret


def test4(x, y=2):
    ret = 1
    while y > 0:
        ret = ret * x
        y -= 1
    return ret


print(test3(5, 3))
print(test4(5))


def test5(*numbers):
    sum = 0
    for i in numbers:
        sum = sum + i
    return sum


print(test5(4, 5))
print(test5(4, 5, 5))
l4 = [4, 5, 6]
print(test5(*l4))


def test6(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)


test6('jack', 18)
test6('jackson', 18, city='beijing')
test6('judy', 18, city='beijing', job='engineer')

extra = {'city': 'Beijing', 'job': 'Engineer'}
test6('jeacka', 18, **extra)

# 检查是否有city和job参数


def test7(name, age, **kw):
    if 'city' in kw:
        pass
    if 'job' in kw:
        pass
    print('name:', name, 'age:', age, 'other:', kw)


def test8(name, age, *, city, job):
    print('name:', name, 'age:', age, 'city:', city, 'job:', job)


test8('kay', 18, city='beijing', job='engineer')


def product(x, *y):
    s = x
    for i in y:
        s = s * i
    return s


def product2(*number):
    ret = 1
    for i in number:
        ret = ret * i
    return ret


print(product(5))
print(product(5, 6))
print(product(5, 6, 7))
print(product(5, 6, 7, 9))

# 递归函数


def test9(n):
    if n == 1:
        return 1
    else:
        return n * test9(n-1)


print(test9(5))
print(test9(100))

l5 = []
for i in range(100):
    l5.append(i)
print(l5)

l6 = []
for i in range(100):
    if i % 2 == 0:
        l6.append(i)
print(l6)

l7 = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(l7[0:3])
print(l7[-2:])

print(l5[10:20])
print(l5[1::2])
print(l5[::5])
print(l5[:])
print(l7[::-1])

# 汉诺塔


def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
    else:
        move(n-1, a, c, b)
        print(a, '-->', c)
        move(n-1, b, a, c)


def trim(s):
    while s[0] == '':
        s = s[1:]
    while s[-1] == '':
        s = s[:-1]
    return s


print(trim('hello  '))


for i, val in enumerate(l7):
    print(i, val)


def findMinAndMax(L):
    if len(L) == 0:
        return(None, None)
        x = L[0]
        y = L[0]
        for i in L:
            if x > i:
                x = i
            elif y < i:
                y = i
        return x, y


print(findMinAndMax([7, 1, 3, 9, 5]))

# 列表生成式
print([x * x for x in range(1, 11)])
print([x for x in range(100)])
print([x for x in range(100) if x % 2 == 0])
# 列出当前目录下的所有文件和目录名
# import os
# print(d for d in os.listdir('.'))

d = {'x': 'A', 'y': 'B', 'z': 'C'}
for x, val in d.items():
    print(x, val)

print([k + '=' + val for k, val in d.items()])

L = ['Hello', 'World', 'IBM', 'Apple']
print([i.lower() for i in L])

print([x * x for x in range(1, 10) if x % 2 == 0])

# 斐波那契


def fib(num):
    n, a, b = 0, 0, 1
    while n < num:
        print(b)
        a, b = b, a+b
        n = n + 1
    return 'done'


def fib2(num):
    n, a, b = 0, 0, 1
    while n < num:
        a, b = b, a+b
        n = n + 1
    return a


print(fib2(6))

# generate(生成器)
g = (x * x for x in range(10))
# next(g)
for i in g:
    print(i)


def fib3(num):
    n, a, b = 0, 0, 1
    while n < num:
        yield b
        a, b = b, a+b
        n = n + 1
    return 'done'


def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield 2
    print('step 3')
    yield 3


o = odd()
print(next(o))
print(next(o))
print(next(o))

# 一般直接用for循环迭代
for i in fib3(6):
    print(i)

# 打印杨辉三角


def triangles():
    s = [1]
    while True:
        yield s
        s = [1]+[s[i]+s[i+1] for i in range(len(s)-1)]+[1]
    pass


n = 0
results = []
for t in triangles():
    results.append(t)
    n = n + 1
    if n == 10:
        break

for t in results:
    print(t)

# 自己实现杨辉三角的打印


def test10():
    s = [1]
    while True:
        yield s
        s = [1] + [s[i] + s[i+1] for i in range(len(s)-1)] + [1]
    pass


ret = []
n = 0
for i in test10():
    ret.append(i)
    n = n + 1
    if n == 10:
        break

for i in ret:
    print(i)

# 迭代器
print(isinstance([], Iterable))  # True
print(isinstance([], Iterator))  # False
print(isinstance(range(10), Iterator))  # False
print(isinstance((x for x in range(10)), Iterator))  # True(generate)
print(isinstance(iter([]), Iterator))  # True(使用iter把[]变成了迭代器)
