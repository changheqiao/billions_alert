# -*- coding: utf-8 -*-
"""
Created by susy at 2020/8/17
"""
import common
import redis
import settings
import socket

logger = common.get_default_logger()

options = {
    socket.SO_KEEPALIVE: 120,
    socket.TCP_KEEPCNT: 32
}
db_offset = 20
db_index = db_offset + 1
pool = redis.ConnectionPool(host=settings.redis_config["host"], port=settings.redis_config["port"], db=db_index,
                            max_connections=settings.redis_config["max"])
r = redis.StrictRedis(connection_pool=pool, socket_keepalive=True, socket_keepalive_options=options,
                      socket_connect_timeout=15)
r._db_index = db_index

db_index = db_offset + 2
pool = redis.ConnectionPool(host=settings.redis_config["host"], port=settings.redis_config["port"], db=db_index,
                            max_connections=settings.redis_config["max"])

timer_r = redis.StrictRedis(connection_pool=pool, socket_keepalive=True, socket_keepalive_options=options,
                            socket_connect_timeout=15)
timer_r._db_index = db_index

db_index = db_offset
pool = redis.ConnectionPool(host=settings.redis_config["host"], port=settings.redis_config["port"], db=db_index,
                            max_connections=settings.redis_config["max"])

common_r = redis.StrictRedis(connection_pool=pool, socket_keepalive=True, socket_keepalive_options=options,
                             socket_connect_timeout=15)
common_r._db_index = db_index

