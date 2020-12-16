# index里面都是我的handler

import tornado.web
import json
import os.path
import config


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.reverse_url("aliengood")  # 对应路由属性的name值，他会找到name属性的值所对应的路由
        self.write("<a href='%s'>去另一个界面</a>" % (url))
# self.reverse_url("alien")会获取到name为”aliengood“的路由的正则匹配


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is home!")


class HelloHandler(tornado.web.RequestHandler):
    # 接收参数的函数，该方法会在http之前执行（也就是在get和post之前）
    def initialize(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def get(self):
        print(self.word1, self.word2)
        self.write("This is helloHandler!")


class AlienHandler(tornado.web.RequestHandler):
    def initialize(self, word3, word4):
        self.word3 = word3
        self.word4 = word4

    def get(self):
        print(self.word3, self.word4)
        self.write("This is AlienHandler!")


class liuyifeiHandler(tornado.web.RequestHandler):
    def get(self, h1, h2, h3):
        print(h1, h2, h3)
        self.write("liuyifei")


class zhangmanyuHandler(tornado.web.RequestHandler):
    # # 每个参数都对应一个接收：http://10.23.27.26:9000/zhangmanyu?a=1&b=2&c=3
    # def get(self):
    #     a = self.get_query_argument("a", default=100, strip=True)
    #     b = self.get_query_argument("b", default=100, strip=True)
    #     c = self.get_query_argument("c", default=100, strip=True)
    #     print(a, b, c)
    #     self.write("zhangmanyu")

    # # 有两个a的赋值：http://10.23.27.26:9000/zhangmanyu?a=1&a=2&c=3
    def get(self):
        alist = self.get_query_arguments("a")
        c = self.get_query_argument("c", default=100, strip=True)
        print(alist[0], alist[1], c)
        self.write("zhangmanyu")
# self.get_query_argument(name, default=ARG_DEFAULT, strip=True)
# 能将get方法里的参数拿出来
# name：从get请求参数字符串中返回指定参数的值，如果出现多个同名参数，返回最后一个值
# default：设置未传参数时，该参数的默认值，如果参数不存在，default也没有设置，会抛出tornado.web.MissingArgumentError（缺少参数）异常
# strip：表示是否过滤掉参数左右两边的空白字符，默认为true过滤
# self.get_query_arguments(name, strip=True)


class PostfileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('postfile.html')

    def post(self):
        name = self.get_body_argument("name")
        passwd = self.get_body_argument("passwd")
        hobbylist = self.get_body_arguments("hobby")
        print(name, passwd, hobbylist)
        self.write("This is postfileHandler！")
# self.get_body_argument(name, default=ARG_DEFAULT, strip=True)
# self.get_body_argument(name, strip=True)
# 获取post方法传递的参数

# 既可以获取get也可以获取post，一般不会选用这种方式
# get_argument(name, default=ARG_DEFAULT, strip=True)
# get_arguments(name, strip=True)


class zhuyinHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.method)
        print(self.request.host)
        print(self.request.uri)
        print(self.request.path)
        print(self.request.query)
        print(self.request.version)
        print(self.request.headers)
        print(self.request.body)
        print(self.request.remote_ip)
        print(self.request.files)
        self.write("This is zhuyinHandler!")


class UpfileHander(tornado.web.RequestHandler):
    def get(self):
        self.render('upfile.html')  # render就是渲染的意思，在浏览器中渲染出upfile.html这个文件的内容

    def post(self):
        # files = self.request.files  # 把这个文件取出来了
        # print(files)
        # 打印这个files（这个files是一个对象），里面是一个字典

        filesDict = self.request.files
        for inputname in filesDict:
            fileArr = filesDict[inputname]
            for fileObj in fileArr:
                # 指定上传文件的存储路径
                filePath = os.path.join(config.BASE_DIR, 'upfile/' + fileObj.filename)  # 指定放到upfile里面，名字为fileObj.filename
                with open(filePath, 'wb') as f:
                    f.write(fileObj.body)  # 把文件的body写进去，内容为fileObj.body
        self.write("ok")


# 服务器响应部分
class WriteHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hhhhhhhhhhhhhhh")
        self.write("jjjjjjjjjjjjjjj")
        self.write("kkkkkkkkkkkkkkk")
        # 刷新缓冲区，关闭当次请求通道
        # 在finish下面就不要write
        self.finish()
        self.write("lllllllllllllll")


class Json1Handler(tornado.web.RequestHandler):
    def get(self):
        per = {
            "name": "alien",
            "age": 18,
            "height": 170,
            "weight": 100
        }
        # 手动将字典转换成json类型的字符串
        jsonStr = json.dumps(per)
        self.set_header('Content-Type', 'application/json;charset=UTF-8')  # Content-Type: application/json;charset=UTF-8
        self.set_header('hello', 'world')  # 也可以自己设置值Hello: world
        self.write(jsonStr)
# json.dump()是将字典转换成json字符串的
# self.set_header(name.value)设置响应头的，名为name的value值，写在get或者post方法里面都可以


# 建议用这个。因为content-type为Application/json
class Json2Handler(tornado.web.RequestHandler):
    def get(self):
        per = {
            "name": "ETalien",
            "age": 18,
            "height": 170,
            "weight": 100
        }
        self.write(per)  # 直接用write返回字典


class HeaderHandler(tornado.web.RequestHandler):
    def set_default_headers(self):  # 需要重写方法
        self.set_header('Content-Type', 'text/html')

    def get(self):  # 包含了set_default_headers里面的header
        self.set_header('alien', 'hello')

    def post(self):  # 包含了set_default_headers里面的header
        pass
# set_default_headers() 在http响应处理方法之前被调用，可以重写该方法，来预先设置默认的headers
# 统一写在set_default_headers() 方法里面，在get和post里面就可以不用写了
# 注意：在http处理方法中使用set_header设置的header会覆盖set_default_headers设置的默认header


class StatusCodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(404)  # 1.设置为正常值Status Code: 404 Not Found
        # self.set_status(999, "who?where?what?")  # 2.设置为自定义的值
        # self.set_status(999)  # 3.无描述，也不是正常值会报错
        self.write("################################")
# self.set_status(status_code, reason=None) 作用：为响应设置状态码
# 参数status_code为状态码类型，为整数
# reason描述状态码的词组，str类型
# 如果reason的值为None，则状态码必须为正常值


class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/')
# 重定向，self.redirect(url) 作用：重定向到url


class ISErrorHandler(tornado.web.RequestHandler):
    def write_error(self, status_code):
        if status_code == 500:
            code = 500  # 返回500界面
            self.write("服务器内部错误")
        elif status_code == 404:
            code = 404
            self.write("资源不存在")
        self.set_status(code)

    def get(self):
        flag = self.get_query_argument("flag")
        if flag == '0':
            self.send_error(500)
        self.write("you are write")
# self.set_error(status_code = 500, **kwargs) 作用：可以抛出HTTP错误状态码，默认为500
# 抛出错误后tornado会调用write_error方法进行处理，并返回给浏览器错误页面
# write_error(status_code, **kwargs) 作用：处理send_error抛出的错误信息，并返回给浏览器错误界面
# 在send_error之后就不要再响应输出了
