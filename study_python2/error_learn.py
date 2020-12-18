import logging
from functools import reduce
import unittest
logging.basicConfig(level=logging.INFO)

# try
try:
    print("try...")
    r = 10/0
    print(r)
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
print('END')

try:
    print('try...')
    r = 10 / int('a')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
finally:
    print('finally...')
print('END')

# 没有错误时可以添加else语句,没有错误的时候就会执行else
try:
    print('try...')
    r = 10 / int('q')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
else:
    print('no error')
finally:
    print('finally...')
print('END')


# 记录错误
# import logging

def foo(s):
    return 10 / int(s)


def bar(s):
    return foo(s) * 2


def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)


main()
print('END')


# # 抛出错误
# class FooError(ValueError):  # 这是一个错误类，继承的是ValueError
#     pass


# def fooo(s):
#     n = int(s)
#     if n == 0:
#         raise FooError('invalid value: %s' % s)
#     return 10 / n


# fooo('0')


def str2num(s):
    # if isinstance(s, int):
    #     return int(s)
    # if isinstance(s, float):
    #     return float(s)
    return float(s)


def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)


def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)


main()


# 调试
# 断言
# def f1(s):
#     n = int(s)
#     assert n != 0, 'n is zero'
#     return 10 / n


# def main():
#     f1('0')


# main()


# logging
# s = '0'
# n = int(s)
# logging.info('n = %d' % n)
# print(10 / n)

d = {'a': 1, 'b': 2, 'c': 3}
print(d)
print(d['a'])

d = dict(a=1, b=2, c=3)
print(d['a'])
print(d['b'])


# 测试一个学生类的分数
# import unittest
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if self.score >= 0 and self.score < 60:
            return 'C'
        elif self.score >= 60 and self.score < 80:
            return 'B'
        elif self.score < 0 or self.score > 100:
            raise ValueError('score must be between 0 and 100')
        else:
            return 'A'


class TestStudent(unittest.TestCase):

    def test_80_to_100(self):
        s1 = Student('Bart', 80)
        s2 = Student('Lisa', 100)
        self.assertEqual(s1.get_grade(), 'A')
        self.assertEqual(s2.get_grade(), 'A')

    def test_60_to_80(self):
        s1 = Student('Bart', 60)
        s2 = Student('Lisa', 79)
        self.assertEqual(s1.get_grade(), 'B')
        self.assertEqual(s2.get_grade(), 'B')

    def test_0_to_60(self):
        s1 = Student('Bart', 0)
        s2 = Student('Lisa', 59)
        self.assertEqual(s1.get_grade(), 'C')
        self.assertEqual(s2.get_grade(), 'C')

    def test_invalid(self):
        s1 = Student('Bart', -1)
        s2 = Student('Lisa', 101)
        with self.assertRaises(ValueError):
            s1.get_grade()
        with self.assertRaises(ValueError):
            s2.get_grade()


# if __name__ == '__main__':
#     unittest.main()


class Dict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()


def fact(n):
    if n < 1:
        raise ValueError
    if n == 1:
        return 1
    else:
        return n * fact(n - 1)


print(fact(10))
