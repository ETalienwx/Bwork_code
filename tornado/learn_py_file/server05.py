# 从config.py中导入参数
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import config  # 引入我自己写的config.py包


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")


# 先创建一个config.py的普通文件
if __name__ == "__main__":
    print(config.options.list)
    app = tornado.web.Application([
        (r"/", IndexHandler)
    ])
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options.port)
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()

# 当我们在代码中使用parse_command_line() 或 parse_config_file()方法时，tornad会默认开启loging模块功能
# 他会向我们的屏幕终端输出一些打印信息，你要是不想看也可以关闭
# 配置文件关闭用：tornado.options.options.loging=None(写在程序一开始的位置)
# 命令行关闭用：python3 server.py --port=8080 --list=hello,world --logging=None
