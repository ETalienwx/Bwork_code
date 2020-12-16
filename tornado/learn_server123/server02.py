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
    httpServer.listen(8000)

    tornado.ioloop.IOLoop.current().start()
