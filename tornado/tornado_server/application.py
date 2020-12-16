# application里面都是我的路由

import tornado.web
from views import index
import config  # 引入我的配置文件


class Application(tornado.web.Application):
    def __init__(self):
        handers = [
            (r'/', index.IndexHandler),
            (r'/home', index.HomeHandler),

            # 这是我们写服务器的时候，手动给handler传的参数
            (r'/hello', index.HelloHandler, {"word1": "hello", "word2": "world"}),

            # name是用于标记这个页面的，以防我的正则发生变化（反向解析）
            tornado.web.url(r'/alien', index.AlienHandler, {"word3": "world", "word4": "hello"}, name="aliengood"),

            # uri
            # 在浏览器中取的值，服务器中也可以获取到，如下获取路由的特定部分：http://10.23.27.26:9000/liuyifei/hello/world/hhh
            (r'/liuyifei/(\w+)/(\w+)/(\w+)', index.liuyifeiHandler),
            # (r'/liuyifei/(?P<h1>\w+)/(?P<h3>\w+)/(?P<h2>\w+)', index.liuyifeiHandler),  # 规定了顺序

            # get
            # 用get方法传参:http://10.23.27.26:9000/zhangmanyu?a=1&b=2&c=3
            # http://10.23.27.26:9000/zhangmanyu?a=1&a=2&c=3
            (r'/zhangmanyu', index.zhangmanyuHandler),

            # post
            (r'/postfile', index.PostfileHandler),

            # request对象
            (r'/zhuyin', index.zhuyinHandler),

            # 上传文件
            (r'/upfile', index.UpfileHander),

            # write
            (r'/write', index.WriteHandler),

            (r'/json1', index.Json1Handler),
            (r'/json2', index.Json2Handler),
            (r'/header', index.HeaderHandler),
            (r'/status', index.StatusCodeHandler),  # 状态码
            (r'/index', index.RedirectHandler),  # 重定向
            # iserror？flag=2
            (r'/iserror', index.ISErrorHandler)
        ]
        # 我让父对象的init函数知道我的配置文件
        # super(Application, self).__init__(handers, debug=True, ...)
        # 如上我们也可以把配置文件跟在后面写，但是显得比较乱，所以我们放在配置文件里面
        # **config.settings就相当于把键值对拿出来了
        super(Application, self).__init__(handers, **config.settings)

# 请求
# 配置
# settings
# debug:
# 设置tornado是否工作在调试模式下，默认为false即工作在生产模式下。开发的时候设置为true，就是改动代码之后不需要重启服务，提高开发的效率。上线之后就要设置为false
# true的特性：自动重启---tornado应用会监控源代码文件，当有改动时便会自动重启服务器，可减少手动重启的次数，提高开发效率
#                   ---如果保存之后代码有错误会导致重启失败，修改错误后需要手动重启
#                   ---可以应用autoreload = True设置
#           取消缓存编译的模板
#                   ---开发阶段不想使用缓存，complied_template_cache = False可以单独设置，默认为True
#           取消缓存静态文件的hash值
#                   ---你改了css，但是网页上没改
#                   ---static_hash_cache = False单独设置
#           提供追踪信息
#                   ---serve_traceback = True来单独设置
# static_path：设置静态文件目录
# template_path：设置模板文件目录

# 路由
# (r'/', index.IndexHandler)前面是正则表达式，匹配成功后执行后面的handler
# 路由传参
# (r'/hello', index.HelloHandler, {"word1":"hello", "word2":"world"})
# 用这个方法接收参数 def initialize(self, word1, word2):
# 赋值给self 然后再在get方法里使用
# 该方法会在http之前调用（也就是在get和post之前调用）

# 有以下三种写法
# (r'/home', index.HomeHandler),
# # 这是我们写服务器的时候，手动给handler传的参数，传参的时候需要重写initialize方法来获取服务器传递过来的参数
# (r'/hello', index.HelloHandler, {"word1": "hello", "word2": "world"})
# # name属性是用于标记这个页面的，以防我的正则发生变化（反向解析），不能使用元组定于路由，得用tornado.web.url
# tornado.web.url(r'/alien', index.AlienHandler, {"word3": "world", "word4": "hello"}, name="aliengood")

# tornado.web.RequestHandler
# 作用：利用HTTP协议向服务器传递参数
# 提取uri的特定部分、
# get方式传递参数，
# post方式传递参数，
# 既可以获取get请求，也可以获取post请求
# 在http报文的头中增加自定义的字段


# request对象：储存了关于请求的相关信息
# method:http请求的方式
# host：请求的主机名
# uri：请求的完整资源地址，包括路径和get查询参数部分
# path：请求路径部分
# query：请求参数部分
# version：使用http版本
# header：请求的协议头，是一个字典类型
# body：请求体数据
# remote_ip：客户端的ip
# files：用户上传的文件类型，用字典描述这个文件的属性
#    {
#         'file': [
#             {
#                 'filename': 'a.txt',
#                 'body': b'内容',
#                 'content_type': 'text/plain'
#             }
#         ]
#         'img':[
#             {
#                 'filename': 'hhh.png',
#                 'body': b'hhhhhhhhhhhhhhh'
#                 'content_type': 'image/png'
#             }
#         ]
#     }

# tornado.httputil.HTTPFile对象：是接受到的文件对象
# 属性：filename文件的实际名字 body文件的数据实体 content_tyoe文件的类型

# 响应
# write：self.write(chunk) 将chunk数据写到输出缓冲区上
