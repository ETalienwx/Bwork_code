# 测试下载直播速率
import requests
import time
from loguru import logger
import eventlet

ChunkSize: int = 10 * 1024 * 1024
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"


def download_speed_hujun(url) -> float:
    with requests.get(url, stream=True, headers={"User-Agent": USER_AGENT}, timeout=10) as r:
        r.raise_for_status()
        length = 0  # in bytes
        start = time.time()
        for chunk in r.iter_content(chunk_size=8192):
            if length >= 2 * 1024 * 1024:
                break
            if chunk:
                length += len(chunk)
        total = time.time() - start  # in seconds
        mega = 1024 * 1024
        mbps = 8 * length / total / mega  # megabits/s
        mbps = round(mbps, 2)
    return mbps


def download_speed_wx(url) -> float:
    try:
        with requests.get(url, stream=True, headers={"User-Agent": USER_AGENT}, timeout=10) as res:
            if 400 <= res.status_code < 500:
                logger.info(f'download speed Client Error: {res.status_code}')
                return 0.0
            if 500 <= res.status_code < 600:
                logger.info(f'download speed Server Error: {res.status_code}')
                return 0.0
            elif res.status_code == 200:
                length = 0
                start = time.time()
                for chunk in res.iter_content(chunk_size=8 * 1024):
                    if length >= ChunkSize:
                        break
                    if chunk:
                        length += len(chunk)
                    now = time.time()
                    if now - start >= 10:
                        print('timeout')
                        break
                total = time.time() - start
                mega = 1024 * 1024
                mbps = 8 * length / total / mega
                mbps = round(mbps, 2)
                return mbps
    except Exception as e:
        logger.info(e)
        return 0.0


def download_file(url):
    response = requests.get(url, stream=True)
    with open("input.flv", "wb") as pdf:
        start = time.time()
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
                if (time.time() - start) > 1:
                    break


if __name__ == "__main__":
    start = time.time()
    d_time = download_speed_wx("https://d1--cn-gotcha04.bilivideo.com/live-bvc/807046/live_1133891791_58575124.flv?expires=1606911930&len=0&oi=3030954244&pt=web&qn=0&trid=d8aec7ee401a4e6f907558cc131fb285&sigparams=cdn,expires,len,oi,pt,qn,trid&cdn=cn-gotcha04&sign=8a93da40877847959ff984219c9456df&p2p_type=0&src=9&sl=1&platform=web&pSession=5TKEhmZW-Mza4-4trG-GAar-A8JXhsDYM00r")
    print("download_speed: ", d_time)
    end = time.time()
    print("download_speed exec time: ", end - start)


