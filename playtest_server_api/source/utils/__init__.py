# -*- coding: utf-8 -*-
import os
import stat
import socket
import signal
import hashlib
import logging
import requests
import settings
import ujson as json
import logging.handlers
from logging import Formatter
from urllib.parse import urlencode
from importlib import import_module
from concurrent.futures import ThreadPoolExecutor
from utils.billions_logger.jsonlogger import JsonFormatter
from utils.billions_logger.lancerhandler import LancerStream
from utils.lancer_logger.logger import IPCLogFormatter, IPCLogHandler

OPS_LOG_SOCKET = '/var/run/lancer/collector.sock'

KB = lambda b: b << 10
MB = lambda b: b << 20
GB = lambda b: b << 30


def get_hostname():
    return socket.gethostname()


def get_class_name(obj):
    return obj.__class__.__name__


def is_socket(fpath):
    return os.path.exists(OPS_LOG_SOCKET) and \
           stat.S_ISSOCK(os.stat(fpath).st_mode)


def init_local_log(logging_level=logging.INFO):
    fmt = '[%(levelname)1.1s %(asctime)s %(module)-16.16s:%(lineno)4d] %(message)s'
    date_fmt = '%y%m%d %H:%M:%S'
    logging.basicConfig(format=fmt, datefmt=date_fmt, level=logging_level)
    if os.path.exists("/data/log/bili-vxcode"):
        LOGGING_ROOT = f"/data/log/bili-vxcode/{settings.PROJECT_NAME}.log"
        opslogHandler = logging.handlers.RotatingFileHandler(LOGGING_ROOT, maxBytes=MB(100), backupCount=5)
        formatter = Formatter(fmt, date_fmt)
        opslogHandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(logging_level)
        logger.addHandler(opslogHandler)


def init_ops_log(job_id, level=logging.INFO, **kwargs):
    if is_socket(OPS_LOG_SOCKET):
        logging.info(f"OPS-log socket detected @{OPS_LOG_SOCKET}")
        init_udp_lancer_log(job_id, level, **kwargs)
    elif settings.SWARM_IN_PRODUCT:
        logging.info(f"OPS-log through HTTP LogStream")
        init_http_lancer_log(job_id, level, **kwargs)
    else:
        logging.info("OPS-log is disabled as no socket detected")


def init_udp_lancer_log(job_id, level=logging.INFO, **kwargs):
    if settings.OPS_LOG_APP_ID:
        fmt = '[%(levelname)1.1s %(asctime)s %(module)-16.16s:%(lineno)4d] %(message)s'
        opslogHandler = logging.StreamHandler(stream=LancerStream(settings.OPS_LOG_TASK_ID,
                                                                  OPS_LOG_SOCKET))
        opslogformatter = JsonFormatter(fmt=fmt,
                                        additional_fields={
                                            'app_id': settings.OPS_LOG_APP_ID,
                                            "job_id": job_id,
                                            "queen": settings.SWARM_QUEEN,
                                            **kwargs
                                        })
        opslogHandler.setFormatter(opslogformatter)
        logger = logging.getLogger()
        logger.setLevel(level)
        logger.addHandler(opslogHandler)
    else:
        logging.info("Please specify OPS_LOG_APP_ID to enable OPS-log")


def init_http_lancer_log(job_id, level=logging.INFO, **kwargs):
    if settings.EDGE_LOG_ID:
        logger = logging.getLogger()
        loghandler = IPCLogHandler()
        formatter = IPCLogFormatter(settings.EDGE_LOG_TEMPLATE,
                                    prefix=settings.EDGE_LOG_ID,
                                    additional_fields={
                                        "job_id": job_id,
                                        "queen": settings.SWARM_QUEEN,
                                        **kwargs
                                    })
        loghandler.setFormatter(formatter)
        logger.addHandler(loghandler)
        logger.setLevel(level)
    else:
        logging.info("Please specify EDGE_LOG_ID to enable EDGE-log")


def hash_md5(msg, raw=False):
    md5 = hashlib.md5()
    md5.update(msg.encode())
    if raw:
        return md5.digest()
    else:
        return md5.hexdigest()


