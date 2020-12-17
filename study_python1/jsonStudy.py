import json
import os.path

dic_list = []
dic = {"name": "1.png", "url": "https://21213"}
dic_list.append(dic)
filename = "2.png"
for i in range(3):
    tmp = {"name": filename, "url": os.path.join(os.path.dirname(__file__), filename)}
    dic_list.append(tmp)
json_str = json.dumps(dic_list)
print(json_str)
