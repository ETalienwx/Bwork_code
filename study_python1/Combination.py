# --------------------------组合--------------------------
# # 学生类
# class Student:
#     def __init__(self, name, score=100):
#         self.name = name
#         self.score = score


# # 教室类
# class ClassRoom:
#     def __init__(self, name):
#         self.name = name


# # 校长类
# class SchoolMasters:
#     def __init__(self, name):
#         self.name = name


# # 学校类（以上三个类共同构成学校类）
# class School:
#     def __init__(self):
#         self.students = Student("张三")
#         self.classroom = [ClassRoom("403"), ClassRoom("404")]
#         self.schoolmaster = SchoolMasters("李四")

#     # def Print(self):
#     #     print(self.schoolmaster.name)


# a = School()
# print(a.schoolmaster.name)

# --------------------------继承1--------------------------
# class Cat:
#     def __init__(self):
#         self.name = "huahua"


# class EShortCat(Cat):
#     def __init__(self):
#         self.type = "英短"


# class AShortCat(Cat):
#     def __init__(self):
#         self.type = "美短"


# class CShortCat(Cat):
#     def __init__(self):
#         self.type = "土猫"


# class SDLionCat(CShortCat):
#     def __init__(self):
#         self.type = "山东狮子猫"

#     def Print(self):
#         print(self.type)


# a = SDLionCat()
# a.Print()  # 山东狮子猫

# --------------------------继承2--------------------------
# class Parent:
#     def __init__(self):
#         self.msg = "hahaha"

#     def PrintMsg(self):
#         print(self.msg)


# class Child(Parent):
#     pass


# c = Child()
# c.PrintMsg()  # 子类可以调取父类的方法

# ----------------
# class Parent:
#     def __init__(self):
#         self.msg = "hahaha"

#     def PrintMsg(self):
#         print(self.msg)


# class Child(Parent):
#     def PrintMsg(self):
#         print("hehehe")


# c = Child()
# c.PrintMsg()  # 子类覆盖掉了父类的方法

# ----------------
# class Parent:
#     def __init__(self):
#         self.msg = "hahaha"

#     def PrintMsg(self):
#         print(self.msg)


# class Child(Parent):
#     def __init__(self):
#         self.msg2 = "hehehe"


# c = Child()
# # c.PrintMsg()  # 子类覆盖掉了父类的方法，会报错，找不到msg
# # print(c.msg)  # 想要去打印Parent里的msg，此时就会报错

# ---------------------
# class Parent:
#     def __init__(self):
#         self.msg = "hahaha"

#     def PrintMsg(self):
#         print(self.msg)


# class Child(Parent):
#     def __init__(self):
#         Parent.__init__(self)  # 显示的调用一下父类的初始函数，简单粗暴，但是不是很方便
#         self.msg2 = "hehehe"


# c = Child()
# c.PrintMsg()
# print(c.msg)  # 正常打印父类的hahaha
# print(c.msg2)

# ----------------
# class Parent:
#     def __init__(self):
#         self.msg = "hahaha"

#     def PrintMsg(self):
#         print(self.msg)


# class Child(Parent):
#     def __init__(self):
#         super().__init__()  # super()可以获取到父类对象的引用，然后.__init__也是去调用父类的初始函数
#         self.msg2 = "hehehe"


# c = Child()
# c.PrintMsg()
# print(c.msg)  # 正常打印父类的hahaha
# print(c.msg2)

# ----------------多态：不需要知道类型也能去使用--------------------------------
# 从函数实现者的角度看，并不知道x和y的类型
# 但是知道x和y支持相加操作，不管是啥类型，都往一起相加
# 就是python中的多态
# def add(x, y):
#     return x + y


# print(add(10, 20))
# print(add('hello', 'world'))
# print(add([1, 2, 3], [4, 5, 6]))

# ----------------常用内建函数--------------------------------
# class Parent:
#     pass
# class Child(Parent):
#     pass
# print(issubclass(Child, Parent))  # 判断child是不是Parent的子类

# class Parent:
#     pass
# a = Parent()
# print(isinstance(a, Parent))  # 判断一个对象是不是一个类的实例

# -------------hasattr,getattr,setattr,delattr 运行时修改-------------------------
# class C:
#     val = 100

#     def Function(self):
#         print("hehe")


# print(getattr(C, 'val'))  # 获取到了val的值
# print(getattr(C, 'Function'))  # 获取到了函数
# print(delattr(C, 'val'))  # 删除了val，所以打印了None
# # print(C.val)  # 上一步删除了val所以这里val打印会报错
# print(hasattr(C, 'val'))

# class C:
#     pass
# print(dir(C))  # 打印类/对象的所有属性和方法
# print(vars(C))  # dir只返回属性，但是vars把值也取出来了

# ----------------特殊函数---------------------------
class Time:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f"{self.hour}:{self.minute}"

    def __len__(self):
        return len(f"{self.hour}:{self.minute}")


time = Time(15, 20)
print(time)
print(len(time))
