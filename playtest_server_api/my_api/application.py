import requests
import time
import logging
import pymongo


# task_id_list = []

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['str_playtest']
task_col = db['tasks']


def str_format(str_str):
    str_str = str_str.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    print(str_str)
    new_ip_port_list = []
    new_ip_port_list.append(str_str)
    return new_ip_port_list


def list_format(str_list):
    str_list = str_list.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    # print("str_list", str_list)
    str_list = str_list[1:-1]
    ip_port_list = str_list.split(',')
    new_ip_port_list = []

    for ip_port in ip_port_list:
        ip_port = ip_port[1:-1]
        new_ip_port_list.append(ip_port)
    return new_ip_port_list


def create_task(ip, port):
    url = 'http://uat-edgediag.bilivideo.com/tasks'
    ip_port = ip + ":" + port
    data = {
      "name": "srt 拨测",
      "type": "srt",
      "cycle": "onetime",
      "detail": {
          "ip_ports": [ip_port]
      },
      "timeout": 3
    }
    params = {
        'su': 'mayday'
    }
    try:
        create_task_res = requests.post(url=url, json=data, params=params)
        print(create_task_res)
    except Exception as error:
        logging.error(f'Create task error: {error}')

    task_dict = {}
    task_id = create_task_res.json().get("id")
    task_dict["id"] = task_id
    task_dict["ip_ports"] = str_format(ip_port)
    task_dict["creat_time"] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # task_id_list.append(task_dict)
    task_col.insert_one(task_dict)
    print("Add task to mongo success！")

    add_group_res = add_group(task_id)
    print(add_group_res)
    if add_group_res['inserted'] == True:
        print("Add task to group success！")
    else:
        print("Add task to group error！")
    if create_task_res.json()["id"] != None:
        print("Create task success！ id ：", create_task_res.json()["id"])
    return create_task_res.json()


def create_tasks(ip_port_list):
    url = 'http://uat-edgediag.bilivideo.com/tasks'
    ip_port_list = list_format(ip_port_list)
    data = {
      "name": "srt 拨测",
      "type": "srt",
      "cycle": "onetime",
      "detail": {
          "ip_ports": ip_port_list
      },
      "timeout": 3
    }
    params = {
        'su': 'mayday'
    }
    try:
        create_task_res = requests.post(url=url, json=data, params=params)
        print(create_task_res)
    except Exception as error:
        logging.error(f'Create task error: {error}')

    task_dict = {}
    task_id = create_task_res.json().get("id")
    task_dict["id"] = task_id
    task_dict["ip_ports"] = ip_port_list
    task_dict["creat_time"] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    task_col.insert_one(task_dict)
    print("Add task to mongo success！")

    add_group_res = add_group(task_id)
    print(add_group_res)
    if add_group_res['inserted'] == True:
        print("Add task to group success！")
        print("Create task to group success！")
    else:
        print("Add task to group error！")
    if create_task_res.json()["id"] != None:
        print("Create task success！ id ：", create_task_res.json()["id"])
    return create_task_res.json()


def get_all_tasks():
    tasks = list(task_col.find({}, {'_id': 0}))
    return tasks


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
    count = 1
    while time.time() < end_time:
        try:
            res = requests.get(get_task_result_url)
            time.sleep(interval_time)
            print(count, res)
            count += 1
        except Exception as error:
            logging.error(f'Get task result error: {error}')
        if res.json():
            break
    return res.json()


# def get_task_status(task_id):
#     get_task_status_url = 'http://uat-edgediag.bilivideo.com/status?su=mayday'
#     # get_task_status_url = 'http://uat-edgediag.bilivideo.com/status' + task_id + '?su=mayday'
#     try:
#         get_status_res = requests.get(get_task_status_url)
#     except Exception as error:
#         logging.error(f'get task_status error: {error}')
#     # res = get_status_res.json().get("status")
#     # return res.json()
#     task_stauts_dict = {}
#     for info in get_status_res.json():
#         if info.get("task_id") == task_id:
#             task_stauts_dict["task_id"] = task_id
#             task_stauts_dict["status"] = info.get("status")
#             return task_stauts_dict
def get_task_status(task_id):
    get_task_status_url = 'http://uat-edgediag.bilivideo.com/status' + task_id + '?su=mayday'
    try:
        get_status_res = requests.get(get_task_status_url)
    except Exception as error:
        logging.error(f'get task_status error: {error}')
    if get_status_res.json().get("status"):
        task_stauts_dict = {}
        task_stauts_dict["task_id"] = task_id
        task_stauts_dict["status"] = get_status_res.get("status")
        return task_stauts_dict
    else:
        return []


def stop_task(task_id):
    stop_task_res = "wait"
    return stop_task_res