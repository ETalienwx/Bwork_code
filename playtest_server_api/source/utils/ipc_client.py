# -*- coding: utf-8 -*-
import os
import sys
import shlex
import logging
import settings
import ujson as json
from subprocess import Popen


def ensure_fifo(path):
    if os.path.exists(path):
        os.unlink(path)
    os.mkfifo(path)


class IPCClient(object):
    HANDLE = os.path.exists(settings.IPC_HANDLER_PATH)

    @classmethod
    def start_server(cls):
        if not cls.HANDLE:
            logging.info(f"Starting IPCServer ....")
            ensure_fifo(settings.IPC_HANDLER_PATH)
            python_exe_path = sys.executable
            entrance_path = os.path.join(settings.SOURCE_ROOT, "app", "ipc_server.py")
            cmd = f"{python_exe_path} {entrance_path}"
            args = shlex.split(cmd)
            cls.HANDLE = Popen(args)
        logging.info(f"IPCServer started in Process {cls.HANDLE.pid}")

    @classmethod
    def stop_server(cls):
        logging.info(f"Stopping IPCServer {cls.HANDLE.pid} ....")
        cls._call_server("stop")
        # No logging should be made after server stopping,
        # otherwise client side will be blocked by writing
        # to a fifo with out a read open process
        if cls.HANDLE:
            cls.HANDLE.wait(10)
        cls.HANDLE = None

    @classmethod
    def report_event(cls, **kwargs):
        cls._call_server("_report_event", **kwargs)

    @classmethod
    def send_logging(cls, **kwargs):
        cls._call_server("_send_logging", **kwargs)

    @classmethod
    def _call_server(cls, func, **kwargs):
        if cls.HANDLE:
            with open(settings.IPC_HANDLER_PATH, 'w', buffering=1) as pipeout:
                request_data = {
                    "func": func,
                    "args": kwargs
                }
                ipc_content = json.dumps(request_data) + os.linesep
                if len(ipc_content) >= 4096:
                    logging.warning("Over 4K FIFO Write is not atomic and may be corrupted")
                pipeout.write(ipc_content)


class IPCContext(IPCClient):
    def __enter__(self):
        self.start_server()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_server()


class IPCEventReporter(IPCClient):
    EVENT_START = "start"
    EVENT_END = "end"

    @staticmethod
    def PROGRAM_NAME(cmd):
        program, args = cmd.split(" ", 1)
        program = os.path.basename(program)
        if "python" in program:
            program = args.split(" ", 1)[0]
            program = os.path.basename(program)
        elif "hadoop fs" in program:
            program = "hadoop"
        return program

    @classmethod
    def __report(cls, cmd, event):
        # FIXME: It's a little dirty here,
        # We are unable to get Job_ID from Job module,
        # which is written during the run time
        # Try to find a fix for it
        event_data = {
            "vxcode_id": settings.SWARM_JOB_ID,
            "program": cls.PROGRAM_NAME(cmd),
            "cmd": cmd,
            "event": event
        }
        IPCClient.report_event(**event_data)

    @classmethod
    def start_cmd(cls, cmd):
        cls.__report(cmd, cls.EVENT_START)

    @classmethod
    def end_cmd(cls, cmd):
        cls.__report(cmd, cls.EVENT_END)