def register_exit_handler(signal_handler):
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)


class Serializable(object):
    @property
    def data(self):
        return self.__dict__

    @property
    def serialization(self):
        return json.dumps(self.__dict__, sort_keys=True)

    @property
    def signature(self):
        return hash_md5(self.serialization)

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)


class VXCodeKnownError(Exception):
    def __init__(self):
        self.err_dict = {
            'error_type': get_class_name(self),
            'error_details': dict(),
            'should_retry': False,
            'reporter': get_hostname(),
        }

    def __str__(self):
        return str(self.err_dict)

    def __repr__(self):
        return repr(self.err_dict)


def generate_error_ctx(ex):
    if isinstance(ex, VXCodeKnownError):
        error_ctx = ex.err_dict
    else:
        error_ctx = {
            'error_type': get_class_name(ex),
            'error_details': {
                'msg': str(ex),
            },
            'should_retry': True,
            'reporter': get_hostname(),
        }
    return error_ctx


class ExecutionError(VXCodeKnownError):
    MAX_LOG_SIZE = KB(2)

    def __init__(self, result):
        super(ExecutionError, self).__init__()
        result.update({
            "stdout": result["stdout"][:self.MAX_LOG_SIZE],
            "stderr": result["stderr"][:self.MAX_LOG_SIZE],
        })
        self.err_dict['error_details'].update(result)
        retcode = result["retcode"]
        if retcode == CostSupervisor.RET_TIMEOUT:
            self.err_dict['should_retry'] = True
        else:
            self.err_dict['should_retry'] = retcode < 0


def checksum_md5(path, chunksize=2 ** 12):
    result = CostSupervisor.run(f"md5sum {path}")
    md5 = result["stdout"].split(' ', 1)[0].strip()
    if result["retcode"]:
        md5 = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunksize), b''):
                md5.update(chunk)
        return md5.hexdigest()
    else:
        return md5


def supervised_run(cmd, timeout=None, progress_cb=None):
    result = CostSupervisor.run(cmd, timeout, progress_cb)
    if result["retcode"]:
        raise ExecutionError(result)
    return result


def supervised_batch_run(cmds, timeouts=None):
    if not timeouts:
        timeouts = [None] * len(cmds)
    if len(cmds) == 1:
        return [supervised_run(cmds[0], timeouts[0])]
    else:
        results = CostSupervisor.run_batch(cmds, timeouts)
        unexpected_generator = (r for r in results if r["retcode"])
        unexpected_result = next(unexpected_generator, None)
        if unexpected_result:
            raise ExecutionError(unexpected_result)
        return results


def batch_run(fn, *args_batch):
    worker_count = len(args_batch[0])
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        return list(executor.map(fn, *args_batch))


def move_file(src, dst):
    return supervised_run(f"mv {src} {dst}")


def copy_file(src, dst):
    return supervised_run(f"cp -rf {src} {dst}")


def sign_dict(data):
    return hash_md5(json.dumps(data, sort_keys=True))


def dict_difference(target, reference):
    target_type = type(target)
    reference_type = type(reference)
    if target_type != reference_type:
        return "Type mismatch: {} vs {}".format(target_type, reference_type)
    else:
        if target_type == dict:
            target_keys = set(target)
            reference_keys = set(reference)
            if target_keys != reference_keys:
                return "Dict key mismatch: target_only {} vs reference only {}".format(
                    target_keys - reference_keys,
                    reference_keys - target_keys
                )
            else:
                for k in target_keys:
                    target_value = target[k]
                    reference_value = reference[k]
                    difference = dict_difference(target_value, reference_value)
                    if difference:
                        return {"KEY_{}".format(k): difference}

        elif target_type == list:
            target_length = len(target)
            reference_length = len(reference)
            if target_length != reference_length:
                return "List length mismatch: target {} vs reference {}".format(target_length, reference_length)
            else:
                for i in range(target_length):
                    target_value = target[i]
                    reference_value = reference[i]
                    difference = dict_difference(target_value, reference_value)
                    if difference:
                        return {"IDX_{}".format(i): difference}

        else:
            if target != reference:
                return "Value mismatch: {} vs {}".format(target, reference)


