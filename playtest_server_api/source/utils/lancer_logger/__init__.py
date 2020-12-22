# -*- coding: utf-8 -*-
"""
# -*- coding: utf-8 -*-
import logging
import sys
from functools import partial
from utils.edge_logger.logger import EdgeSimpleLogHandler, EdgeLogReporter, EdgeWorkerFormater
from utils.log import init_std_log
from utils.edge_logger.jsonlogger import JsonFormatter
from multiprocessing import Event, Queue
import signal



def register_exit_handler(event=None):
    signal.signal(signal.SIGTERM, partial(signal_handler, event))
    signal.signal(signal.SIGINT, partial(signal_handler, event))
    signal.signal(signal.SIGQUIT, partial(signal_handler, event))


def init_edge_log(log_queue, app_id, log_template):
    logger = logging.getLogger()
    loghandler = EdgeSimpleLogHandler(log_queue)
    formater = EdgeWorkerFormater(log_template, prefix=str(app_id))
    loghandler.setFormatter(formater)
    logger.addHandler(loghandler)
    logger.setLevel('INFO')


def app_demo(event):
    import time
    i = 1
    while not event.is_set():
        print('in app demo')
        logging.info(i)
        i += 1
        time.sleep(1)

event = Event()
global_log_queue = Queue()

if __name__ == '__main__':
    log_template = '{instance_id}|{level}|{lineno}|{log}|{stage}|{stage_id}|{task_id}'
    init_edge_log(global_log_queue, '003228', log_template)


    lancer_api = "http://dataflow.biliapi.com/log/system"
    log_reporter = EdgeLogReporter(global_log_queue, event, lancer_api)

    def signal_handler(event, sig, frame):
        if event:
            logging.info('set event: {}'.format(event))
            log_reporter.terminate()
            event.set()
        logging.info('received signal: {}, frame {}, exit soon...'.format(sig, frame.f_code))

    register_exit_handler(event)
    log_reporter.start()

    # todo app
    app_demo(event)

    log_reporter.join()

"""

