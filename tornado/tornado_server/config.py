# config里都是我的配置

import os.path

BASE_DIR = os.path.dirname(__file__)  # 生成我当前文件所在的目录的绝对路径
# 参数
options = {
    "port": 9001
}

# 配置
settings = {
    "debug": True,
    "static_path": os.path.join(BASE_DIR, "static"),
    "template_path": os.path.join(BASE_DIR, "templates")
}
