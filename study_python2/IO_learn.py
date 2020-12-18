import os
from io import StringIO
from io import BytesIO
import pickle
import json

f = os.getcwd()
print(f)


try:
    f = open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r')
    print(f.read())  # 一次读取所有的内容
finally:
    if f:
        f.close()

with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r') as f:
    print(f.read(9))  # 读取九个字符，最后一个是\n

with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r') as f:
    print(f.readlines())  # 按行读取，返回一个列表，列表的每一个元素是文件的每一行

with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r') as f:
    print(f.readline())   # 读取第一行的内容

l1 = []
with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r') as f:
    file_text = f.readlines()
    for line in file_text:
        l1.append(line.rstrip())
print(l1)

# 读取二进制文件，比如图片、视频等等
# f = open('/Users/bilibili/Desktop/pycode1/study2/test.gif', 'rb')
# print(f.read())

# f = open('/Users/bilibili/Desktop/pycode1/study2/let it go.mp4', 'rb')
# print(f.read())


with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("I am Meringue.\n")
    f.write("I am now studying in NJTECH.\n")

with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r') as f:
    print(f.read())

with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
    f.write("I major in Machine learning and Computer vision.\n")

with open('/Users/bilibili/Desktop/pycode1/study2/test.txt', 'r') as f:
    print(f.read())


# import io import StringIO
f = StringIO()
f.write('hello world')
print(f.getvalue())

s = 'Hello!\nHi!\nGoodbye!'
f = StringIO(s)
while True:
    ret = f.readline()
    if ret == '':
        break
    print(ret.rstrip())

# from io import BytesIO
f = BytesIO()
f.write('中文'.encode('utf-8'))
print(f.getvalue())

data = '人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。'.encode('utf-8')
f = BytesIO(data)
print(f.read())

# 操作系统类型
print(os.name)  # posix 如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统
# 详细系统信息
print(os.uname())
# 环境变量
print(os.environ)  # 操作系统中定义的环境变量，全部保存在os.environ这个变量中
# 要获取某个环境变量的值，可以调用os.environ.get('key')
print(os.environ.get('PATH'))

# 查看当前文件的绝对路径
print(os.path.abspath('.'))  # /Users/bilibili/Desktop/pycode1
print(os.path.abspath(__file__))  # /Users/bilibili/Desktop/pycode1/study2/IO_learn.py
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
os.path.join('/Users/bilibili/Desktop/pycode1', 'testdir')
# 然后创建一个目录:
os.mkdir('/Users/bilibili/Desktop/pycode1/testdir')
# 删掉一个目录:
os.rmdir('/Users/bilibili/Desktop/pycode1/testdir')
# 拆分路径：
print(os.path.split('/Users/bilibili/Desktop/pycode1/study2/IO_learn.py'))
# 列出当前目录(pycode)下的所有目录
print([x for x in os.listdir('.') if os.path.isdir(x)])
# 列出所有的.py文件
print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py'])
print(os.path.splitext('/Users/bilibili/Desktop/pycode1/study2/IO_learn.py')[0])  # /Users/bilibili/Desktop/pycode1/study2/IO_learn
print(os.path.splitext('/Users/bilibili/Desktop/pycode1/study2/IO_learn.py')[1])  # .py

# impore pickle
d = dict(name='bob', age=20, score=90)
print(pickle.dumps(d))

# d = dict(name='jack', age=20, score=90)
# f = open('/Users/bilibili/Desktop/pycode1/study2/test1.txt', 'wb')
# pickle.dump(d, f)
# f.close()

# 序列化
d = dict(name='bob', age=20, score=90)
with open('/Users/bilibili/Desktop/pycode1/study2/test1.txt', 'wb') as f:
    pickle.dump(d, f)

# 反序列化
with open('/Users/bilibili/Desktop/pycode1/study2/test1.txt', 'rb') as f:
    print(pickle.load(f))

# dumps()方法返回一个str，内容就是标准的JSON
d = dict(name='bob', age=20, score=90)
j = json.dumps(d)
print(j)

d = dict(name='bob', age=20, score=90)
with open('/Users/bilibili/Desktop/pycode1/study2/test1.txt', 'w') as f:
    json.dump(d, f)

with open('/Users/bilibili/Desktop/pycode1/study2/test1.txt', 'r') as f:
    print(json.load(f))
