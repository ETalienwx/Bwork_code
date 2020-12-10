# 使用进程拉取直播流
import subprocess
import requests
import time
import os
from multiprocessing import Process, Pipe
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


def download_file(url, conn):
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
    try:
        response = requests.get(url, stream=True, headers=headers)
        with open("input.flv", "wb") as pdf:
            start = time.time()
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
                    if (time.time() - start) > 1:
                        break
    except Exception as error:
        print("Request stream url error!", error)

    if os.path.getsize("input.flv") > 0:
        print("download file success!")
        conn.send(1)
    else:
        print("download file error!")
        conn.send(-1)


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
    # 正确的流
    url = "https://d1--cn-gotcha04.bilivideo.com/live-bvc/101540/live_52926766_1129961_1500.flv?cdn=cn-gotcha04&expires=1597225352&len=0&oi=3030954244&pt=web&qn=150&trid=6b995acd90ff4d3c921aabb2cdf5c26b&sigparams=cdn,expires,len,oi,pt,qn,trid&sign=d4a051ae42471e1ea03ba7020294d19f&ptype=0&src=9&sl=2&order=1&platform=web&pSession=NjJCGpix-zYH1-4J0p-i5W4-2kcWzRswKEBa"
    # 错误的流
    # url = "https://d1--cn-gotcha04.bilivideo.com/live-bvc/208258/live_52926766_1129961_1500.flv?cdn=cn-gotcha04&expires=1597217512&len=0&oi=3030954244&pt=web&qn=150&trid=ed819650419545c09b72800ce7548c57&sigparams=cdn,expires,len,oi,pt,qn,trid&sign=5785ccd89c84f4fd9f188ed63474774d&ptype=0&src=9&sl=3&order=1&platform=web&pSession=kKbe92E4-DeC4-4QT2-penA-8mimYiXc3Ktn"
    parent_conn, child_conn = Pipe()
    download_process = Process(target=download_file, args=(url, child_conn))
    print('download_process process will start.')
    download_process.start()
    download_process.join()
    print('download_process process end.')
    if parent_conn.recv() == 1:
        pull_first_packet()
    else:
        print("stream expire!")


if __name__ == '__main__':
    main()
