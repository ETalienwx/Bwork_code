from functools import reduce
import functools
import time
print(abs(-10))

a = abs(-20)
print(a)

b = abs
print(b(-30))

# 把函数作为参数


def func1(x, y, f):
    return f(x) + f(y)


print(func1(-30, 20, abs))

a = map(abs, [-10, -20, 30, -40])
print(list(a))


def func2(x):
    return x * x


b = map(func2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(list(b))

print(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])))

# reduce
# from functools import reduce


def func3(x, y):
    return x + y


print(reduce(func3, [1, 2, 3, 4, 5, 6, 7, 8]))  # 36

print(sum([1, 2]))  # 3


def func4(x, y):
    return x * 10 + y


print(reduce(func4, [1, 2, 3, 4, 5, 6, 7, 8]))

# 把字符串转换成int
# 个十百位相加


def func5(x, y):
    return x * 10 + y


# 变成数字


def strtoint(s):
    digit = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    return digit[s]


print(reduce(func5, map(strtoint, '56923')))

print(type(int('99999')))

print('ACD'.lower())


def normalize1(name):
    s = name.title()
    return s


def normalize2(name):
    s = name.lower()
    s = s[0].upper() + s[1:]
    return s


L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize1, L1))
print(L2)

print(normalize2('BBBBB'))


def m(x, y):
    return x * y


def prod(L):
    return(reduce(m, L))


print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')


def str2float(s):
    tmp = s.find('.')
    s1 = s[:tmp]
    s2 = s[tmp+1:]
    s1 = list(map(int, s1))
    s2 = list(map(int, s2))
    s2 = s2[::-1]
    tmp1 = reduce(m1, s1)
    tmp2 = reduce(m2, s2)
    return tmp1 + tmp2*0.1


def m1(x, y):
    return x * 10 + y


def m2(x, y):
    return x * 0.1 + y


print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')


# filter(筛选器)


def is_odd(x):
    return x % 2 != 1  # 偶数


def is_empty(x):
    return x and x.strip()


L = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
print(list(filter(is_odd, L)))
print(list(filter(is_empty, ['A', '', 'B', None, 'C', '  '])))

# 筛选回数12321


def is_palindrome(n):
    return str(n) == str(n)[::-1]


output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))
if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')

print(sorted([5, 2, 3, 4, 6]))  # [2, 3, 4, 5, 6]
print(sorted([-5, 2, 3, 4, -6]))  # [-6, -5, 2, 3, 4]
print(sorted([-5, 2, 3, 4, -6], key=abs))  # [2, 3, 4, -5, -6]
print(sorted(['bob', 'about', 'Zoo', 'Credit']))  # ['Credit', 'Zoo', 'about', 'bob']
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower))  # ['about', 'bob', 'Credit', 'Zoo']
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.upper))  # ['about', 'bob', 'Credit', 'Zoo']
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.upper, reverse=True))  # 逆序排序 ['Zoo', 'Credit', 'bob', 'about']

# L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]按照名字排序


def by_name(t):
    return t[0]


def by_score(t):
    return -t[1]


L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
print(sorted(L, key=by_name))
print(sorted(L, key=by_score))

# 函数作为返回值


def calc_sum(*x):
    sum = 0
    for i in x:
        sum = sum + i
    return sum


print(calc_sum(1, 2, 3, 4, 5, 6, 7, 8))


def lazy_sum(*x):
    def sum():
        retsum = 0
        for i in x:
            retsum = retsum + i
        return retsum
    return sum


print(lazy_sum(1, 2, 3, 4, 5, 6, 7, 8))  # <function lazy_sum.<locals>.sum at 0x1058f9200>
# 因为lazy_sum返回的是一个函数，因此需要调用才可以打印出结果
print(lazy_sum(1, 2, 3, 4, 5, 6, 7, 8)())  # 36

# 利用闭包返回一个计数器函数，每次调用它返回递增整数


def createCounter():
    x = [0]  # 创建了一个新的链表，链表里面有一个数，为0

    def counter():
        x[0] = x[0] + 1  # 取链表中的第一个数0，然后+1操作，以此类推
        return x[0]  # 返回这个数

    return counter   # 返回conter函数


counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')

print(list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8])))

# 装饰器


def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


# 把@log放到now()函数的定义处，相当于执行了语句now = log(now),wrapper()函数的参数定义是(*args, **kw)，因此，wrapper()函数可以接受任意参数的调用。在wrapper()函数内，首先打印日志，再紧接着调用原始函数
@log
def now():
    print('2020-6-28,12:00')


print(now.__name__)  # wrapper(name已经发生了改变了)
now()


# 需要传入参数的话，比如要自定义log的文本


def log(test):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (test, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

# now = log('execute')(now)，首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数
@log('execute')
def now():
    print('2020-6-28,12:00')


print(now.__name__)  # wrapper(name已经发生了改变了)
now()

# 因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错
# 不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的
# 定义wrapper()的前面加上@functools.wraps(func)即可
# import functools


def log(func):
    @functools.wraps(func)  # wrapper.__name__ = func.__name__
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


# import functools


def log(test):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('call %s():' % func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator


# 设计一个decorator，它可作用于任何函数上，并打印该函数的执行时间


def metric(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        t = time.time()  # 现在的时间
        func(*args, **kw)  # 运行一下函数
        print('%s executed in %s ms' % (func.__name__, time.time() - t))  # 计算时间差
        return func(*args, **kw)
    return wrapper


@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y


@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z


f = fast(11, 22)
s = slow(11, 22, 33)


# 偏函数
print(int('10', 2))  # 计算10的二进制输出


def int2(x, base=2):
    return int(x, base)


print(int2('1000'))

int2 = functools.partial(int, base=2)
print(int2('1000'))

