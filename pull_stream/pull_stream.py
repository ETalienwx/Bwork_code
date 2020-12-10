# 拉取源站视频流
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


def pull_stream(url):
    command = "ffprobe -show_packets -loglevel warning {url}"
    pull_command = command.format(url=url)
    args = dict(
        shell=True,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        timeout=2,
    )
    result = SrtResult()
    result.command = pull_command
    result.timeout = 2
    try:
        result_str = subprocess.check_output(pull_command, **args)
        result.stdout = result_str
    except subprocess.TimeoutExpired as exception:
        result.killed = True
        if exception.stdout is not None:
            result.stdout = exception.stdout.decode('utf-8')
        if exception.stderr is not None:
            result.stderr = exception.stderr.decode('utf-8')
    packet_start = result.stdout.find("[PACKET]")
    packet_end = result.stdout.find("[/PACKET]") + 9
    packet_str = result.stdout[packet_start:packet_end]
    result.stdout = packet_str
    print(result.to_dict())


def main():
    pull_stream("http://cn-shyp-office-live-01.bilibili.co/live-bvc/live_52926766_1129961_1500.flv")


if __name__ == '__main__':
    main()