def ensure_local_path(fpath):
    if os.path.isfile(fpath) or os.path.islink(fpath):
        os.unlink(fpath)
    supervised_run(f"mkdir -p {fpath}")


DEFAULT_FFPROBE_OUTPUT_FORMAT = "-of default=nk=1:nw=1"


def get_stream_bitrate(path, is_audio):
    if is_audio:
        selected_stream = "-select_streams a:0 "
    else:
        selected_stream = "-select_streams v:0 "
    cmd = f"{settings.FFPROBE_GENERAL_CMD} {selected_stream} -show_entries stream=bit_rate {DEFAULT_FFPROBE_OUTPUT_FORMAT} {path}"
    result = supervised_run(cmd)
    return int(result["stdout"])


def get_format_bitrate(path):
    cmd = f"{settings.FFPROBE_GENERAL_CMD} -show_entries format=bit_rate {DEFAULT_FFPROBE_OUTPUT_FORMAT} {path}"
    result = supervised_run(cmd)
    return int(result["stdout"])


def get_format_name(path):
    cmd = f"{settings.FFPROBE_GENERAL_CMD} -show_entries format=format_name {DEFAULT_FFPROBE_OUTPUT_FORMAT} {path}"
    result = supervised_run(cmd)
    assert result["stdout"]
    raw_format = result["stdout"]
    if "mp4" in raw_format:
        return "mp4"
    if "matroska" in raw_format:
        return "mkv"
    return result["stdout"]


def get_frame_count(path, is_audio):
    stream_select = f"-select_streams {'a:0' if is_audio else 'v:0'}"
    cmd = f"{settings.FFPROBE_GENERAL_CMD} {stream_select} -show_entries packet=null -of json {path}"
    result = supervised_run(cmd)
    if result["stdout"]:
        packet_meta = json.loads(result["stdout"]).get("packets", list())
        if packet_meta:
            return len(packet_meta)
    return 0


def get_codec_name(input_path, is_audio):
    if is_audio:
        stream_select = "-select_streams a:0"
    else:
        stream_select = "-select_streams v:0"
    probe_cmd = f"{settings.FFPROBE_GENERAL_CMD} {stream_select} -show_entries stream=codec_name " \
                f"{DEFAULT_FFPROBE_OUTPUT_FORMAT} {input_path}"
    result = supervised_run(probe_cmd)
    return result["stdout"]


def get_format_duration(video_path):
    probe_cmd = f"{settings.FFPROBE_GENERAL_CMD} -show_entries format=duration {DEFAULT_FFPROBE_OUTPUT_FORMAT} {video_path}"
    duration_in_sec = supervised_run(probe_cmd)["stdout"]
    duration_in_sec = float(duration_in_sec) if duration_in_sec else 0
    return int(duration_in_sec * 1000)


def get_stream_discard_time(path, is_audio=False, consider_editlist=1):
    probe_params = "-ignore_editlist 0" if consider_editlist else ""
    stream_selection = "-select_streams a:0" if is_audio else "-select_streams v:0"
    cmd = f"{settings.FFPROBE_GENERAL_CMD} {probe_params} {stream_selection} " \
          f"-read_intervals %+20 -show_entries packet=pts_time,flags,duration_time -of json {path}"
    result = supervised_run(cmd)
    packets = json.loads(result["stdout"])
    packets = packets.get("packets", list())
    discard_time = 0
    # FIXME: Still some discussions on why it's implemented this way
    for packet in packets:
        if 'D' in packet["flags"]:
            discard_time += float(packet.get('duration_time', 0))
        else:
            return discard_time
    return 0


def get_stream_start_time(path, is_audio, consider_editlist):
    probe_params = "-ignore_editlist 0" if consider_editlist else ""
    stream_selection = "-select_streams a:0" if is_audio else "-select_streams v:0"
    cmd = f"{settings.FFPROBE_GENERAL_CMD} {probe_params} {stream_selection} " \
          f"-show_entries stream=start_time -of json {path}"
    result = supervised_run(cmd)
    stream_data = json.loads(result["stdout"])
    return float(stream_data["streams"][0]["start_time"])


