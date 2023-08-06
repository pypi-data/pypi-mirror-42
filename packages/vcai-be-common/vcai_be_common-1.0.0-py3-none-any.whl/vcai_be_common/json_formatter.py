# -*- coding: utf-8 -*-
import logging
import json
import datetime
import random
import time


def new_gid():
    str = ""
    for i in range(9):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return time.strftime("%Y%m%d%H%M%S", time.localtime()) + str


class Gid:
    unique_flownum = None

    @classmethod
    def get_gid(cls):
        if not cls.unique_flownum:
            cls.unique_flownum = new_gid()
        return cls.unique_flownum


REMOVE_ATTR = ["filename", "name", "funcName", "processName", "process", "levelno",
               "lineno", "module", "exc_text", "stack_info", "created", "msecs", "relativeCreated",
               "exc_info", "msg",
               "args"]


class JSONFormatter(logging.Formatter):
    unique_flownum = Gid.get_gid()

    def format(self, record):
        extra_record = self.build_record(record)
        extra = {}
        self.set_unique_flownum(extra, extra_record)
        self.set_format_time(extra)  # set time
        extra['level'] = extra_record['levelname']
        extra['logger'] = extra_record['pathname']
        extra['thread'] = extra_record['threadName']
        if isinstance(record.msg, dict):
            extra['msg'] = record.msg  # set message
        else:
            if record.args:
                extra['msg'] = "'" + record.msg + "'," + str(record.args).strip('()')
            else:
                extra['msg'] = record.msg
        if record.exc_info:
            extra['stackTrace'] = self.formatException(record.exc_info)
        if self._fmt == 'pretty':
            return json.dumps(extra, indent=1, ensure_ascii=False)
        else:
            return json.dumps(extra, ensure_ascii=False)

    @classmethod
    def build_record(cls, record):
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in REMOVE_ATTR
        }

    @classmethod
    def set_format_time(cls, extra):
        now = datetime.datetime.now()
        format_time = now.strftime("%Y-%m-%d %H:%M:%S" + ".%03d" % (now.microsecond / 1000))
        extra['time'] = format_time
        return format_time

    @classmethod
    def set_unique_flownum(cls, extra, extra_record):
        if extra_record['uniqueFlowNo']:
            extra['uniqueFlowNo'] = extra_record['uniqueFlowNo']
        else:
            extra['uniqueFlowNo'] = JSONFormatter.unique_flownum
