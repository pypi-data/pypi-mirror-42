# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2018-01-10 16:27:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2018-08-10 11:05:00

"""Usage:

import easylogger
easylogger.init("test")

import logging
logger = logging.getLogger(__name__)
logger.info("test log")
"""
import os
import logging
import logging.handlers

# from cloghandler import ConcurrentRotatingFileHandler

DEFAULT_FILE_CONF = dict(
    file_path="logs",
    file_name=None,
    fmt="%(asctime)s [%(name)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    # when to specify the type of interval
    # S for seconds; M for minutes, H for hours, D for day; W for week
    when="D",
    interval=1,
    # backupCount files will be kept
    backupCount=50,

)


def init(name="easylog", level="DEBUG", console=True, file=True, file_conf=DEFAULT_FILE_CONF, log_file_name=None):
    logger = logging.getLogger(name)
    # print "\n\n in init log , logging.getLogger() is ", logger
    logger.setLevel(level)

    if console:
        console_handler = logging.StreamHandler()

        fmt = "%(asctime)s [%(name)s:%(lineno)d] %(levelname)s: %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if file:
        # update default file config
        FILE_CONF = DEFAULT_FILE_CONF.copy()
        FILE_CONF.update(file_conf)

        file_path = FILE_CONF.get("file_path")
        if not os.path.isdir(file_path):
            os.mkdir(file_path)

        file_name = FILE_CONF.get("filename") or name or log_file_name
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename="%s/%s.log" % (file_path, file_name),
            when=FILE_CONF.get("when"),
            interval=FILE_CONF.get("interval"),
            backupCount=FILE_CONF.get("backupCount"),
            delay=False,
            utc=False
        )

        # file_handler = ConcurrentRotatingFileHandler(
        #     "%s/%s.log" % (file_path, file_name),
        #     "a",
        #     # 超过10m 大小
        #     1024 * 1024 * 10
        # )

        formatter = logging.Formatter(FILE_CONF.get("fmt"), datefmt=FILE_CONF.get("datefmt"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def init_sql_log():
    """写入数据库的日志"""
    pass
