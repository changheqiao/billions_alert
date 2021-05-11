# -*- coding: utf-8 -*-
"""
Created by susy at 2020/8/22
"""
from common.resources import r as redis_cache
import time
import common
logger = common.get_default_logger()


class Lock:
    timeout = 10

    def __init__(self, key):
        self.key = key
        self._lock = 0

    def __enter__(self):
        while self._lock != 1:
            self._lock = redis_cache.set(name=self.key, value='1', nx=True, ex=self.timeout)
            if self._lock == 1:
                return self._lock
            else:
                time.sleep(0.1)
        return self._lock

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._lock:
            redis_cache.delete(self.key)
        if exc_tb:
            logger.warning('[Exit {}]: Exited with exception[{}] raised.'.format(self.key, exc_value))
            logger.exception(exc_tb)
        return True


class CheckLock:
    def __init__(self, key):
        self.key = key

    def __enter__(self):
        while redis_cache.exists(self.key):
            time.sleep(0.1)
        return True

    def __exit__(self, exc_type, exc_value, exc_tb):
        return True

