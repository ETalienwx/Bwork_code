from multiprocessing import Process, Queue
from multiprocessing import Pool
import os
import subprocess
import threading
import random
import time

# 1
# print('process is start...', os.getpid())
# child = os.fork()
# if child == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), child))


# 2
# 启动一个子进程并等待其结束
# 子进程执行的代码
# def child_do(name):
#     print('I am child process, my name is %s (%s)...' % (name, os.getpid()))


# if __name__ == '__main__':
#     print('parent process %s.' % os.getpid())
#     child = Process(target=child_do, args=('test',))
#     print('child process will start.')
#     child.start()  # start()方法启动
#     child.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
#     print('child process end.')


# 3
def task(name):
    print('running task %s(%s)' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('task %s run %0.2f seconds.' % (name, end - start))


if __name__ == '__main__':
    print('process is start %s' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(task, args=(i,))
    print('waiting for all subprocesses done...')
    p.close()  # 对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了
    p.join()
    print('all subprocesses done')


# 4
print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)


# 5
def write(q):
    print('Writing Process %s', os.getpid())
    for value in ['A', 'B', 'C']:
        print('put %s in queue' % value)
        q.put(value)
        time.sleep(random.random())


def read(q):
    print('Reading Process %s', os.getpid())
    while True:
        value = q.get()
        print('get %s in queue' % value)


if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()


# 多线程
# 6
def loop():
    print('thread %s is running..' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        # time.sleep(1)
    print('thread %s end' % threading.current_thread().name)


print('thread %s is running' % threading.current_thread().name)  # 由于任何进程默认就会启动一个线程，我们把该线程称为主线程
t = threading.Thread(target=loop, name='LoopThread')  # 创建了一个叫LoopThread的线程，执行的函数式loop
t.start()  # 启动线程
t.join()  # 等待线程
print('thread %s end.' % threading.current_thread().name)  # threading.current_thread()返回当前线程的实例


# 加锁Lock
balance = 0
lock = threading.Lock()


def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(1000000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()


t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)


# 创建全局ThreadLocal对象:
local_school = threading.local()


def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
