#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-15 12:12:06
# @Author  : wangxuan
# @File    : main.py
# @Software: PyCharm
import logging
import settings
import requests
import time

from utils import init_ops_log, init_local_log

nerve_url = 'http://bvc-nerve.bilibili.co/quality/query/dns?edge=2'


def get_nerve_list():
    while True:
        try:
            nerve_response = requests.get(nerve_url, timeout=3)
            break
        except requests.exceptions.RequestException as error:
            logging.error(error)

    try:
        nerve_info_list = nerve_response.json()['data']['list']
    except Exception as error:
        logging.error(f'Get nerve json error: {error}')

    return nerve_info_list


def get_ip_list():
    nerve_list = get_nerve_list()
    ip_list = []
    for info in nerve_list:
        try:
            for idc_server in info.get('idc_server'):
                ip = idc_server.get('ip')
                ip_list.append(ip)
        except Exception as error:
            logging.error(f'Get ip list error: {error}')
    return ip_list


def get_ip_port_list(ip_list):
    n = len(ip_list)
    for i in range(0, n):
        ip_list[i] = ip_list[i] + ":1935"
    return ip_list


def create_batch_tasks(ip_port_list):
    url = 'http://uat-edgediag.bilivideo.com/tasks'
    data = {
        "name": "srt 拨测",
        "type": "srt",
        "cycle": "cron",
        "detail": {
            "run_at": "*/15 * * * *",
            "ip_ports": ip_port_list
        },
        "timeout": 3
    }
    params = {
        'su': 'mayday'
    }
    try:
        res = requests.post(url=url, json=data, params=params)
    except Exception as error:
        logging.error(f'Create batch task error: {error}')
    return res.json().get('id')


def create_task(ip_list):
    url = 'http://uat-edgediag.bilivideo.com/tasks'
    for host_ip in ip_list:
        cmd = "nc -v -u " + host_ip + " 1935"
        data = {
          "name": "srt 拨测 wx",
          "type": "command",
          "cycle": "onetime",
          "detail": {
              "cmd": cmd,
              "stdin": None,
              "output_path": None,
              "timeout": 3
          }
        }
        params = {
            'su': 'mayday'
        }
        try:
            res = requests.post(url=url, json=data, params=params)
        except Exception as error:
            logging.error(f'Create task error: {error}')
        # print(res.json())
    return res.json().get('id')


def add_group(task_id):
    add_group_url = 'http://uat-edgediag.bilivideo.com/groups/5f060322ccf0ed0f6970cdbf/tasks/' + task_id + '?su=mayday'
    try:
        res = requests.put(add_group_url)
    except Exception as error:
        logging.error(f'Add task to group error: {error}')
    return res.json()


def get_task_result(task_id):
    interval_time = 1
    time_out = 20
    get_task_result_url = 'http://uat-edgediag.bilivideo.com/results/general/' + task_id + '?su=mayday'
    start_time = time.time()
    end_time = start_time + time_out
    while time.time() < end_time:
        try:
            res = requests.get(get_task_result_url)
            time.sleep(interval_time)
        except Exception as error:
            logging.error(f'Get task result error: {error}')
        if res.json():
            break
    return res.json()



def main2():
    ip_list = get_ip_list()
    ip_port_list = get_ip_port_list(ip_list)
    # ip_port_list = ['183.146.25.70:1935', '36.248.39.69:1935', '119.84.43.194:1935']
    task_id = create_batch_tasks(ip_port_list)
    print(task_id)



def main1():
    while True:
        ip_list = ["183.146.25.70"]
        try:
            task_id = create_task(ip_list)
            print("task_id", task_id)
            add_group_res = add_group(task_id)
            print(add_group_res)
            task_result = get_task_result(task_id)
            logging.info(task_result)
        except requests.exceptions.RequestException as error:
            logging.error(error)
        time.sleep(900)
        print("next task")


if __name__ == "__main__":
    init_local_log(settings.LOGGING_LEVEL)
    init_ops_log("playtest")

    # main1()
    main2()
