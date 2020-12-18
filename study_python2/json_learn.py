import json_tools


def jsonDiff():
    a = {"code": 0,"message": "success"}
    b = {"code": 0,"message": "success"}
    result = json_tools.diff(a, b)
    print(result)


if __name__=="__main__":
    jsonDiff()