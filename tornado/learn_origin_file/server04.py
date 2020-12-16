# # 从命令行导入参数用法
# # 想用外部变量的值的时候就要先定义变量（options.define（））
# # 然后在接收保存该变量options.parse_command_line()
# # 然后在使用options.options.变量名

# # -*- coding: utf-8 -*
# import tornado.web
# import tornado.ioloop
# import tornado.httpserver
# # 引入tornado.options模块
# import tornado.options

# # tornado.options.define(name, default, type, help, multiple)
# # name：选项变量名，必须保证唯一性，否则会报错“options ’xxx‘ already define ...”
# # default：设置选项变量的默认值，默认为none
# # type：设置选项变量的类型，从命令行或配置文件导入参数时，tornado会根据类型转换输入的值。
# # 转换不成会出错。可以是str，int，float，datetime。
# # 如果没有设置type，会根据default的值进行转换。如果default没有设置就不进行转换
# # multiple：设置选项变量是否可以为多个值，默认为false
# # help：选项变量的帮助提示信息
# # 定义了两个变量
# tornado.options.define("port", default=8000, type=int)
# tornado.options.define("list", default=[], type=str, multiple=True)

# # tornado.options.options 全局的options对象，所有定义的选项变量都会作为该对象的属性
# # 只要我们用define定义的变量，都会成为tornado.options.options对象的属性


# class IndexHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("hello world! My name is alien！")


# if __name__ == '__main__':
#     # tornado.options.parse_command_line() 转换命令行参数
#     # （就是能从命令行把参数转换进来，不用写参数，转换后的参数保存在了tornado.options.options）
#     # 转换变量的值
#     tornado.options.parse_command_line()
#     print("list = ", tornado.options.options.list)
#     app = tornado.web.Application([
#         (r"/", IndexHandler)
#     ])
#     httpServer = tornado.httpserver.HTTPServer(app)
#     httpServer.bind(tornado.options.options.port)  # 使用这个变量的值
#     httpServer.start(5)
#     tornado.ioloop.IOLoop.current().start()

#     # python server04.py --port=9000 --list=hello,world,hello,bit
#     # 执行上述命令行会启动服务器并打印如下内容
#     # list =  ['hello', 'world', 'hello', 'bit']
#     # [I 191121 14:16:33 process:126] Starting 5 processes

# ------------------------------------------------------------------------------------------------------
# 从配置文件导入参数

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options


tornado.options.define("port", default=8000, type=int)
tornado.options.define("list", default=[], type=str, multiple=True)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")


# 先创建一个config的普通文件
if __name__ == "__main__":
    # tornado.options.options.logging = None
    tornado.options.parse_config_file("config")
    print(tornado.options.options.list)
    app = tornado.web.Application([
        (r"/", IndexHandler)
    ])
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(tornado.options.options.port)
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()
# 说明：书写格式仍需要按照python的语法要求来写
# 不支持字典类型