def get_stream_types(path):
    cmd = f"{settings.FFPROBE_GENERAL_CMD} -show_entries stream=codec_type {DEFAULT_FFPROBE_OUTPUT_FORMAT} {path}"
    result = supervised_run(cmd)
    return result["stdout"]


def get_pixels_per_frame(path):
    cmd = f"{settings.FFPROBE_GENERAL_CMD} -select_streams v:0 -show_entries stream=width,height -of json {path}"
    result = supervised_run(cmd)
    if result["stdout"]:
        stream_data = json.loads(result["stdout"])["streams"]
        if stream_data:
            stream_data = stream_data[0]
            return int(stream_data["width"]) * int(stream_data["height"])
    return 0


def get_total_pixel_count(path):
    frame_count = get_frame_count(path, False)
    return frame_count * get_pixels_per_frame(path)


def get_stream_timeline(path, is_audio):
    if is_audio:
        selected_stream = "-select_streams a:0 "
    else:
        selected_stream = "-select_streams v:0 "
    cmd = f"{settings.FFPROBE_GENERAL_CMD} {selected_stream} -show_entries packet=dts -of json {path}"
    result = supervised_run(cmd)
    if result["stdout"]:
        packets = json.loads(result["stdout"]).get("packets", [])
        return [p["dts"] for p in packets]
    return list()


def calc_frame_rate(rate_str):
    if not rate_str:
        return 0
    nomin = float(rate_str.split('/')[0])
    denomin = float(rate_str.split('/')[1])
    if not denomin:
        return 0
    return nomin / denomin


def get_stream_metas(path, is_audio, items):
    entries = ",".join(items)
    stream_select = f"-select_streams {'a:0' if is_audio else 'v:0'}"
    cmd = f"{settings.FFPROBE_GENERAL_CMD} {stream_select} -show_entries stream={entries} -of json {path}"
    result = supervised_run(cmd)
    stream_metas = json.loads(result["stdout"]).get('streams', list())
    if stream_metas:
        stream_meta = stream_metas[0]
        if "r_frame_rate" in stream_meta:
            stream_meta["r_frame_rate"] = calc_frame_rate(stream_meta["r_frame_rate"])
        return stream_meta
    else:
        return dict()


def get_color_matrix(path):
    color_items = ["color_range", "color_space", "color_prime", "color_transfer"]
    cmd = f"{settings.FFPROBE_GENERAL_CMD} -select_streams v:0 -show_entries " \
          f"stream={','.join(color_items)} -of json {path}"
    result = supervised_run(cmd)
    if result["stdout"]:
        raw_matrix = json.loads(result["stdout"]).get('streams', list())[0]
        return {
            item: raw_matrix[item]
            for item in color_items
            if item in raw_matrix
        }
    return dict()


def CLIP(val, below, upper):
    tmp = max(val, below)
    return min(tmp, upper)


def LOCAL_PATH(filename):
    return os.path.join(settings.LOCAL_WORKSPACE_ROOT, filename)


def generate_curl_cmd(method, url, **kwargs):
    params = kwargs.get("params", None)
    if params:
        url += ("?" + urlencode(params))
    payload = kwargs.get("json", "")
    if payload:
        payload = f"-d '{json.dumps(payload)}'"
    else:
        payload = kwargs.get("data", "")
        if payload:
            payload = f"-d '{payload}'"

    headers = kwargs.get("headers", "")
    if headers:
        headers = " ".join([f"-H \"{k}:{v}\"" for k, v in headers.items()])
    return f"curl -X {method.upper()} \"{url}\" {payload} {headers}"


def create_hdfs_folder(folder):
    folder = folder.replace("hdfs://", "")
    supervised_run(f"runuser xcode -c 'hadoop fs -mkdir -p {folder}'")


def purge_hdfs_folder(folder):
    folder = folder.replace("hdfs://", "")
    supervised_run(f"runuser xcode -c 'hadoop fs -rm -r {folder}'")
