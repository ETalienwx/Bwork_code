# 通过命令获取latency
import subprocess
from enum import Enum


class BaseInfo(object):
    def from_dict(self, meta: dict):
        props = self.__dict__
        for k in props:
            v = meta.get(k, None)
            setattr(self, k, v)

    def to_dict(self) -> dict:
        props = {}
        for k, v in self.__dict__.items():
            value = v
            if v.__class__.__base__ is Enum:
                value = v.value
            props[k] = value
        return props


class SrtResult(BaseInfo):
    def __init__(self):
        super(SrtResult, self).__init__()
        self.command = None
        self.stdout = None
        self.stderr = None
        self.timeout = None
        self.killed = False


def pull_stream(live_address):
    command = "ffmpeg_latency_checking -loglevel warning -i {live_address} output.flv"
    args = dict(
        shell=True,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        timeout=2
    )
    result = SrtResult()
    result.command = command.format(live_address=live_address)
    result.timeout = 2
    try:
        result_str = subprocess.check_output(command, **args).decode('utf-8')
        result.stdout = result_str
    except subprocess.TimeoutExpired as exception:
        result.killed = True
        if exception.stdout is not None:
            result.stdout = exception.stdout.decode('utf-8')
        if exception.stderr is not None:
            result.stderr = exception.stderr.decode('utf-8')
    return result_str


def main():
    # live_address = "https://d1--cn-gotcha04.bilivideo.com/live-bvc/614977/live_52926766_1129961_1500.flv?cdn=cn-gotcha04&expires=1597313569&len=0&oi=3030954244&pt=web&qn=150&trid=231d6b508bd945509eb2fbe8cea9820d&sigparams=cdn,expires,len,oi,pt,qn,trid&sign=15ae8ad3e683ae65309879e80440ed4b&ptype=0&src=9&sl=6&order=1&platform=web&pSession=nc5c6ss3-0hHk-4j1Y-beQj-HHZ5zDhaNkHz"
    live_address = "rtmp://172.16.0.50/mylive/1998"
    res = pull_stream(live_address)
    print(res)


if __name__ == '__main__':
    main()