# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/12
"""

from common import singleton, wxapi, caches
from common.resources import common_r as redis_cache
from exception import exceptions
import time
from settings import WX_API


WX_DEFAULT_APP_ID = WX_API["appid"]


@singleton
class AccessTokenCacheService:

    def refresh_access_token(self, params):
        platform = params.get("p", "wx")
        _appid = params.get("id", None)
        access_token = ""
        if "wx" == platform:
            if not _appid:
                _appid = WX_DEFAULT_APP_ID
            lock_key = "lock:refresh:access:{}:token:{}".format(_appid, "wx")
            key = "wx:access_token:{}".format(_appid)
            access_token = caches.get_from_cache(key)
            if not access_token:
                if redis_cache.set(name=lock_key, value='1', nx=True, ex=10):
                    try:
                        access_token = caches.get_from_cache(key)
                        if not access_token:
                            cfg = self.fetch_cfg(_appid, platform)
                            jsonrs = wxapi.get_access_token(cfg)
                            if "access_token" in jsonrs:
                                access_token = jsonrs["access_token"]
                                expires_in = jsonrs["expires_in"]
                                timeout = expires_in - 5 * 60
                                caches.put_to_cache(key, access_token, timeout)
                    finally:
                        redis_cache.delete(lock_key)
        return access_token

    def fetch_access_token(self, params):

        rs = {}
        platform = params.get("p", "wx")

        if "wx" == platform:
            key = "wx:access_token"
            access_token = caches.get_from_cache(key)
            if access_token:
                rs["access_token"] = access_token
            else:
                access_token = self.refresh_access_token(dict(p="wx"))
                dog = 20
                while not access_token and dog > 0:
                    time.sleep(0.5)
                    dog = dog - 1
                    access_token = self.refresh_access_token(dict(p="wx"))
                if not access_token:
                    raise exceptions.InvalidAccessTokenError("AccessToken获取失败")
                rs["access_token"] = access_token
        return rs

    def fetch_wx_access_token(self):
        return self.fetch_access_token(dict(p="wx"))


access_token_cache = AccessTokenCacheService()
