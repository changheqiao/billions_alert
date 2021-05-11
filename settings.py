# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/11
"""
import logging
import os
import sys

env = os.getenv('env', None)
if not env and len(sys.argv) > 1:
    env = sys.argv[-1]
if not env:
    env = 'PROD'

TIME_ZONE = 'Asia/Chongqing'
redis_config = {
    # "host":"172.31.140.255",
    "host": "127.0.0.1",
    "port": 6379,
    "max": 4
}
mysql_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "app",
    "password": "654321",
    "db": "billions_alert"
}
service = {
    "port": 8080,
}

grafana = {
    "domain": "https://f.alphaconsensus.com"
}

if "TEST" == env:
    # redis_config['host'] = '111.229.193.232'
    redis_config['host'] = '127.0.0.1'
    mysql_config['user'] = 'api'
    mysql_config['host'] = '127.0.0.1'
    mysql_config['password'] = 'api'
    mysql_config['db'] = 'marketdata'

STANDARD_FORMAT = '%(asctime)s %(levelname)s [%(threadName)s:%(thread)d][%(filename)s:%(lineno)d]# %(message)s'
PLAIN_FORMAT = '%(asctime)s|%(filename)s|%(message)s'


def build_logging_config(log_name, log_file_name, fmt="text"):
    log_dir = "./logs"
    _cfg = dict(
        version=1,
        disable_existing_loggers=False,
        formatters=dict(
            text=dict(
                format=STANDARD_FORMAT
            ),
            plain=dict(
                format=PLAIN_FORMAT
            )
        ),
        handlers=dict(
            text={
                "level": logging.DEBUG,
                "class": 'logging.handlers.RotatingFileHandler',
                "formatter": fmt,
                "filename": '%s/%s.log' % (log_dir, log_file_name),
                "maxBytes": 2000000,  # 日志大小 300 bit
                "backupCount": 8,
                "encoding": 'utf-8'
            },

        ),
        loggers={
            log_name: {
                'handlers': ['text'],
                'level': logging.DEBUG
            }
        }
    )
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return _cfg
