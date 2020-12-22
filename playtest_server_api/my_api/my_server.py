#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import my_api.application

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


class IndexHandler(RequestHandler):
    def get(self):
        self.render('api.html')


class HealthHandler(RequestHandler):
    def get(self):
        per = {
            "version": "1.0.0",
            "status": "alive"
        }
        self.write(per)


class CreateTaskHandler(RequestHandler):
    def get(self):
        self.render('createtask.html')

    def post(self):
        ip = self.get_body_argument("ip")
        port = self.get_body_argument("port")
        res = my_api.application.create_task(ip, port)
        res = dict(res)
        self.write(res)


class CreateTasksHandler(RequestHandler):
    def get(self):
        self.render('createtasks.html')

    def post(self):
        ip_port_list = self.get_body_argument("ip_port_list")
        res = my_api.application.create_tasks(ip_port_list)
        res = dict(res)
        self.write(res)
        # ip_port_list = self.get_body_argument("ip_port_list")
        # my_api.application.create_tasks(ip_port_list)
        # self.write(ip_port_list)
        # ip_port_list = self.get_body_argument("ip_port_list")
        # print(type(ip_port_list))
        # self.write(ip_port_list)


class GetTasksHandler(RequestHandler):
    def get(self):
        res = my_api.application.get_all_tasks()
        res = str(res)
        self.write(res)


class GetResultHander(RequestHandler):
    def get(self):
        self.render('getresult.html')

    def post(self):
        task_id = self.get_body_argument("task_id")
        res = my_api.application.get_task_result(task_id)
        print(res)
        res = str(res)
        self.write(res)


class GetTaskResultHander(RequestHandler):
    def get(self, task_id):
        res = my_api.application.get_task_result(task_id)
        print(res)
        res = str(res)
        self.write(res)


class GetStatusHander(RequestHandler):
    def get(self):
        self.render('getstatus.html')

    def post(self):
        task_id = self.get_body_argument("task_id")
        res = my_api.application.get_task_status(task_id)
        res = str(res)
        self.write(res)


class GetTaskStatusHander(RequestHandler):
    def get(self, task_id):
        res = my_api.application.get_task_status(task_id)
        print(res)
        res = str(res)
        self.write(res)


class StopTaskHander(RequestHandler):
    def get(self):
        self.render('stop.html')

    def post(self):
        task_id = self.get_body_argument("task_id")
        res = my_api.application.stop_task(task_id)
        self.write(res)


def start():
    application = Application(
        [
            (r'/', IndexHandler),
            (r'/health', HealthHandler),
            (r'/createtask', CreateTaskHandler),
            (r'/createtasks', CreateTasksHandler),
            (r'/tasks', GetTasksHandler),
            (r'/getresult', GetResultHander),
            (r'/getresult/(\w+)', GetTaskResultHander),
            (r'/getstatus', GetStatusHander),
            (r'/getstatus/(\w+)', GetTaskStatusHander),
            (r'/stop', StopTaskHander),
        ],
        autoreload=True)
    application.listen(8765)
    IOLoop.current().start()


if __name__ == "__main__":
    start()
