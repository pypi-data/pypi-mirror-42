import logging
from logging.config import fileConfig
import vcai_be_common.log_constant as log_constant

class Log:
    fileConfig('log_conf.ini')
    log = logging.getLogger()

    @classmethod
    def info(cls, msg, **context):
        if context:
            unique_flownum = context[log_constant.UNIQUE_FLOW_NO]
        else:
            unique_flownum = None
        Log.log.info(msg, extra={log_constant.UNIQUE_FLOW_NO: unique_flownum})

    @classmethod
    def warn(cls, msg, **context):
        if context:
            unique_flownum = context[log_constant.UNIQUE_FLOW_NO]
        else:
            unique_flownum = None
        Log.log.warn(msg, extra={log_constant.UNIQUE_FLOW_NO: unique_flownum})

    @classmethod
    def error(cls, msg, **context):
        if context:
            unique_flownum = context[log_constant.UNIQUE_FLOW_NO]
        else:
            unique_flownum = None
        Log.log.error(msg, extra={log_constant.UNIQUE_FLOW_NO: unique_flownum}, exc_info=True)
