# -*- coding: utf-8 -*-
import time
import logging
import ujson as json
from collections import OrderedDict
from utils.lancer_logger.jsonlogger import JsonFormatter
from utils.ipc_client import IPCClient


class EdgeSimpleFormatter(JsonFormatter):

    def __init__(self, template, *args, **kwargs):
        super(EdgeSimpleFormatter, self).__init__(*args, **kwargs)
        self.template = template

    def log_to_template(self, log):
        # overwrite
        return json.dumps(log)

    def format(self, record):
        """Formats a log record and serializes to json"""
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None
        else:
            record.message = record.getMessage()
        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get('exc_info'):
            message_dict['exc_info'] = self.formatException(record.exc_info)
        if not message_dict.get('exc_info') and record.exc_text:
            message_dict['exc_info'] = record.exc_text

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)

        return "{logid}{ts}{log_detail}".format(
            logid=self.prefix,
            ts=int(time.time() * 1000),
            log_detail=self.log_to_template(log_record)
        )


class IPCLogFormatter(EdgeSimpleFormatter):

    def log_to_template(self, log):
        return self.template.format(
            instance_id=log.get('instance_id', 'unknown_instance'),
            level=log.get('level', 'EEE'),
            lineno=log.get('lineno', 0),
            job_id=log.get('job_id', 'unknown_job'),
            queen=log.get('queen', 'unknown_queen'),
            log=log['log'],
            module=log.get("module", "unknown module")
        )


class IPCLogHandler(logging.Handler):

    def __init__(self):
        super(IPCLogHandler, self).__init__()
        self.client = IPCClient()

    def emit(self, record):
        msg = self.format(record)
        try:
            self.client.send_logging(msg=msg)
        except Exception as exc:
            logging.error(exc, exc_info=True)
