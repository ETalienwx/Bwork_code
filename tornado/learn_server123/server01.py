import tornado.web
import tornado.ioloop


# 类比Django里的视图：视图是处理请求的get，post
class IndexHandler(tornado.web.RequestHandler):  # 响应客户端的请求
    def get(self):  # get请求执行这个
        self.write("hello world! My name is alien！")
    # def post(self):  # post请求执行这个
    #     pass


if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/", IndexHandler)  # 在浏览器上输入ip+端口后，执行响应我这个IndexHandler
    ])
    app.listen(8000)  # 绑定监听端口号
    tornado.ioloop.IOLoop.current().start()  # 开启I/O循环，开启监听
