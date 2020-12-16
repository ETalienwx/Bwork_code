import tornado.web
import tornado.ioloop
# 引入httpserver模块
import tornado.httpserver


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world! My name is alien！")


if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/", IndexHandler)
    ])
    # app.listen(8000)  # 这里使用listen创建了一个服务器

    # 这里手动创建服务器
    httpServer = tornado.httpserver.HTTPServer(app)
    # 绑定端口
    # httpServer.listen(8000)
    httpServer.bind(8000)  # 这里只进行绑定操作
    httpServer.start(5)  # 起五个进程（多进程）
    # 虽然tornado给我们提供了一次性启动多个进程的方式，但是由于一些问题，不建议使用上面的start方式开启多进程
    # 建议手动启动多个进程，并且还能绑定多个端口号
    # 问题
    # 1.每个子进程都会从父进程中复制一份IOLoop的实例，如果在创建子进程前修改了IOLoop，会影响所有的子进程
    # 2.所有的进程都是由一条命令启动的，无法做到在不停止服务的情况下修改代码
    # 3.所有进程共享一个端口，想要分别监控很困难
    tornado.ioloop.IOLoop.current().start()
