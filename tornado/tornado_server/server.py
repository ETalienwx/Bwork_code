# 服务器都在server里面

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import config
# from views import index
import application

if __name__ == "__main__":
    app = application.Application()
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options["port"])
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()
