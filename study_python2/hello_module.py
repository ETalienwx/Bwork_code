#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 这是一个简单的模块的编写方法
'a test module'

__author__ = 'wangxuan'

import sys


def test():
    args = sys.argv
    if len(args) == 1:
        print(args[0] + ' 一个参数')
    elif len(args) == 2:
        print(args[0] + ' ' + args[1] + ' 两个参数')
    else:
        print('too many arguments')


if __name__ == '__main__':
    test()
