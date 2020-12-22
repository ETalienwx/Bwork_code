# -*- coding: utf-8 -*-
import os
from logging import INFO
from importlib import import_module
from settings.envs.dev import *

APP_PORT = 80
SETTINGS_ROOT = os.path.dirname(os.path.realpath(__file__))
SOURCE_ROOT = os.path.dirname(SETTINGS_ROOT)
PROJECT_ROOT = os.path.dirname(SOURCE_ROOT)
CONF_ROOT = os.path.join(PROJECT_ROOT, "conf")
HADOOP_CONF_ROOT = os.path.join(CONF_ROOT, "hadoop")
README_PATH = os.path.join(PROJECT_ROOT, "README.md")
ENVS_ROOT = os.path.join(SETTINGS_ROOT, "envs")

ENV = os.getenv("SETTING_ENV", "dev")
ENVS = filter(lambda r: r != '__init__',
              [os.path.splitext(env)[0] for env in
               os.listdir(ENVS_ROOT)])
IS_LOCAL_TEST = "dev" in ENV
print(f"Load settings for queen [{ENV}]")
SWARM_IN_TEST = "dev" in ENV
SWARM_IN_PRODUCT = "prod" in ENV
SWARM_IN_DOCKER = os.path.exists("/.dockerenv")
IPC_HANDLER_PATH = "/tmp/ipc.fifo"
EDGE_LOG_TEMPLATE = '{instance_id}|{level}|{lineno}|{job_id}|{queen}|{log}|{module}'
SWARM_QUEEN = os.getenv("SWARM_QUEEN", "dev")

OPS_LOG_SOCKET = '/var/run/lancer/collector.sock'
OPS_LOG_APP_ID = 'video.bvc_network.srt_playtest'  # 用来在ops-log上查找日志的key
LOGGING_LEVEL = INFO
SENTRY_DSN = 'https://18d30fcd3e3a411ab9496af38ba75ad1@o375870.ingest.sentry.io/5195949'
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Shanghai')


# overwrite setting
if ENV in ENVS:
    print(f"Load settings for transcode scheduler [{ENV}]")
    cur_env = import_module('settings.envs.' + ENV)
    names = [name for name in dir(cur_env) if not name.startswith('__')]

    g = globals()
    for name in names:
        g[name] = getattr(cur_env, name)
