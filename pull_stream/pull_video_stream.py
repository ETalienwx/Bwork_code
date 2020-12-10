# 拉取视频流
import subprocess
import requests
from multiprocessing import Process
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


def download_file(url):
    print(url)

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, stream=False, timeout=2).content
        with open('input.flv', 'wb') as f:
            f.write(response)
    except Exception as e:
        print(e)

    # try:
    #     req = request.Request(url)
    #     req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36")
    #     response = request.urlopen(req).read()
    #     with open('input.flv', 'wb') as f:
    #         f.write(response)
    # except Exception as e:
    #     print(e)

    print("download file success!")


def pull_first_packet():
    command = "ffprobe -show_packets input.flv"
    args = dict(
        shell=True,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        timeout=2,
    )
    result = SrtResult()
    result.command = command
    result.timeout = 2
    try:
        result_str = subprocess.check_output(command, **args)
        result.stdout = result_str
    except subprocess.TimeoutExpired as exception:
        result.killed = True
        if exception.stdout is not None:
            result.stdout = exception.stdout.decode('utf-8')
        if exception.stderr is not None:
            result.stderr = exception.stderr.decode('utf-8')
    packet_start = result.stdout.find("[PACKET]")
    packet_end = result.stdout.find("[/PACKET]") + 9
    packer_str = result.stdout[packet_start:packet_end]
    result.stdout = packer_str
    print(result.to_dict())


def main():
    url = "http://bvcflow2.bilibili.co/proxy/?http://10.68.68.166:2281/bbqxcode2/37/57/m200805wssvid1596627570021505737-1-720p-2m-264.mp4"
    download_process = Process(target=download_file, args=(url, ))
    print('download_process process will start.')
    download_process.start()
    download_process.join()
    print('download_process process end.')
    pull_first_packet()


if __name__ == '__main__':
    main()
